from django.db import models
from django.urls import reverse


class PropertyQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def for_sale(self):
        return self.filter(listing_type=Property.ListingType.SALE)

    def for_rent(self):
        return self.filter(listing_type=Property.ListingType.RENT)

    def with_listing_relations(self):
        return self.select_related('agent').prefetch_related('gallery', 'features')

    def search(self, *, location='', max_price='', min_beds='', badge='', listing_type=''):
        queryset = self

        if location:
            queryset = queryset.filter(location__icontains=location.strip())

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_beds:
            queryset = queryset.filter(beds__gte=min_beds)

        if badge:
            queryset = queryset.filter(badge=badge)

        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)

        return queryset


class Property(models.Model):
    class ListingType(models.TextChoices):
        SALE = 'sale', 'For Sale'
        RENT = 'rent', 'For Rent'

    class Badge(models.TextChoices):
        LUXURY = 'luxury', 'Luxury'
        NEW = 'new', 'New'
        REDUCED = 'reduced', 'Reduced'

    title = models.CharField(max_length=255)
    listing_type = models.CharField(
        max_length=10,
        choices=ListingType.choices,
        default=ListingType.SALE,
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    beds = models.PositiveIntegerField(default=1)
    baths = models.PositiveIntegerField(default=1)
    sqft = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='properties/')
    badge = models.CharField(
        max_length=20,
        choices=Badge.choices,
        blank=True,
        null=True,
    )
    featured = models.BooleanField(default=False)
    agent = models.ForeignKey(
        'Agent',
        on_delete=models.SET_NULL,
        related_name='properties',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PropertyQuerySet.as_manager()

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name_plural = 'Properties'
        indexes = [
            models.Index(fields=['listing_type', '-created_at']),
            models.Index(fields=['featured', '-created_at']),
            models.Index(fields=['badge']),
        ]

    def __str__(self):
        return f'{self.title} ({self.get_listing_type_display()})'

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    @property
    def is_for_rent(self):
        return self.listing_type == self.ListingType.RENT

    @property
    def display_price_suffix(self):
        return '/month' if self.is_for_rent else ''

    @property
    def price_per_sqft(self):
        if not self.sqft:
            return None
        return self.price / self.sqft


class PropertyImage(models.Model):
    class PhotoType(models.TextChoices):
        EXTERIOR = 'exterior', 'Exterior'
        LIVING = 'living', 'Living Room'
        BEDROOM = 'bedroom', 'Bedroom'
        BATHROOM = 'bathroom', 'Bathroom'
        KITCHEN = 'kitchen', 'Kitchen'
        POOL = 'pool', 'Pool'
        VIEW = 'view', 'View'
        OTHER = 'other', 'Other'

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery',
    )
    image = models.ImageField(upload_to='property_gallery/')
    photo_type = models.CharField(
        max_length=20,
        choices=PhotoType.choices,
        default=PhotoType.OTHER,
    )
    caption = models.CharField(max_length=120, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        label = self.caption or self.get_photo_type_display()
        return f'{label} for {self.property.title}'


class Agent(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, default='Senior Property Specialist')
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    image = models.ImageField(upload_to='agents/')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    reviews_count = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PropertyFeature(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='features',
    )
    feature = models.CharField(max_length=255)

    class Meta:
        ordering = ['feature']

    def __str__(self):
        return self.feature


class Inquiry(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries',
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f'{self.name} - {self.property.title}'


class ContactMessage(models.Model):
    class Interest(models.TextChoices):
        BUYING = 'buying', 'Buying a Property'
        SELLING = 'selling', 'Selling a Property'
        RENTING = 'renting', 'Renting / Leasing'
        INVESTMENT = 'investment', 'Investment Advice'
        VALUATION = 'valuation', 'Property Valuation'
        GENERAL = 'general', 'General Inquiry'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    interest = models.CharField(
        max_length=100,
        choices=Interest.choices,
        blank=True,
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'
