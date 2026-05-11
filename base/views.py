from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Property, ContactMessage, TeamMember
from .forms import ContactForm


PROPERTIES_DATA = [
    {'id': 1, 'title': 'Maple Ridge Family Home', 'location': 'Austin, Texas', 'price': 485000, 'beds': 4, 'baths': 3, 'sqft': 2340, 'badge': 'sale', 'image': 'images/maple.jpg', 'featured': False},
    {'id': 2, 'title': 'Harborview Waterfront Villa', 'location': 'Miami, Florida', 'price': 1250000, 'beds': 6, 'baths': 5, 'sqft': 5100, 'badge': 'luxury', 'image': 'images/waterfront.jpg', 'featured': True},
    {'id': 3, 'title': 'Westside Contemporary Townhouse', 'location': 'Denver, Colorado', 'price': 310000, 'beds': 3, 'baths': 2, 'sqft': 1780, 'badge': 'new', 'image': 'images/townhouse.webp', 'featured': False},
    {'id': 4, 'title': 'Oakwood Estates Residence', 'location': 'Nashville, Tennessee', 'price': 675000, 'beds': 5, 'baths': 4, 'sqft': 3620, 'badge': 'sale', 'image': 'images/oakwood.jpg', 'featured': False},
    {'id': 5, 'title': 'Summit Mountain Retreat', 'location': 'Aspen, Colorado', 'price': 540000, 'beds': 4, 'baths': 3, 'sqft': 2890, 'badge': 'reduced', 'image': 'images/mountain.jpg', 'featured': False},
    {'id': 6, 'title': 'Downtown Loft Apartment', 'location': 'Chicago, Illinois', 'price': 228000, 'beds': 2, 'baths': 1, 'sqft': 1100, 'badge': 'new', 'image': 'images/loft.avif', 'featured': False},
]

TEAM_DATA = [
    {'name': 'Sarah Mitchell', 'role': 'Founding Partner & CEO', 'bio': '15+ years of experience and a passion for matching people with the homes they deserve.', 'image': 'images/agent2.jpg'},
    {'name': 'James Harrington', 'role': 'Senior Property Specialist', 'bio': 'Luxury residential expert across Florida and California with 12 years in the field.', 'image': 'images/agent1.jpg'},
    {'name': 'David Park', 'role': 'Investment Advisor', 'bio': 'Expert in multi-family and commercial investment properties nationwide.', 'image': 'images/david.jpg'},
    {'name': 'Elena Vasquez', 'role': "Buyer's Agent", 'bio': 'Specializes in guiding first-time buyers through every step of the process.', 'image': 'images/agent3.jpg'},
]


def index(request):
    featured_properties = PROPERTIES_DATA[:6]
    return render(request, 'index.html', {
    'properties': featured_properties,
})


def listings(request):
    properties = PROPERTIES_DATA.copy()
    
    # Filters nga GET parameters
    location = request.GET.get('location', '').lower()
    max_price = request.GET.get('price', '')
    min_beds = request.GET.get('beds', '')
    prop_type = request.GET.get('type', '')

    if location:
        properties = [p for p in properties if location in p['location'].lower()]
    if max_price:
        properties = [p for p in properties if p['price'] <= int(max_price)]
    if min_beds:
        properties = [p for p in properties if p['beds'] >= int(min_beds)]
    if prop_type:
        properties = [p for p in properties if p['badge'] == prop_type]

    return render(request, 'listings.html', {
        'properties': properties,
        'total_count': len(PROPERTIES_DATA),
        'filtered_count': len(properties),
        'filters': {
            'location': request.GET.get('location', ''),
            'price': max_price,
            'beds': min_beds,
            'type': prop_type,
        }
    })


def about(request):
    return render(request, 'about.html', {
        'team': TEAM_DATA,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                interest=form.cleaned_data.get('interest', ''),
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Mesazhi u dërgua me sukses!')
            return redirect('contact')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def property_detail(request, pk):
    # Gjej property nga lista statike (ose nga DB)
    prop = next((p for p in PROPERTIES_DATA if p['id'] == pk), PROPERTIES_DATA[1])
    similar = [p for p in PROPERTIES_DATA if p['id'] != pk and p['badge'] == prop.get('badge')][:3]
    
    return render(request, 'property.html', {
        'property': prop,
        'similar_properties': similar,
    })