from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('buyer/', views.buyer_dashboard_view, name='buyer_dashboard'),
    path('seller/', views.seller_dashboard_view, name='seller_dashboard'),
    path('admin/', views.admin_dashboard_view, name='admin_dashboard'),
]
