from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)

class Product_Types(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.name

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_type_id = models.ForeignKey(Product_Types, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=100000)
    price = models.CharField(max_length=500)
    pricesale = models.CharField(max_length=500, default=price)
    status = models.CharField(max_length=500)
    quantity = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        if self.pricesale and self.price:
            self.on_sale = float(self.pricesale) < float(self.price)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product_Images(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_images')
    url = models.ImageField(upload_to='images/products', null=True, blank=True, max_length=50000)

    def __str__(self):
        return f"{self.product.name} - Image {self.product_image_id}"

