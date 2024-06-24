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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

#_________________________________API________________________________
# Trong views.py của ứng dụng của bạn
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib import messages

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            auth.login(request, user)
            messages.success(request, f"Login successfully! Welcome back, {username}.")
            return Response({'refreshToken': str(refresh), 'accessToken': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            messages.info(request, 'Invalid username or password.')
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    if 'Authorization' not in request.headers:
        return Response({"message": "JWT is missing in request header."}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh_token = request.session.get('refresh_token')
    print(refresh_token)

    # Lấy thông tin sản phẩm từ request data (POST data)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)  # Mặc định là 1 nếu không có quantity

    try:
        user = request.user  # Đây là user đăng nhập, nếu có
        user_profile, created = Users.objects.get_or_create(user=user)

        try:
            cart, created = Carts.objects.get_or_create(user=user_profile)
        except Exception as e:
            cart = Carts.objects.filter(user=user_profile).order_by('-created_at').first()
            messages.error(request, f"Lỗi lấy giỏ hàng: {str(e)}")

        # Lấy thông tin sản phẩm từ database
        product = Products.objects.get(pk=product_id)

        # Tạo hoặc cập nhật chi tiết giỏ hàng cho sản phẩm
        try:
            cart_detail, created = Cart_Details.objects.get_or_create(cart=cart, product=product)
        except Exception as e:
            cart_detail = Cart_Details.objects.filter(user=user_profile).order_by('-created_at').first()
            messages.error(request, f"Lỗi lấy chi tiết giỏ hàng: {str(e)}")
            

        cart_detail.quantity += quantity
        cart_detail.save()

        # Cập nhật thông tin giỏ hàng
        cart.total_quantity += quantity
        cart.total_amount += int(product.pricesale) * quantity
        cart.save()

        # Serialize giỏ hàng để trả về thông tin mới nhất
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
    except Users.DoesNotExist:
        return Response({"message": "Fail to add product to cart."}, status=status.HTTP_404_NOT_FOUND)
    

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


from django.db import transaction
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    user_profile, created = Users.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Extract order information from request data
        payment_method = request.data.get('payment_method')
        total_amount = request.data.get('total_amount')
        note = request.data.get('note')
        status = request.data.get('status', 'Pending')  # default status if not provided

        order_details = request.data.get('order_details', [])

        # Create an order transactionally
        with transaction.atomic():
            # Create the order instance
            order = Orders.objects.create(
                user=user_profile,
                payment_method=payment_method,
                total_amount=total_amount,
                note=note,
                status=status
            )

            # Create order details for each item in order_details
            for item in order_details:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                price = item.get('price')

                # Fetch the product instance
                product = Products.objects.get(product_id=product_id)

                Order_Details.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

            # Optionally, you may want to perform additional operations such as updating stock levels, etc.

        # Serialize and return the order response
        serializer = OrderSerializer(order)
        return Response(serializer.data, '201')

    return Response({"message": "Lỗi tạo đơn hàng"})

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
    serializer_class = CartDetailSerializer

    def dispatch(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return Response({"message": "JWT is missing in request header."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        cart_id = self.kwargs['pk']
        return Cart_Details.objects.filter(cart__cart_id=cart_id)

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



# from .retrieve_information import main
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

# CALLBACK_URL='http://127.0.0.1:8000/'
CALLBACK_URL='https://e836-2405-4802-8029-8a90-1df5-bdcb-357c-8534.ngrok-free.app/'
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
        'redirecturl': f"{CALLBACK_URL}order/payment/success/",
        'user_id': provider
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
    userid = request.data.get('userid')
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
        "embed_data": generate_embed_data(userid),
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
#     user = request.user
#     user_profile, created = Users.objects.get_or_create(user=user)
    print(request.data)
    type = request.data.get('type')
    # request_data = request.data.get('data')
    # print(f"{CALLBACK_URL}order/payment/success")
    data_dict = json.loads(request.data['data'])

    # Phân tích dữ liệu JSON từ chuỗi JSON trong khóa "embed_data"
    embed_data_dict = json.loads(data_dict['embed_data'])

    # Lấy giá trị của khóa "user_id"
    user_id = embed_data_dict['user_id']
    
    if (type == 1):
        # user_id = request_data['embed_data']['user_id']
        print("🚀 ~ user_id:", user_id)
        
        try:
            user_profile = Users.objects.get(user=user_id)
            # Lấy giỏ hàng của người dùng
            # cart, created = Carts.objects.get_or_create(user=user_profile.id)
            try:
                cart, created = Carts.objects.get_or_create(user=user_profile)
                order, created = Orders.objects.get_or_create(user=user_profile).order_by('-created_at').first()
                order.status = 'paid'
                order.save()
                
            except Exception as e:
                cart = Carts.objects.filter(user=user_profile).order_by('-created_at').first()
                messages.error(request, f"Lỗi lấy giỏ hàng: {str(e)}")
                
            # Xóa tất cả chi tiết giỏ hàng của giỏ hàng đó
            cart_details = Cart_Details.objects.filter(cart=cart)
            # Xóa chi tiết giỏ hàng
            cart_details.delete()
            # Xóa giỏ hàng
            cart.delete()
        except Users.DoesNotExist:
            print({'error': 'Not found'})

        return redirect(f"{CALLBACK_URL}order/payment/success")
    else:
        return redirect(f"{CALLBACK_URL}order/payment/fail")
    print("Result:" + str(type))

    
    # f"{CALLBACK_URL}order/payment/success"
    # Process result

    return Response(type, status=status.HTTP_200_OK)
