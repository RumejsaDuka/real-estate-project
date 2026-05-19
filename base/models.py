from django.db import models


class Property(models.Model):

    LISTING_TYPE = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )

    PROPERTY_BADGES = (
        ('luxury', 'Luxury'),
        ('new', 'New'),
        ('reduced', 'Reduced'),
    )

    title = models.CharField(max_length=255)

    # 🔥 this is the important one now
    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPE,
        default='sale'
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
        choices=PROPERTY_BADGES,
        blank=True,
        null=True
    )

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"

class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(
        upload_to='property_gallery/'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Agent(models.Model):

    name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=255,
        default='Senior Property Specialist'
    )

    phone = models.CharField(max_length=30)

    email = models.EmailField()

    image = models.ImageField(
        upload_to='agents/'
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=5.0
    )

    reviews_count = models.PositiveIntegerField(default=0)

    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PropertyFeature(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='features'
    )

    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature


class Inquiry(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    name = models.CharField(max_length=255)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.property.title}"