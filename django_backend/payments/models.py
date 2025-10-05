from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    order_id = models.CharField(max_length=64, db_index=True)  # reference to store.Order id or code
    stripe_session_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="usd")
    status = models.CharField(max_length=32, default="created")  # created | paid | failed | refunded
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.order_id} - {self.status}"

class SellerWallet(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet({self.seller}) balance={self.balance}"

class Earning(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="earnings")
    order_id = models.CharField(max_length=64, db_index=True)
    order_item_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # seller amount after fee
    platform_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Earning seller={self.seller_id} order={self.order_id} amount={self.amount}"

class PayoutRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("paid", "Paid"),
        ("rejected", "Rejected"),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payout_requests")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=32, default="manual")  # manual | stripe

    def __str__(self):
        return f"PayoutRequest({self.seller_id}, {self.amount}, {self.status})"
