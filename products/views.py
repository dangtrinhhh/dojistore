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

def getProductOrderedType():
    unique_names = Product_Types.objects.values_list('name', flat=True).distinct()
    for name in unique_names:
        products_for_type = Products.objects.filter(product_type_id__name=name)
        yield products_for_type

# Create your views here.
def index(request):
    products_for_type = getProductOrderedType()
    # To get Products from database:
    # Products.objects.get() can only return 1 product
    # fruits = Products.objects.filter(typeProduct__iexact='fruit').order_by('-created_at')[:8]
    # vegetables = Products.objects.filter(typeProduct__iexact='vegetable').order_by('-created_at')[:8]
    # others = Products.objects.filter(typeProduct__iexact='other').order_by('-created_at')[:8]
    # __icontain: get element contain keyword
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    
    if request.method == "POST":
        # user = request.user
        # user_profile, created = Users.objects.get_or_create(user=user)
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
        # , 'user_profile': user_profile
        return render(request, 'index.html', {'products_for_type': products_for_type, 'blogs': blogs})

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

def updatepassword(request):
    user = request.user
    user_profile, created = Users.objects.get_or_create(user=user)
    
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
                return render(request, 'profile.html')
        
        messages.success(request, 'Update successfully')
    else:
        return render(request, 'profile.html', {'user_profile': user_profile})

def addproduct(request):
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

    return render(request, 'addproduct.html', {'unique_names': unique_names})
    
def editproduct(request, slug):
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
            product.created_at = datetime.now()
        product.last_updated = datetime.now()
        
        try:
            product.save()
            messages.success(request, "Update Product Successfully")
            return redirect("/")
        except Exception as e:
            messages.error(request, f"Failed to update product: {str(e)}")
            return redirect("editproduct", slug=slug)

    else:
        product = Products.objects.get(product_id=slug)
        return render(request, 'editproduct.html', {'product': product})

def deleteproduct(request, slug):
    product = Products.objects.get(product_id=slug)
    
    try:
        product.delete()
        messages.success(request, "Delete Product Successfully")
        return redirect("/")
    except Exception as e:
        messages.error(request, f"Failed to delete product: {str(e)}")
        return redirect("/")

def products(request):
    
    # fruits = Products.objects.filter(typeProduct__iexact='fruit').order_by('-created_at')
    # vegetables = Products.objects.filter(typeProduct__iexact='vegetable').order_by('-created_at')
    # others = Products.objects.filter(typeProduct__iexact='other').order_by('-created_at')
    products_for_type = getProductOrderedType()
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    return render(request, 'products.html', {'products_for_type': products_for_type, 'blogs': blogs})
    
def productDetails(request, slug):
    product = Products.objects.get(product_id=slug)
    return render(request, 'productDetails.html', {'product': product})

def cart(request):
    return render(request, 'cart.html', {})

def page_not_found(request, exception):
    return render(request, '404.html', status=404)