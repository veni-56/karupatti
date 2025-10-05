from django.urls import path
from . import views

urlpatterns = [
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.checkout_success, name="success"),
    path("cancel/", views.checkout_cancel, name="cancel"),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
    path("seller/payouts/", views.seller_payouts, name="seller_payouts"),
    path("seller/payouts/request/", views.request_payout, name="request_payout"),
]
