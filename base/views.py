from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import ContactForm
from .models import Agent, Property


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
        'location': str,
        'price': int,
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
                location=self.filters['location'],
                max_price=self.filters['price'],
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
        return context

    def get_gallery_photos(self, property_obj):
        fallback_slots = [
            ('Exterior', 'Main property exterior', property_obj.image.url),
            ('Bedroom', 'Bedroom and sleeping area', static('images/bedroom.jpg')),
            ('Bathroom', 'Bathroom details', static('images/salom.jpg')),
            ('Pool', 'Outdoor pool and leisure area', static('images/waterfront.jpg')),
        ]

        photos = [
            {
                'label': fallback_slots[0][0],
                'caption': property_obj.title,
                'url': property_obj.image.url,
            }
        ]

        for image in property_obj.gallery.all()[:3]:
            fallback_label, fallback_caption, _ = fallback_slots[min(len(photos), len(fallback_slots) - 1)]
            label = image.caption or image.get_photo_type_display()
            caption = image.caption or f'{image.get_photo_type_display()} photo'

            if image.photo_type == image.PhotoType.OTHER and not image.caption:
                label = fallback_label
                caption = fallback_caption

            photos.append({
                'label': label,
                'caption': caption,
                'url': image.image.url,
            })

        used_labels = {photo['label'] for photo in photos}
        for label, caption, url in fallback_slots[1:]:
            if len(photos) >= 4:
                break
            if label in used_labels:
                continue
            photos.append({'label': label, 'caption': caption, 'url': url})

        return photos[:4]


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
        messages.success(self.request, 'Thanks. Your message has been sent.')
        return super().form_valid(form)


index = HomeView.as_view()
listings = PropertyListView.as_view()
property_detail = PropertyDetailView.as_view()
about = AboutView.as_view()
contact = ContactView.as_view()
