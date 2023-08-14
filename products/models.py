from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    
# class Product(models.Model):
#     title = models.CharField(max_length=100)
#     price = models.CharField(max_length=100)
#     description = models.CharField(max_length=10000)
#     createdAt = models.DateTimeField(default=datetime.now, blank=True)