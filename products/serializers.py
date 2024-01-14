# serializers.py
from rest_framework import serializers
from .models import Products, Product_Images, Product_Types

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = ('product_image_id', 'url',)

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ('product_id', 'name', 'description', 'price', 'pricesale', 'status', 'quantity', 'quantity_sold', 'created_at', 'last_updated', 'images')

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Types
        fields = ('product_type_id', 'name', 'last_updated')

class ProductWithTypeSerializer(serializers.Serializer):
    type = ProductTypeSerializer()
    products = ProductSerializer(many=True)
