from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Blog

# Create your views here.
def writeblog(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        
        if len(request.FILES) != 0:
            blog.image = request.FILES['image']
        
        blog.save()
        messages.success(request, "Add Blog Successfully")
        return redirect("/")
    else:
        return render(request, 'writeblog.html')
    
def blogs(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'blogs.html', {'blogs': blogs})
    
def blogDetails(request, slug):
    blog = Blog.objects.get(id=slug)
    return render(request, 'blogDetails.html', {'blog': blog})

def aboutUs(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'aboutUs.html', {'blogs': blogs})

def contact(request):
    blogs = Blog.objects.all().order_by('-createdAt')
    return render(request, 'contact.html', {'blogs': blogs})
