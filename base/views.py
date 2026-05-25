from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import ContactForm, LoginForm, MessageForm, PropertyForm, RegisterForm
from .models import Agent, Favorite, Message, Property


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = (
            Property.objects
            .featured()
            .with_listing_relations()[:6]
        )
        return context


class PropertyListView(ListView):
    model = Property
    template_name = 'listings.html'
    context_object_name = 'properties'
    paginate_by = 12

    allowed_filters = {
        'q': str,
        'location': str,
        'min_price': int,
        'max_price': int,
        'beds': int,
        'type': str,
        'listing_type': str,
    }

    def get_queryset(self):
        self.filters = self.get_filters()
        return (
            Property.objects
            .with_listing_relations()
            .search(
                query=self.filters['q'],
                location=self.filters['location'],
                min_price=self.filters['min_price'],
                max_price=self.filters['max_price'],
                min_beds=self.filters['beds'],
                badge=self.filters['type'],
                listing_type=self.filters['listing_type'],
            )
        )

    def get_filters(self):
        filters = {}

        for key, caster in self.allowed_filters.items():
            raw_value = self.request.GET.get(key, '').strip()
            if not raw_value:
                filters[key] = ''
                continue

            try:
                filters[key] = caster(raw_value)
            except (TypeError, ValueError):
                filters[key] = ''

        valid_badges = {choice.value for choice in Property.Badge}
        valid_listing_types = {choice.value for choice in Property.ListingType}

        if filters['type'] and filters['type'] not in valid_badges:
            filters['type'] = ''

        if filters['listing_type'] and filters['listing_type'] not in valid_listing_types:
            filters['listing_type'] = ''

        return filters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Property.objects.count()
        context['filtered_count'] = self.object_list.count()
        context['filters'] = {key: str(value) if value else '' for key, value in self.filters.items()}
        if self.request.user.is_authenticated:
            context['favorite_ids'] = set(
                Favorite.objects
                .filter(user=self.request.user)
                .values_list('property_id', flat=True)
            )
        else:
            context['favorite_ids'] = set()
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property.html'
    context_object_name = 'property'
    pk_url_kwarg = 'pk'
    queryset = Property.objects.with_listing_relations()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_property = self.object
        similar_properties = (
            Property.objects
            .with_listing_relations()
            .exclude(pk=current_property.pk)
            .filter(listing_type=current_property.listing_type)
            .order_by('-featured', '-created_at')[:3]
        )

        if len(similar_properties) < 3:
            similar_properties = (
                Property.objects
                .with_listing_relations()
                .exclude(pk=current_property.pk)
                .order_by('-featured', '-created_at')[:3]
            )

        context['similar_properties'] = similar_properties
        context['gallery_photos'] = self.get_gallery_photos(current_property)
        context['message_form'] = MessageForm()
        context['is_favorite'] = (
            self.request.user.is_authenticated and
            Favorite.objects.filter(user=self.request.user, property=current_property).exists()
        )
        return context

    def get_gallery_photos(self, property_obj):
        photos = [
            {
                'label': 'Foto kryesore',
                'caption': property_obj.title,
                'url': property_obj.image.url,
            }
        ]

        for image in property_obj.gallery.all():
            label = image.caption or image.get_photo_type_display()
            caption = image.caption or image.get_photo_type_display()

            photos.append({
                'label': label,
                'caption': caption,
                'url': image.image.url,
            })

        return photos


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agents'] = Agent.objects.all()
        return context


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Faleminderit. Mesazhi juaj u dergua.')
        return super().form_valid(form)


class CurrencyIdentifierView(TemplateView):
    template_name = 'currency_identifier.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Dolet nga llogaria.')
        return super().dispatch(request, *args, **kwargs)


class AuthView(View):
    template_name = 'auth/auth.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account')

        active_tab = request.GET.get('tab')
        if active_tab not in {'login', 'register'}:
            active_tab = 'register' if request.resolver_match.url_name == 'register' else 'login'

        return self.render_auth(request, active_tab=active_tab)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('account')

        action = request.POST.get('action')
        if action == 'register':
            register_form = RegisterForm(request.POST)
            login_form = LoginForm(request)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, 'Llogaria u krijua me sukses.')
                return redirect('account')
            return self.render_auth(
                request,
                login_form=login_form,
                register_form=register_form,
                active_tab='register',
            )

        login_form = LoginForm(request, data=request.POST)
        register_form = RegisterForm()
        if login_form.is_valid():
            login(request, login_form.get_user())
            messages.success(request, 'Hyret me sukses.')
            return redirect(request.GET.get('next') or 'account')

        return self.render_auth(
            request,
            login_form=login_form,
            register_form=register_form,
            active_tab='login',
        )

    def render_auth(self, request, login_form=None, register_form=None, active_tab='login'):
        from django.shortcuts import render

        context = {
            'login_form': login_form or LoginForm(request),
            'register_form': register_form or RegisterForm(),
            'active_tab': active_tab,
        }
        return render(request, self.template_name, context)


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Prona u shtua me sukses.')
        return super().form_valid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied('You can only edit your own properties.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Prona u perditesua me sukses.')
        return super().form_valid(form)


class FavoriteToggleView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            property=property_obj,
        )

        if created:
            messages.success(request, 'Prona u ruajt ne favorite.')
        else:
            favorite.delete()
            messages.success(request, 'Prona u hoq nga favoritet.')

        return redirect(request.POST.get('next') or property_obj.get_absolute_url())


class FavoriteListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(f'{reverse("account")}#favorites')


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = (
            Favorite.objects
            .filter(user=self.request.user)
            .select_related('property', 'property__owner', 'property__agent')
        )
        context['my_properties'] = (
            Property.objects
            .filter(owner=self.request.user)
            .with_listing_relations()
        )
        context['received_messages'] = (
            Message.objects
            .filter(receiver=self.request.user)
            .select_related('sender', 'property')
        )
        context['sent_messages'] = (
            Message.objects
            .filter(sender=self.request.user)
            .select_related('receiver', 'property')
        )
        return context


class InboxRedirectView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(f'{reverse("account")}#messages')


class PropertyMessageView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        receiver = property_obj.owner

        if receiver is None:
            messages.error(request, 'Kjo prone nuk ka perdorues marres per mesazhin.')
            return redirect(property_obj.get_absolute_url())

        if receiver == request.user:
            messages.error(request, 'Nuk mund t\'i dergoni mesazh vetes per pronen tuaj.')
            return redirect(property_obj.get_absolute_url())

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.property = property_obj
            message.save()
            messages.success(request, 'Mesazhi u dergua me sukses.')
        else:
            messages.error(request, 'Ju lutem shkruani nje mesazh te vlefshem.')

        return redirect(property_obj.get_absolute_url())


index = HomeView.as_view()
listings = PropertyListView.as_view()
property_detail = PropertyDetailView.as_view()
about = AboutView.as_view()
contact = ContactView.as_view()
currency_identifier = CurrencyIdentifierView.as_view()
login_view = AuthView.as_view()
logout_view = UserLogoutView.as_view()
register = AuthView.as_view()
property_create = PropertyCreateView.as_view()
property_update = PropertyUpdateView.as_view()
toggle_favorite = FavoriteToggleView.as_view()
favorites = FavoriteListView.as_view()
account = AccountDashboardView.as_view()
inbox = InboxRedirectView.as_view()
send_property_message = PropertyMessageView.as_view()
