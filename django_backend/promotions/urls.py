from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    
    # Coupons
    path('coupons/', views.coupons_page, name='coupons'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
]
