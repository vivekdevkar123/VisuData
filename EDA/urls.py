from django.urls import path
from .views import *
urlpatterns = [
    path('uploadfile/',FileUpload,name="upload-file"),
    path('history/',History,name="history"),
    path('del/<slug:id>',Delete_Record,name='delete-record'),
    path('<slug:id>',Analysis,name='data-analysis'),
    path('datacleaning/mean/<slug:id>',mean_imputation,name='mean_imputation_view'),
    path('datacleaning/median/<slug:id>',median_imputation,name='median_imputation_view'),
    path('datacleaning/mode/<slug:id>',mode_imputation,name='mode_imputation_view'),
    path('download/<slug:id>',DownloadDataset,name='DownloadDataset'),
    path('addnote/<slug:id>',AddNote,name='Add-note'),
    path('note/delete/<slug:id>',DeleteNote,name='Delete-note'),
]