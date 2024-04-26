from django.shortcuts import render, redirect
from .models import Carts, Cart_Details, Orders, Order_Details
from products.models import Products, Product_Types, Product_Images, Users
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Carts, Cart_Details
from .serializers import CartSerializer, CartDetailSerializer
from decimal import Decimal
from django.db.models import F

#_________________________________API________________________________

@api_view(['POST'])
def add_to_cart(request):
    # Lấy thông tin sản phẩm từ request data (POST data)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)  # Mặc định là 1 nếu không có quantity

    # Lấy hoặc tạo giỏ hàng cho người dùng hiện tại
    user = request.user  # Đây là user đăng nhập, nếu có
    user_profile, created = Users.objects.get_or_create(user=user)
    cart, created = Carts.objects.get_or_create(user=user_profile)

    # Lấy thông tin sản phẩm từ database
    product = Products.objects.get(pk=product_id)

    # Tạo hoặc cập nhật chi tiết giỏ hàng cho sản phẩm
    cart_detail, created = Cart_Details.objects.get_or_create(cart=cart, product=product)
    cart_detail.quantity += quantity
    cart_detail.save()

    # Cập nhật thông tin giỏ hàng
    cart.total_quantity += quantity
    cart.total_amount += int(product.pricesale) * quantity
    cart.save()

    # Serialize giỏ hàng để trả về thông tin mới nhất
    cart_serializer = CartSerializer(cart)
    return Response(cart_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_cart_item_quantity(request, cart_detail_id):
    try:
        cart_detail = Cart_Details.objects.select_related('cart').get(pk=cart_detail_id)
    except Cart_Details.DoesNotExist:
        return Response({"message": "Cart detail not found"}, status=status.HTTP_404_NOT_FOUND)

    new_quantity = request.data.get('quantity')

    if new_quantity is None:
        return Response({"message": "Quantity parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Update total_quantity in cart
    cart_detail.cart.total_quantity += (int(new_quantity) - int(cart_detail.quantity))
    cart_detail.cart.save()

    # Update total_amount in cart
    product = cart_detail.product
    price = product.price
    if product.pricesale:
        price = product.pricesale
    cart_detail.cart.total_amount += (int(new_quantity) - int(cart_detail.quantity)) * int(price)
    cart_detail.cart.save()

    # Update the quantity
    cart_detail.quantity = new_quantity
    cart_detail.save()

    # Serialize the updated cart detail
    serializer = CartDetailSerializer(cart_detail)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_cart_item(request, cart_detail_id):
    try:
        cart_detail = Cart_Details.objects.select_related('cart').get(pk=cart_detail_id)
    except Cart_Details.DoesNotExist:
        return Response({"message": "Cart detail not found"}, status=status.HTTP_404_NOT_FOUND)

    # Lấy sản phẩm và số lượng trước khi xóa
    product = cart_detail.product
    quantity = cart_detail.quantity

    # Xóa cart detail
    cart_detail.delete()

    # Cập nhật total_quantity và total_amount của cart
    cart = cart_detail.cart
    cart.total_quantity -= int(quantity)
    price = product.price if not product.pricesale else product.pricesale
    cart.total_amount -= int(quantity) * int(price)
    cart.save()

    return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_order(request):
    user = request.user
    if request.method == 'POST':
        order_data = request.data
        order_data['user'] = user.id 

        order = Orders()
        # Gọi hàm generate_order_code từ instance
        order_data['order_code'] = order.generate_order_code()

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            # Lấy danh sách chi tiết đơn hàng từ dữ liệu yêu cầu
            order_details_data = request.data.get('order_details', [])
            if not isinstance(order_details_data, list):
                return Response({'error': 'Invalid order details format'}, status=status.HTTP_400_BAD_REQUEST)

            # Tạo serializer cho từng chi tiết đơn hàng và lưu vào cơ sở dữ liệu
            for detail_data in order_details_data:
                # Lấy thông tin sản phẩm từ order_details
                product_id = detail_data.get('product_id')
                price = detail_data.get('price')

                # Kiểm tra xem product_id có tồn tại không
                if not product_id:
                    return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

                # Kiểm tra xem sản phẩm có tồn tại trong cơ sở dữ liệu không
                try:
                    product = Products.objects.get(pk=product_id)
                except Products.DoesNotExist:
                    return Response({'error': f'Product with ID {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

                # Cập nhật detail_data với sản phẩm và order tương ứng
                detail_data['product'] = product_id
                detail_data['price'] = price
                detail_data['order'] = order.pk

                # Tạo serializer cho chi tiết đơn hàng và lưu vào cơ sở dữ liệu
                detail_serializer = OrderDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def order_detail(request, order_id):
    try:
        order = Orders.objects.get(order_id=order_id)
        order_serializer = OrderSerializer(order)
        details = Order_Details.objects.filter(order=order)
        details_serializer = OrderDetailSerializer(details, many=True)
        return Response({'order': order_serializer.data, 'order_details': details_serializer.data})
    except Orders.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#_______________________________________API__________________________________

from rest_framework import generics
from rest_framework.response import Response
from .models import Carts, Cart_Details, Orders, Order_Details
from .serializers import CartSerializer, CartDetailSerializer, OrderSerializer, OrderDetailSerializer
from rest_framework import status
from rest_framework.decorators import api_view

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer

class CartDetailListCreateView(generics.ListCreateAPIView):
    queryset = Cart_Details.objects.all()
    serializer_class = CartDetailSerializer

class CartDetailDetailView(generics.ListAPIView):
    # generics.RetrieveUpdateDestroyAPIView
    serializer_class = CartDetailSerializer
    def get_queryset(self):
        cart_id = self.kwargs['pk']
        return Cart_Details.objects.filter(cart__cart_id=cart_id)
    # queryset = Cart_Details.objects.all()

class OrderListCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class OrderDetailListCreateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order_Details.objects.all()
    serializer_class = OrderDetailSerializer

class OrderDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order_Details.objects.all()
    serializer_class = OrderDetailSerializer



from .retrieve_information import main
from django.middleware.csrf import get_token
from django.http import JsonResponse

from django.http import JsonResponse

def get_csrf_token(request):
    response = JsonResponse({'csrf_token': 'your_csrf_token'})
    response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3001'
    return response

import hashlib
import json
import time
from datetime import datetime
import requests
from time import time
from datetime import datetime
import json, hmac, hashlib, urllib.request, urllib.parse, random

CALLBACK_URL='https://8a1d-2405-4802-90a4-50f0-e40d-1c7a-1846-bd8a.ngrok-free.app/'
ZALOPAY_KEY_1 = "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn"
ZALOPAY_APP_ID = 2554
ZALOPAY_CALLBACK_URL = f"{CALLBACK_URL}api/payment-status/"

def generate_app_trans_id(order_id, created_at):
    return created_at.strftime('%y%m%d') + '_' + str(order_id)

def generate_created_at():
    return datetime.utcnow()

def generate_embed_data(provider):
    preferred_payment_method = []
    embed_data = {
        'preferred_payment_method': preferred_payment_method,
        'redirecturl': f"{CALLBACK_URL}order/payment/success/"
    }
    return json.dumps(embed_data)

def generate_item_data(items):
    return json.dumps(items or [])

def hash_mac_by_key1(data):
    return hash_mac(ZALOPAY_KEY_1, data)

def hash_mac(key, data):
    hmac = hashlib.sha256(key.encode('utf-8'))
    hmac.update(data.encode('utf-8'))
    return hmac.hexdigest()

@api_view(['POST'])
def process_payment(request):
    username = request.data.get('username')
    price = request.data.get('price')
    config = {
        "app_id": 2553,
        "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
        "key2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
        "endpoint": "https://sb-openapi.zalopay.vn/v2/create"
    }
    transID = random.randrange(1000000)
    print(random.randrange(1000000))
    order = {
        "app_id": config["app_id"],
        "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID), # mã giao dich có định dạng yyMMdd_xxxx
        "app_user": username,
        "app_time": int(round(time() * 1000)), # miliseconds
        "embed_data": generate_embed_data(''),
        "item": json.dumps([{}]),
        "amount": price,
        "description": "DoubleTBad - Thanh toán đơn hàng #" + str(transID),
        "bank_code": "zalopayapp",
        "callback_url": ZALOPAY_CALLBACK_URL,
    }

    # app_id|app_trans_id|app_user|amount|apptime|embed_data|item
    data = "{}|{}|{}|{}|{}|{}|{}".format(order["app_id"], order["app_trans_id"], order["app_user"], 
    order["amount"], order["app_time"], order["embed_data"], order["item"])

    order["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

    response = urllib.request.urlopen(url=config["endpoint"], data=urllib.parse.urlencode(order).encode())
    result = json.loads(response.read())

    for k, v in result.items():
        print("{}: {}".format(k, v))

    # image_file = request.data.get('image')
    
    # personal_information = main(image_file)

    return Response(result, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def payment_status(request):
    user = request.user
    user_profile, created = Users.objects.get_or_create(user=user)
    type = request.data.get('type')
    # print(f"{CALLBACK_URL}order/payment/success")
    
    if (type == 1):
        user = request.user
        user_profile, created = Users.objects.get_or_create(user=user)
        try:
            # Lấy giỏ hàng của người dùng
            cart, created = Carts.objects.get_or_create(user=user_profile.id)
            # Xóa tất cả chi tiết giỏ hàng của giỏ hàng đó
            cart_details = Cart_Details.objects.filter(cart=cart)
            # Xóa chi tiết giỏ hàng
            cart_details.delete()
            # Xóa giỏ hàng
            cart.delete()
        except Carts.DoesNotExist:
            print({'error': 'Cart not found'})

        return redirect(f"{CALLBACK_URL}order/payment/success")
    else:
        return redirect(f"{CALLBACK_URL}order/payment/fail")
    print("Result:" + str(type))

    
    # f"{CALLBACK_URL}order/payment/success"
    # Process result

    return Response(result, status=status.HTTP_200_OK)
