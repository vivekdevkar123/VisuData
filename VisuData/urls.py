from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('myadminpannel/', admin.site.urls),
    path('',include('mainapp.urls')),
    path("users/", include("users.urls")),
    path('data/',include('EDA.urls')),
    path('visu/',include('Visulization.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)