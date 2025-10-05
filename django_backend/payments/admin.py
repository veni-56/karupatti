from django.contrib import admin
from .models import Payment, SellerWallet, Earning, PayoutRequest

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order_id", "amount", "currency", "status", "created_at")
    search_fields = ("order_id", "stripe_session_id", "status")

@admin.register(SellerWallet)
class SellerWalletAdmin(admin.ModelAdmin):
    list_display = ("seller", "balance", "total_earned", "total_withdrawn", "updated_at")
    search_fields = ("seller__username", "seller__email")

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ("seller", "order_id", "order_item_id", "amount", "platform_fee", "created_at")
    search_fields = ("seller__username", "order_id", "order_item_id")

@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    list_display = ("seller", "amount", "status", "method", "created_at", "processed_at")
    list_filter = ("status", "method")
    actions = ["mark_paid", "approve", "reject"]

    def mark_paid(self, request, queryset):
        from django.utils import timezone
        for payout in queryset.filter(status__in=["approved", "pending"]):
            payout.status = "paid"
            payout.processed_at = timezone.now()
            payout.save()
            # adjust wallet
            wallet, _ = SellerWallet.objects.get_or_create(seller=payout.seller)
            wallet.balance = wallet.balance - payout.amount
            wallet.total_withdrawn = wallet.total_withdrawn + payout.amount
            wallet.save()
    mark_paid.short_description = "Mark selected payouts as paid"

    def approve(self, request, queryset):
        queryset.update(status="approved")
    approve.short_description = "Approve selected payouts"

    def reject(self, request, queryset):
        queryset.update(status="rejected")
    reject.short_description = "Reject selected payouts"
