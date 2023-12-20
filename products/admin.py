from django.contrib import admin
from .models import Products, Users, Product_Types, Product_Images

# Register your models here.
admin.site.register(Products)
admin.site.register(Users)
admin.site.register(Product_Types)
admin.site.register(Product_Images)