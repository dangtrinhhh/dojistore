from django.urls import path, include
from . import views
from .views import CustomPasswordResetView
from django.conf.urls import handler404
from .views import page_not_found_view
from django.conf.urls import handler500
from .views import server_error_view
from django.shortcuts import render
from django.urls import re_path
from .views import ProductWithTypeAPIView, ProductSearchView


# trong urls.py
from django.urls import path
from .views import handler404

handler404 = handler404  # Tạo biến global cho view

# Thêm đoạn code sau vào urlpatterns
# handler404 = handler404  # Sử dụng view tùy chỉnh cho lỗi 404

# handler500 = server_error_view
# handler404 = page_not_found_view

# def handler404(request, exception, template_name='404.html'):
#     response = render(request, template_name)
#     response.status_code = 404
#     return response

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
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('loading', views.loading, name='loading'),
    path('cart', views.cart, name='cart'),
    path('orders/list', views.orders, name='orders'),
    path('order/history', views.orderHistory, name='orderHistory'),
    path('order/details/<str:slug>', views.orderDetails, name='orderDetails'),
    path('order/payment', views.payment, name='payment'),
    path('order/payment/success/', views.paymentSuccess, name='paymentSuccess'),
    path('order/payment/failed/', views.paymentFailed, name='paymentFailed'),
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/', include('allauth.urls')),
    path('handler404/', handler404),
    path('404', views.notFound, name='notFound'),

    # path('accounts/reset/fail', CustomPasswordResetView.as_view(), name='password_reset'),
    
    # ____________________________________API_____________________________________
    path('api/product-with-type/', ProductWithTypeAPIView.as_view(), name='api-product-with-type'),
    path('api/products/search/', ProductSearchView.as_view(), name='api-product-search'),
]

# handler404 = handler404
# handler404 = re_path(r'^.*$', handler404)