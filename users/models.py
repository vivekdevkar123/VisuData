from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    nationality = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

