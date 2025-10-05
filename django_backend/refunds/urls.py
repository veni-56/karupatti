from django.urls import path
from . import views

app_name = 'refunds'

urlpatterns = [
    path('', views.refund_request_list, name='refund_request_list'),
    path('<str:request_number>/', views.refund_request_detail, name='refund_request_detail'),
    path('create/<str:order_number>/', views.create_refund_request, name='create_refund_request'),
    path('<str:request_number>/cancel/', views.cancel_refund_request, name='cancel_refund_request'),
    path('store-credit/balance/', views.store_credit_balance, name='store_credit_balance'),
]
