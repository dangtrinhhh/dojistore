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
    cart.total_amount += int(product.price) * quantity
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
    print(cart_detail.cart.total_quantity)
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
#_________________________________________________________________

# Create your views here.
# def add_to_cart(request, product_id):
#     # Lấy hoặc tạo giỏ hàng cho người dùng
#     cart, created = Carts.objects.get_or_create(user=request.user)

#     # Thêm sản phẩm vào giỏ hàng
#     product = Products.objects.get(pk=product_id)
#     cart.products.add(product)

#     return redirect('cart')

# def view_cart(request):
#     # Lấy giỏ hàng của người dùng
#     user = request.user  # Đây là user đăng nhập, nếu có
#     cart = None
#     if user.is_authenticated:
#         user_profile, created = Users.objects.get_or_create(user=user)
#         cart, created = Carts.objects.get_or_create(user=user_profile)
    
#     print(cart)
#     # Hiển thị thông tin giỏ hàng trong template
#     return render(request, 'cart.html', {'cart': cart})

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

ZALOPAY_KEY_1 = "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn"
ZALOPAY_APP_ID = 2554
ZALOPAY_CALLBACK_URL = "https://7166-2405-4802-90a4-50f0-edb2-3867-9f02-35a7.ngrok-free.app/api/payment-status/"

def generate_app_trans_id(order_id, created_at):
    return created_at.strftime('%y%m%d') + '_' + str(order_id)

def generate_created_at():
    return datetime.utcnow()

def generate_embed_data(provider):
    preferred_payment_method = []
    embed_data = {
        'preferred_payment_method': preferred_payment_method,
        'redirecturl': 'https://7166-2405-4802-90a4-50f0-edb2-3867-9f02-35a7.ngrok-free.app/order/payment/success'
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

# Create Order ZaloPay
def create_order(customer_full_name, total_amount, order, provider_id, items):
    created_time = generate_created_at()
    payload = {
        'key1': ZALOPAY_KEY_1,
        'app_id': ZALOPAY_APP_ID,
        'app_user': customer_full_name,
        'app_trans_id': str(generate_app_trans_id(order['id'], created_time)),
        'app_time': int(time.mktime(created_time.timetuple())) * 1000,  # Convert to milliseconds
        'amount': int(total_amount),
        'bank_code': "",
        'embed_data': generate_embed_data(provider_id),
        'item': generate_item_data(items),
        'description': 'DoubleTBad - Thanh toán đơn hàng #{}'.format(order["displayId"]),
        'callback_url': ZALOPAY_CALLBACK_URL,
    }
    mac_string = str(payload['app_id']) + '|' + payload['app_trans_id'] + '|' + payload['app_user'] + '|' + str(payload['amount']) + '|' + str(payload['app_time']) + '|' + payload['embed_data'] + '|' + payload['item']
    payload['mac'] = hash_mac_by_key1(mac_string)
    # payload['mac'] = hash_mac_by_key1('|'.join(str(value) for value in payload.values() if value is not None))

    print(payload)
    # Send request
    response = requests.post('https://sb-openapi.zalopay.vn/v2/create', json=payload)
    if response.status_code == 200:
        data = response.json()
        print('Processed image:', data)
        # Do something with the response data
    else:
        print('Error when processing image:', response.text)

@api_view(['POST'])
def process_payment(request):
    # create_order('John Doe', 100000, {
    #         'id': '123456',
    #         'description': 'Order description',
    #         'displayId': 'ADHBW23NHJSW4JK',
    #         # Các thông tin khác về đơn hàng
    #     }, '123', [
    #         {'name': 'Item 1', 'quantity': 2, 'price': 50},
    #         {'name': 'Item 2', 'quantity': 1, 'price': 30},
    #         # Các mặt hàng khác trong đơn hàng
    #     ]
    # )
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
        "app_user": "Dang Trinh",
        "app_time": int(round(time() * 1000)), # miliseconds
        "embed_data": json.dumps({}),
        "item": json.dumps([{}]),
        "amount": 50000,
        "description": "DoubleTBad - Thanh toán đơn hàng #"+str(transID),
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
    result = request.data.items()
    print("Result:" + result)
    # Process result

    return Response(result, status=status.HTTP_200_OK)
