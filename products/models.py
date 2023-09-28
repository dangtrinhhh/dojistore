from django.db import models
from datetime import datetime
# import os

# Create your models here.

class Product(models.Model):
    image = models.ImageField(upload_to='images/products', null=True, blank=True, max_length=50000)
    name = models.CharField(max_length=500)
    typeProduct = models.CharField(max_length=500)
    price = models.CharField(max_length=500)
    pricesale = models.CharField(max_length=500, default=price)
    description = models.CharField(max_length=100000)
    
    def save(self, *args, **kwargs):
        if self.pricesale and self.price:
            self.onSale = float(self.pricesale) < float(self.price)
        super(Product, self).save(*args, **kwargs)
    onSale = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=datetime.now, blank=True)