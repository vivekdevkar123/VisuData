from django.db import models

# Create your models here.


class ContactU(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    description = models.TextField()

    def __str__(self):
        return self.name
