from django.shortcuts import render, redirect
from .models import Cart, Product

# Create your views here.
def add_to_cart(request, product_id):
    # Lấy hoặc tạo giỏ hàng cho người dùng
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Thêm sản phẩm vào giỏ hàng
    product = Product.objects.get(pk=product_id)
    cart.products.add(product)

    return redirect('cart')

def view_cart(request):
    # Lấy giỏ hàng của người dùng
    cart = Cart.objects.get(user=request.user)
    
    # Hiển thị thông tin giỏ hàng trong template
    return render(request, 'cart.html', {'cart': cart.products.all()})