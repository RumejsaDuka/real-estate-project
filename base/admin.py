from django.contrib import admin

from .models import (
    Property,
    PropertyImage,
    Agent,
    PropertyFeature,
    Inquiry
)

admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Agent)
admin.site.register(PropertyFeature)
admin.site.register(Inquiry)