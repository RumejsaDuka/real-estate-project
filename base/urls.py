from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'listings/',
        views.listings,
        name='listings'
    ),

    path(
        'property/<int:pk>/',
        views.property_detail,
        name='property'
    ),

    path(
        'about/',
        views.about,
        name='about'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),

]