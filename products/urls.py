from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('products/delete/<str:slug>', views.deleteproduct, name='deleteproduct'),   
    path('products/edit/<str:slug>', views.editproduct, name='editproduct'),   
    path('products', views.products, name='products'),
    path('products/<str:slug>', views.productDetails, name='productDetails'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]

