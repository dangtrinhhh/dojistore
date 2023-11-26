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
    fruits = Product.objects.filter(typeProduct__iexact='fruit').order_by('-createdAt')[:8]
    vegetables = Product.objects.filter(typeProduct__iexact='vegetable').order_by('-createdAt')[:8]
    others = Product.objects.filter(typeProduct__iexact='other').order_by('-createdAt')[:8]
    # __icontain: get element contain keyword
    blogs = Blog.objects.all().order_by('-createdAt')[:6]
    
    if request.method == "POST":
        email = request.POST.get('email', '')
        if email == '':
            username = request.POST['username']
            password = request.POST['password']
            
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
        return render(request, 'index.html', {'fruits': fruits, 'vegetables': vegetables, 'others': others, 'blogs': blogs})

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
                return redirect(nextUrl)
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

def forgotpassword(request):
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
                return redirect('/login')
        else:
            messages.info(request, 'Password doesn\'t match')
    else:
        return redirect('/profile')

def updatepassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        user = request.user
        if password == password2:
            user.set_password(password)
            user.save()
            messages.success(request, 'Update password successfully')
            messages.info(request, 'Please login')
            return redirect('/login')
        else:
            messages.error(request, 'Password doesn\'t match')
            return render(request, 'profile.html')
    else:
        return render(request, 'profile.html')

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
        
        try:
            product.save()
            messages.success(request, "Add Product Successfully")
            return redirect("/addproduct")
        except Exception as e:
            messages.error(request, f"Failed to add product: {str(e)}")
            return redirect("/addproduct")
    else:
        return render(request, 'addproduct.html')
    
def editproduct(request, slug):
    if request.method == 'POST':
        newName = request.POST.get('name', '')
        newTypeProduct = request.POST.get('typeProduct', '')
        newPrice = request.POST.get('price', '')
        newPriceSale = request.POST.get('pricesale', '')
        newDescription = request.POST.get('description', '')
        setNewest = request.POST.get('setToNewest', '')
        
        product = Product.objects.get(id=slug)
        if newName != '':
            product.name = newName
        if newTypeProduct != '':
            product.typeProduct = newTypeProduct
        if newPrice != '':
            product.price = newPrice
        if newPriceSale != '':
            product.pricesale = newPriceSale
        if newDescription != '':
            product.description = newDescription
        if len(request.FILES) != 0:
            product.image = request.FILES['image']
        if setNewest == 'on':
            product.createdAt = datetime.now()
        
        try:
            product.save()
            messages.success(request, "Update Product Successfully")
            return redirect("/")
        except Exception as e:
            messages.error(request, f"Failed to update product: {str(e)}")
            return redirect("editproduct", slug=slug)

    else:
        product = Product.objects.get(id=slug)
        return render(request, 'editproduct.html', {'product': product})

def deleteproduct(request, slug):
    product = Product.objects.get(id=slug)
    try:
        product.delete()
        messages.success(request, "Delete Product Successfully")
        return redirect("/")
    except Exception as e:
        messages.error(request, f"Failed to delete product: {str(e)}")
        return redirect("/")

def products(request):
    fruits = Product.objects.filter(typeProduct__iexact='fruit').order_by('-createdAt')
    vegetables = Product.objects.filter(typeProduct__iexact='vegetable').order_by('-createdAt')
    others = Product.objects.filter(typeProduct__iexact='other').order_by('-createdAt')
    blogs = Blog.objects.all().order_by('-createdAt')[:6]
    return render(request, 'products.html', {'fruits': fruits, 'vegetables': vegetables, 'others': others, 'blogs': blogs})
    
def productDetails(request, slug):
    product = Product.objects.get(product_id=slug)
    return render(request, 'productDetails.html', {'product': product})

def cart(request):
    return render(request, 'cart.html', {})

def page_not_found(request, exception):
    return render(request, '404.html', status=404)