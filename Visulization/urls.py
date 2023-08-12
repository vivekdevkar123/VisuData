from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:id>/',Visulization_Home,name='Visulization-Home'),
    path('scatter/<slug:id>', scatter_plot, name='scatter_plot'),
    path('line/<slug:id>', line_plot, name='line_plot'),
    path('bar/<slug:id>', bar_chart, name='bar_chart'),
    path('histogram/<slug:id>', histogram, name='histogram'),
    path('pie/<slug:id>', pie_chart, name='pie-char'),
    path('save_plot/<int:id>', Save_Plot, name='Save-Plot'),
    path('delete_plot/<int:id>', Delete_Plot, name='Delete-Plot'),
]