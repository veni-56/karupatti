from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("api/products/", views.products_api, name="products_api"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("checkout/", views.checkout, name="checkout"),
]
