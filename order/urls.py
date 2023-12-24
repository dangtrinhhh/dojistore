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

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('order-details/', OrderDetailListCreateView.as_view(), name='order-detail-list-create'),
    path('order-details/<int:pk>/', OrderDetailDetailView.as_view(), name='order-detail-detail'),
]
