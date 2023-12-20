from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import Blogs
from .forms import BlogPostForm
from products.models import Users

# Create your views here.
def writeblog(request):
    if request.method == 'POST':
        try:
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Add Blog Successfully")
                return redirect("/writeblog")
        except MultiValueDictKeyError:
            messages.error(request, f"Failed to add blog: {str(e)}")
            pass
    else:
        form = BlogPostForm()
    context = {
        'form': form
    }
    return render(request, 'writeblog.html', context)
# def writeblog(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'writeblog.html')
#             # return HttpResponse('New Blog Successfully Added')
#     else:
#         form = BlogPostForm()
#         context = {
#             'form':form
#         }
#     return render(request, 'writeblog.html', {'form':form})
    # if request.method == 'POST':
    #     blog = Blog()
    #     blog.title = request.POST.get('title')
    #     blog.content = request.POST.get('content')
        
    #     if len(request.FILES) != 0:
    #         blog.image = request.FILES['image']
        
    #     try:
    #         blog.save()
    #         messages.success(request, "Add Blog Successfully")
    #         return redirect("/")
    #     except Exception as e:
    #         messages.error(request, f"Failed to create blog: {str(e)}")
            # return redirect("writeblog.html")
    # else:
        # return render(request, 'writeblog.html')
  
    
def editblog(request, slug):
    if request.method == 'POST':
        newTitle = request.POST.get('title', '')
        newContent = request.POST.get('content', '')
        setNewest = request.POST.get('setToNewest', '')
        
        blog = Blogs.objects.get(id=slug)
        if newTitle != '':
            blog.title = newTitle
        if newContent != '':
            blog.content = newContent
        if len(request.FILES) != 0:
            blog.image = request.FILES['image']
        if setNewest == 'on':
            blog.createdAt = datetime.now()

        try:
            blog.save()
            messages.success(request, "Update Blog Successfully")
            return redirect("/")
        except Exception as e:
            messages.error(request, f"Error updating blog: {str(e)}")
            return redirect("editblog", slug=slug)
    else:
        blog = Blogs.objects.get(id=slug)
        return render(request, 'editblog.html', {'blog': blog})

def deleteblog(request, slug):
    blog = Blogs.objects.get(id=slug)
    
    try:
        blog.delete()
        messages.success(request, "Delete Blog Successfully")
        return redirect("/")
    except Exception as e:
        messages.error(request, f"Failed to delete blog: {str(e)}")
        return redirect("/")

  
    
def blogs(request):
    blogs = Blogs.objects.all().order_by('-createdAt')
    return render(request, 'blogs.html', {'blogs': blogs})
    
def blogDetails(request, slug):
    blog = Blogs.objects.get(id=slug)
    blogs = Blogs.objects.all().order_by('-createdAt')[:6]
    return render(request, 'blogDetails.html', {'blog': blog, 'blogs': blogs})

def aboutUs(request):
    blogs = Blogs.objects.all().order_by('-createdAt')
    return render(request, 'aboutUs.html', {'blogs': blogs})

def contact(request):
    blogs = Blogs.objects.all().order_by('-createdAt')
    return render(request, 'contact.html', {'blogs': blogs})

def profile(request):
    user = request.user
    user_profile, created = Users.objects.get_or_create(user=user)
    return render(request, 'profile.html', {'user_profile': user_profile})
