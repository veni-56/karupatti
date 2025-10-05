from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<slug:slug>/edit/', views.product_update, name='product_update'),
    path('products/<slug:slug>/delete/', views.product_delete, name='product_delete'),
    path('products/<slug:slug>/images/', views.product_images, name='product_images'),
    path('images/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    
    # Earnings
    path('earnings/', views.earnings, name='earnings'),
]
