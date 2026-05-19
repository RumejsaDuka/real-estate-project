from django.shortcuts import render, get_object_or_404
from .models import (
    Property,
    PropertyImage,
    Agent,
    PropertyFeature,
    Inquiry
)


# HOME PAGE
def index(request):
    featured_properties = Property.objects.filter(featured=True)[:6]

    context = {
        'featured_properties': featured_properties
    }
    return render(request, 'index.html', context)


# LISTINGS PAGE
def listings(request):
    properties = Property.objects.all().order_by('-created_at')

    location     = request.GET.get('location')
    price        = request.GET.get('price')
    beds         = request.GET.get('beds')
    property_type = request.GET.get('type')
    listing_type = request.GET.get('listing_type')   # ← NEW: 'sale' or 'rent'

    # FILTERS
    if location:
        properties = properties.filter(location__icontains=location)

    if price:
        properties = properties.filter(price__lte=price)

    if beds:
        properties = properties.filter(beds__gte=beds)

    if property_type:
        properties = properties.filter(badge=property_type)

    if listing_type:                                  # ← NEW
        properties = properties.filter(listing_type=listing_type)

    context = {
        'properties': properties,
        'total_count': Property.objects.count(),
        'filtered_count': properties.count(),
        'filters': {
            'location':     location     or '',
            'price':        price        or '',
            'beds':         beds         or '',
            'type':         property_type or '',
            'listing_type': listing_type or '',       # ← NEW
        }
    }
    return render(request, 'listings.html', context)


# SINGLE PROPERTY PAGE
def property_detail(request, pk):
    property = get_object_or_404(Property, id=pk)

    # Pull similar listings of the SAME type (sale/rent) first,
    # fall back to any 3 if not enough.
    similar_properties = (
        Property.objects
        .exclude(id=property.id)
        .filter(listing_type=property.listing_type)
        .order_by('-created_at')[:3]
    )
    if similar_properties.count() < 3:
        similar_properties = Property.objects.exclude(id=property.id)[:3]

    context = {
        'property': property,
        'similar_properties': similar_properties,
    }
    return render(request, 'property.html', context)


# CONTACT PAGE
def contact(request):
    return render(request, 'contact.html')


# ABOUT PAGE
def about(request):
    agents = Agent.objects.all()
    context = {'agents': agents}
    return render(request, 'about.html', context)