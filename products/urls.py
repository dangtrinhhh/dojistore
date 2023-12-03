from django.urls import path, include
from . import views
from .views import CustomPasswordResetView

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
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('updatepassword', views.updatepassword, name='updatepassword'),
    path('cart', views.cart, name='cart'),
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/', include('allauth.urls')),
    # path('accounts/reset/fail', CustomPasswordResetView.as_view(), name='password_reset'),
]

