from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=1000)
    phone = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)