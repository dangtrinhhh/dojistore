from rest_framework import serializers
from .models import Carts, Cart_Details, Orders, Order_Details

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'

class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Details
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Details
        fields = '__all__'
