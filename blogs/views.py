from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Blog

# Create your views here.
def writeblog(request):
    if request.method == 'POST':
        product = Blog()
        product.name = request.POST.get('name')
        product.typeProduct = request.POST.get('typeProduct')
        product.description = request.POST.get('description')
        
        if len(request.FILES) != 0:
            product.image = request.FILES['image']
        
        product.save()
        messages.success(request, "Add Product Successfully")
        return redirect("/")
    else:
        return render(request, 'writeblog.html')
    
def blogs(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'blogs.html', {'blogs': blogs})
    
def blogDetails(request, slug):
    blog = Blog.objects.get(title=slug)
    return render(request, 'blogDetails.html', {'blog': blog})

def aboutUs(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'aboutUs.html', {'blogs': blogs})

def contact(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'contact.html', {'blogs': blogs})
