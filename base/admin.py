from django.contrib import admin

from .models import (
    Agent,
    ContactMessage,
    Inquiry,
    Property,
    PropertyFeature,
    PropertyImage,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'photo_type', 'caption', 'sort_order')


class PropertyFeatureInline(admin.TabularInline):
    model = PropertyFeature
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'listing_type',
        'price',
        'location',
        'beds',
        'baths',
        'featured',
        'agent',
        'created_at',
    )
    list_filter = ('listing_type', 'badge', 'featured', 'created_at')
    search_fields = ('title', 'location', 'description')
    list_editable = ('featured',)
    autocomplete_fields = ('agent',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = (PropertyImageInline, PropertyFeatureInline)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'rating', 'reviews_count')
    search_fields = ('name', 'email', 'role')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'property__title', 'message')
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'interest', 'subject', 'created_at')
    list_filter = ('interest', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)


admin.site.register(PropertyImage)
admin.site.register(PropertyFeature)
