from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Blogs
from .forms import BlogPostForm
from products.models import Users, Products, Product_Types, Product_Images
from order.models import Carts, Cart_Details, Orders, Order_Details
from products.views import getProductOrderedType

# Create your views here.
def writeblog(request):
    user = request.user
    if user and user.is_superuser:
        if request.method == 'POST':
            try:
                form = BlogPostForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Thêm blog thành công")
                    return redirect("/writeblog")
            except MultiValueDictKeyError:
                messages.error(request, f"Thêm blog thất bại: {str(e)}")
                pass
        else:
            form = BlogPostForm()
        context = {
            'form': form
        }
        return render(request, 'writeblog.html', context)
    else:
        messages.info(request, "Bạn không có quyền truy cập trang này.")
        return redirect("/")
    
def editblog(request, slug):
    user = request.user
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    
    if user and user.is_superuser:
        blog = Blogs.objects.get(id=slug)
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                setNewest = request.POST.get('setToNewest', '')
                if setNewest == 'on':
                    blog.created_at = datetime.now()
                    
                blog.last_updated = datetime.now()
                form.save()
                messages.success(request, "Cập nhật blog thành công")
                return redirect("/")
            else:
                messages.error(request, "Lỗi cập nhật blog. Vui lòng kiểm tra lại thông tin.")
        else:
            form = BlogPostForm(instance=blog)
        return render(request, 'editblog.html', {'form': form, 'blog': blog, 'cart': cart})
    else:
        messages.info(request, "Bạn không có quyền truy cập trang này.")
        return redirect("/")

def deleteblog(request, slug):
    user = request.user
    
    if user and user.is_superuser:
        blog = Blogs.objects.get(id=slug)
        
        try:
            blog.delete()
            messages.success(request, "Xóa blog thành công")
            return redirect("/")
        except Exception as e:
            messages.error(request, f"Lỗi xóa blog: {str(e)}")
            return redirect("/")
    else:
        messages.info(request, "Bạn không có quyền truy cập trang này.")
        return redirect("/")

  
    
def blogs(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
    blogs = Blogs.objects.all().order_by('-created_at')
    return render(request, 'blogs.html', {'blogs': blogs, 'cart': cart})
    
def blogDetails(request, slug):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    blog = Blogs.objects.get(id=slug)
    blogs = Blogs.objects.all().order_by('-created_at')[:6]
    return render(request, 'blogDetails.html', {'blog': blog, 'blogs': blogs, 'cart': cart})

def aboutUs(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    product_types = Product_Types.objects.all()
    products_with_images = getProductOrderedType(8) 
    blogs = Blogs.objects.all().order_by('-created_at')
    return render(request, 'aboutUs.html', {'product_types': product_types, 'products_with_images': products_with_images, 'blogs': blogs, 'cart': cart})

def contact(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    blogs = Blogs.objects.all().order_by('-created_at')
    return render(request, 'contact.html', {'blogs': blogs, 'cart': cart})

def profile(request):
    user = request.user  # Đây là user đăng nhập, nếu có
    cart = None
    if user.is_authenticated:
        user_profile, created = Users.objects.get_or_create(user=user)
        cart, created = Carts.objects.get_or_create(user=user_profile)
        
    return render(request, 'profile.html', {'user_profile': user_profile, 'cart': cart})
