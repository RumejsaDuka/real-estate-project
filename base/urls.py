from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('',     views.index,      name='index'),
    path('listings/',   views.listings,  name='listings'),
    path('about/',      views.about,     name='about'),
    path('contact/',      views.contact, name='contact'),
    path('property/<int:pk>/', views.property_detail, name='property'),
]