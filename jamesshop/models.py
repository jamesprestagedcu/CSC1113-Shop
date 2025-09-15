from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    preferences = models.JSONField(default=dict)
    
    def __str__(self):
        return self.username

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    product_image = models.FileField(upload_to='products')