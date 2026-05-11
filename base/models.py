from django.db import models


class Property(models.Model):
    BADGE_CHOICES = [
        ('sale', 'For Sale'),
        ('luxury', 'Luxury'),
        ('new', 'New'),
        ('reduced', 'Reduced'),
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sqft = models.IntegerField(default=0)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='sale')
    image = models.CharField(max_length=500 , default='static/images/abouthero.jpg')  # URL ose path
    featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    lot_size = models.CharField(max_length=50, blank=True)
    garage = models.IntegerField(default=0)
    pool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return self.title

    def get_price_display(self):
        return f"${self.price:,.0f}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    interest = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.CharField(max_length=500)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name