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
