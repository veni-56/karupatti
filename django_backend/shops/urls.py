from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('create/', views.create_shop_view, name='create_shop'),
    path('update/', views.update_shop_view, name='update_shop'),
    path('list/', views.shop_list_view, name='shop_list'),
    path('<slug:slug>/', views.shop_detail_view, name='shop_detail'),
]
