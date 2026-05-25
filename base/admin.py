from django.contrib import admin

from .models import (
    Agent,
    ContactMessage,
    Favorite,
    Inquiry,
    Message,
    Property,
    PropertyFeature,
    PropertyImage,
)


admin.site.site_header = 'Grand Realty Admin'
admin.site.site_title = 'Grand Realty Admin'
admin.site.index_title = 'Administration'


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
        'owner',
        'created_at',
    )
    list_filter = ('listing_type', 'badge', 'featured', 'created_at')
    search_fields = ('title', 'location', 'description', 'owner__username')
    list_editable = ('featured',)
    autocomplete_fields = ('agent', 'owner')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (PropertyImageInline, PropertyFeatureInline)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'rating', 'reviews_count', 'has_linkedin')
    search_fields = ('name', 'email', 'role')
    list_filter = ('role',)

    fieldsets = (
        ('General Information', {
            'fields': ('name', 'role', 'image', 'bio'),
        }),
        ('Contact and Social Links', {
            'description': 'Agent contact details and social profile links.',
            'fields': ('phone', 'email', 'linkedin'),
        }),
        ('Reviews', {
            'fields': ('rating', 'reviews_count'),
        }),
    )

    @admin.display(description='LinkedIn?', boolean=True)
    def has_linkedin(self, obj):
        return bool(obj.linkedin)


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    search_fields = ('user__username', 'property__title')
    list_filter = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'property', 'created_at', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'property__title', 'text')
    list_filter = ('created_at', 'is_read')
    readonly_fields = ('created_at',)


admin.site.register(PropertyImage)
admin.site.register(PropertyFeature)
