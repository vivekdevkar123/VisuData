from django.urls import path
from .views import *
urlpatterns = [
    path('uploadfile/',FileUpload,name="upload-file"),
    path('history/',History,name="history"),
    path('del/<slug:id>',Delete_Record,name='delete-record'),
    path('<slug:id>',Analysis,name='data-analysis'),
]