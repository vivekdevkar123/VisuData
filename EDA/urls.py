from django.urls import path
from .views import *
urlpatterns = [
    path('uploadfile/',FileUpload,name="upload-file")
]