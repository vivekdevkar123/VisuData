from django.db import models
from EDA.models import Dataset

# Create your models here.

class Plot(models.Model):
    plot_id = models.AutoField(primary_key=True)
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return str(self.plot_id)