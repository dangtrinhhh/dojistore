from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Products, Product_Types, Product_Images
from blogs.models import Blogs
from order.models import Carts, Cart_Details, Orders, Order_Details
from .models import Users
from allauth.account.views import PasswordResetView
from django.http import HttpResponseRedirect
from django.urls import reverse
from allauth.account.utils import filter_users_by_email
import numpy as np
from django_filters.rest_framework import DjangoFilterBackend

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = filter_users_by_email(email)

        if not users:
            # User not found, display an error message
            messages.error(self.request, "This email address hasn't been signed up yet.")
            return self.render_to_response(self.get_context_data(form=form))

        # Proceed with the password reset process
        return super().form_valid(form)

def getProductOrderedType(num_products=None):
    # Lấy danh sách tất cả các loại sản phẩm
    product_types = Product_Types.objects.all()

    # Tạo một danh sách để lưu trữ sản phẩm và hình ảnh tương ứng
    products_with_images = []

    # Lặp qua từng loại sản phẩm và lấy danh sách sản phẩm tương ứng
    for product_type in product_types:
        # Lấy danh sách sản phẩm, sắp xếp theo created_at
        products = Products.objects.filter(product_type_id=product_type.product_type_id).order_by('-created_at')

        # Nếu num_products được cung cấp, chỉ lấy số lượng sản phẩm mong muốn
        if num_products is not None:
            products = products[:num_products]

        # Tạo một danh sách hình ảnh cho từng sản phẩm
        products_and_images = []

        for product in products:
            # Lấy danh sách hình ảnh cho sản phẩm hiện tại
            images = Product_Images.objects.filter(product=product)

            # Thêm sản phẩm và danh sách hình ảnh vào danh sách chung
            products_and_images.append({
                'product': product,
                'images': images
            })

        # Thêm danh sách sản phẩm và hình ảnh vào danh sách chung
        products_with_images.append({
            'product_type': product_type,
            'products_and_images': products_and_images
        })
    print(products_with_images)
    return products_with_images

# Create your views here.
def index(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    
    # print(request.META.get("REMOTE_ADDR"))
    
    product_types = Product_Types.objects.all()
    products_with_images = getProductOrderedType()
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    
    if request.method == "POST":
        email = request.POST.get('email', '')
        if email == '':
            username = request.POST['username']
            password = request.POST['password']
            print(username + "/" + password)
            
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, f"Login successfully! Welcome back, {username}.")
                return redirect('/')
            else:
                messages.info(request, 'Invalid username or password.')
                return redirect('/login')
        else:
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already existed.')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already existed.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Register successfully.')
                    return redirect('login')
            else:
                messages.info(request, 'Passwords donot match')
                return redirect('register')
    else:
        return render(request, 'index.html', {'product_types': product_types, 'products_with_images': products_with_images, 'blogs': blogs, 'cart': cart, 'is_staff': user.is_staff})

def register(request):
    nextUrl = request.POST.get('next')
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                if nextUrl != '' and nextUrl is not None:
                    return redirect(nextUrl)
                else:
                    return redirect('/')
        else:
            messages.info(request, 'Password doesn\'t match')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        # nextUrl = request.POST.get('next')
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Login successfully! Welcome back, {username}.")
            return redirect("/")
            # return redirect(nextUrl)
        else:
            messages.info(request, 'Invalid username or password.')
            return redirect('login')
        
    else: 
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def updateprofile(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        
        # Update profile information
        if phoneNumber != '':
            user_profile.phone = phoneNumber
        if address != '':
            user_profile.address = address
            
        user_profile.last_updated = datetime.now()
        user_profile.save()
        
        if password != '' and password2 != '':
            if password == password2:
                user.set_password(password)
                user.save()
                
                messages.info(request, 'Please login')
                return redirect('/login')
            else:
                messages.error(request, 'Password doesn\'t match')
        
        messages.success(request, 'Update successfully')
        return redirect("/profile")
    else:
        return render(request, 'profile.html', {'user_profile': user_profile, 'cart': cart})

def addproduct(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    
    if user and user.is_superuser:
        unique_names = Product_Types.objects.values_list('name', flat=True).distinct()

        if request.method == 'POST':
            product = Products()
            product.name = request.POST.get('name')
            product_type_name = request.POST.get('typeProduct')

            # Get or create Product_Type
            product_type, created = Product_Types.objects.get_or_create(name=product_type_name)
            product.product_type_id = product_type

            product.price = request.POST.get('price')
            product.pricesale = request.POST.get('pricesale', '')
            product.description = request.POST.get('description')
            product.save()

            # Process uploaded image
            if 'image' in request.FILES:
                image = request.FILES['image']
                product_image = Product_Images(product=product, url=image)
                product_image.save()

            messages.success(request, "Add Product Successfully")
            return redirect("/addproduct")

        return render(request, 'addproduct.html', {'unique_names': unique_names, 'cart': cart})
    else:
        messages.info(request, "You don't have permission to access this page.")
        return redirect("/")
    
def editproduct(request, slug):
    user = request.user
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    
    if user and user.is_superuser:
        if request.method == 'POST':
            newName = request.POST.get('name', '')
            newTypeProduct = request.POST.get('typeProduct', '')
            newPrice = request.POST.get('price', '')
            newPriceSale = request.POST.get('pricesale', '')
            newDescription = request.POST.get('description', '')
            setNewest = request.POST.get('setToNewest', '')
            
            product = Products.objects.get(product_id=slug)
            
            if newName != '':
                product.name = newName
            if newTypeProduct != '':
                # Assuming product type is a foreign key in Products model
                product.typeProduct.name = newTypeProduct
                product.typeProduct.save()
            if newPrice != '':
                product.price = newPrice
            if newPriceSale != '':
                product.pricesale = newPriceSale
            if newDescription != '':
                product.description = newDescription
            if setNewest == 'on':
                product.created_at = datetime.now()
            product.last_updated = datetime.now()

            # Process uploaded image
            if 'image' in request.FILES:
                # Delete existing product images
                product.product_images.all().delete()
                
                # Save the new image
                image = request.FILES['image']
                product_image = Product_Images(product=product, url=image)
                product_image.save()
            
            try:
                product.save()
                messages.success(request, "Update Product Successfully")
                return redirect("/")
            except Exception as e:
                messages.error(request, f"Failed to update product: {str(e)}")
                return redirect("editproduct", slug=slug)

        else:
            product = Products.objects.get(product_id=slug)
            images = Product_Images.objects.filter(product=product)
            product.images = images
            return render(request, 'editproduct.html', {'product': product, 'cart': cart})
    else:
        messages.info(request, "You don't have permission to access this page.")
        return redirect("/")
    
def deleteproduct(request, slug):
    product = Products.objects.get(product_id=slug)
    user = request.user
    
    if user and user.is_superuser:
        try:
            product.delete()
            messages.success(request, "Delete Product Successfully")
            return redirect("/")
        except Exception as e:
            messages.error(request, f"Failed to delete product: {str(e)}")
            return redirect("/")
    else:
        messages.info(request, "You don't have permission to access this page.")
        return redirect("/")

def products(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    product_types = Product_Types.objects.all()
    products_with_images = getProductOrderedType() 
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    return render(request, 'products.html', {'product_types': product_types, 'products_with_images': products_with_images, 'blogs': blogs, 'cart': cart, 'is_staff': user.is_staff})
    
def productDetails(request, slug):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    product = Products.objects.get(product_id=slug)
    product_images = Product_Images.objects.filter(product=product)
    print(product_images)
    return render(request, 'productDetails.html', {'product': product, 'product_images': product_images, 'cart': cart})

def cart(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    return render(request, 'cart.html', {'cart': cart, 'blogs': blogs})

def orderHistory(request):
    return render(request, 'orderHistory.html', {})

def orderDetails(request):
    return render(request, 'orderDetails.html', {})

def payment(request):
    return render(request, 'payment.html', {})


def loading(request):
    return render(request, 'loading.html', {})

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

def handler404(request, exception):
    return render(request, '404.html', status=404)

# _____________________API_________________________

# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import Products, Product_Types
from .serializers import ProductTypeSerializer, ProductSerializer, ProductWithTypeSerializer, ProductImageSerializer

class ProductWithTypeAPIView(generics.ListAPIView):
    serializer_class = ProductWithTypeSerializer

    def get_queryset(self):
        product_types = Product_Types.objects.all()
        data = []

        for product_type in product_types:
            products = Products.objects.filter(product_type_id=product_type.product_type_id)
            serialized_products = ProductSerializer(products, many=True).data

            data.append({
                'type': ProductTypeSerializer(product_type).data,
                'products': serialized_products
            })

        return data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Loop through each product and add images
        for product_data in serializer.data:
            products = product_data['products']
            for product in products:
                product_obj = Products.objects.get(product_id=product['product_id'])
                images_serializer = ProductImageSerializer(product_obj.product_images.all(), many=True)
                product['images'] = images_serializer.data

        return Response(serializer.data)

