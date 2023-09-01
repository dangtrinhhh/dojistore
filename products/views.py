from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Product
from blogs.models import Blog

# Create your views here.
def index(request):
    # To get Products from database:
    # Product.objects.get() can only return 1 product
    fruits = Product.objects.filter(typeProduct__iexact='fruit').order_by('-createdAt')
    vegetables = Product.objects.filter(typeProduct__iexact='vegetable').order_by('-createdAt')
    others = Product.objects.exclude(typeProduct__iexact='other').order_by('-createdAt')
    # __icontain: get element contain keyword
    blogs = Blog.objects.all().order_by('-createdAt')
    
    if request.method == "POST":
        email = request.POST.get('email', '')
        if email == '':
            username = request.POST['username']
            password = request.POST['password']
            
            user = auth.authenticate(username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Tên tài khoản hoặc mật khẩu không đúng.')
                return redirect('/login')
        else:
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email đã tồn tại.')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Tên đăng nhập đã tồn tại.')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('login')
            else:
                messages.info(request, 'Mật khẩu không khớp')
                return redirect('register')
    else:
        return render(request, 'index.html', {'fruits': fruits, 'vegetables': vegetables, 'others': others, 'blogs': blogs})

def register(request):
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
                return redirect('login')
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
        
        if user is not None:
            auth.login(request, user)
            return redirect( '/' )
        else:
            messages.info(request, 'Tên tài khoản hoặc mật khẩu không đúng.')
            return redirect('login')
        
    else: 
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect( '/' )

def addproduct(request):
    if request.method == 'POST':
        product = Product()
        product.name = request.POST.get('name')
        product.typeProduct = request.POST.get('typeProduct')
        product.price = request.POST.get('price')
        product.pricesale = request.POST.get('pricesale', '')
        product.description = request.POST.get('description')
        
        if len(request.FILES) != 0:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, "Add Product Successfully")
        return redirect("/")
    else:
        return render(request, 'addproduct.html')
    
def products(request):
    fruits = Product.objects.filter(typeProduct__iexact='fruit').order_by('-createdAt')
    vegetables = Product.objects.filter(typeProduct__iexact='vegetable').order_by('-createdAt')
    others = Product.objects.exclude(typeProduct__iexact='other').order_by('-createdAt')
    return render(request, 'products.html', {'fruits': fruits, 'vegetables': vegetables, 'others': others})
    
def productDetails(request, slug):
    product = Product.objects.get(id=slug)
    return render(request, 'productDetails.html', {'product': product})

def page_not_found(request, exception):
    return render(request, '404.html', status=404)