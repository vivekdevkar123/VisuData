from django.db import models
from django.conf import settings
    
class Dataset(models.Model):
    dataset_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dataset_name = models.CharField(max_length=100)
    uploaded_file = models.FileField(upload_to='datasets/')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dataset_name
    

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)
    note = models.CharField(max_length=1000)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note
    