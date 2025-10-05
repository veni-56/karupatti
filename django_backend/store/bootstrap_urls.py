from django.urls import path
from . import bootstrap_views as views

app_name = "store_bootstrap"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products_list, name="products"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:pk>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
]
