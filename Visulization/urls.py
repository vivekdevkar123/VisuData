from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:id>/',Visulization_Home,name='Visulization-Home'),
    path('scatter/<slug:id>', scatter_plot, name='scatter_plot'),
]