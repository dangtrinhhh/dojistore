from django.db import models
from datetime import datetime
from products.models import Products, Users
import uuid

class Carts(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)

class Cart_Details(models.Model):
    cart_details_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=50, unique=True)
    payment_method = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)
    
    def generate_order_code(self):
        # Tạo một chuỗi UUID
        unique_id = str(uuid.uuid4().int)
        
        # Lấy 12 kí tự ngẫu nhiên từ UUID
        order_code = unique_id[:12].upper()

        return order_code

    def save(self, *args, **kwargs):
        # Nếu order_code chưa được thiết lập, tạo một order_code mới
        if not self.order_code:
            self.order_code = self.generate_order_code()

        super().save(*args, **kwargs)

class Order_Details(models.Model):
    order_details_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(default=datetime.now, blank=True)