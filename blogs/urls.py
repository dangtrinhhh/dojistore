from django.urls import path, include
from . import views

urlpatterns = [
    path('writeblog', views.writeblog, name='writeblog'),
    path('blogs', views.blogs, name='blogs'),
    path('blogs/<str:slug>', views.blogDetails, name='blogDetails'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('contact', views.contact, name='contact'),
]