from django.urls import path
from .views import (
    CartListCreateView, CartDetailView,
    CartDetailListCreateView, CartDetailDetailView,
    OrderListCreateView, OrderDetailView,
    OrderDetailListCreateView, OrderDetailDetailView
)
from . import views

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('carts/', CartListCreateView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),

    path('cart-details/', CartDetailListCreateView.as_view(), name='cart-detail-list-create'),
    path('cart-details/<int:pk>/', CartDetailDetailView.as_view(), name='cart-detail-detail'),

    path('create-order/', views.create_order, name='create-order'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('order-details/', OrderDetailListCreateView.as_view(), name='order-detail-list-create'),
    path('order-details/<int:pk>/', OrderDetailDetailView.as_view(), name='order-detail-detail'),
    path('update-cart-item-quantity/<int:cart_detail_id>/', views.update_cart_item_quantity, name='update-cart-item-quantity'),
    path('delete-cart-item/<int:cart_detail_id>/', views.delete_cart_item, name='delete-cart-item'),
    
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('payment-status/', views.payment_status, name='payment_status'),
    path('process-payment/', views.process_payment, name='process_payment'),
]
