from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('about/', about, name='AboutUs'),
    path('contact/', contact, name='MyContact'),
    path('search/', search, name='search'),
]
