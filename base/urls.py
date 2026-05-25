from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('properties/new/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('property/<int:pk>/message/', views.send_property_message, name='send_property_message'),
    path('account/', views.account, name='account'),
    path('favorites/', views.favorites, name='favorites'),
    path('inbox/', views.inbox, name='inbox'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('currency-identifier/', views.currency_identifier, name='currency_identifier'),
]
