from rest_framework import serializers
from .models import Carts, Cart_Details, Orders, Order_Details
from products.models import Products, Product_Types, Product_Images, Users

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'
 
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = ('product_image_id', 'url')

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='product_images')

    class Meta:
        model = Products
        fields = ('product_id', 'name', 'description', 'price', 'pricesale', 'status', 'quantity', 'quantity_sold', 'created_at', 'last_updated', 'images')
              
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = ('product_id', 'name', 'description', 'price', 'pricesale', 'status', 'quantity', 'quantity_sold', 'created_at', 'last_updated')

class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart_Details
        fields = ('cart_details_id', 'quantity', 'created_at', 'product', 'cart')

# class CartDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart_Details
#         fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Details
        fields = '__all__'
