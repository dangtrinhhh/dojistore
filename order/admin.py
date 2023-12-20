from django.contrib import admin
from .models import Carts, Cart_Details, Orders, Order_Details

# Register your models here.
admin.site.register(Carts)
admin.site.register(Cart_Details)
admin.site.register(Orders)
admin.site.register(Order_Details)
