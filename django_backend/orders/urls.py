from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create/', views.create_order, name='create_order'),
    path('my-orders/', views.order_list, name='order_list'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
    path('<str:order_number>/cancel/', views.cancel_order, name='cancel_order'),
    path('<str:order_number>/stripe/', views.stripe_checkout, name='stripe_checkout'),
    path('<str:order_number>/paypal/', views.paypal_checkout, name='paypal_checkout'),
]
