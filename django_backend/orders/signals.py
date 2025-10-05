from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderItem
from payments.models import SellerWallet, Earning


@receiver(post_save, sender=Order)
def handle_order_payment(sender, instance, created, **kwargs):
    """Handle order payment and distribute earnings"""
    if instance.payment_status == 'paid' and not created:
        # Check if earnings already distributed
        if not Earning.objects.filter(order_id=str(instance.id)).exists():
            # Distribute earnings to sellers
            for item in instance.items.all():
                if item.shop and item.shop.owner:
                    # Create earning record
                    Earning.objects.create(
                        seller=item.shop.owner,
                        order_id=str(instance.id),
                        order_item_id=str(item.id),
                        amount=item.seller_amount,
                        platform_fee=item.platform_fee
                    )
                    
                    # Update seller wallet
                    wallet, _ = SellerWallet.objects.get_or_create(seller=item.shop.owner)
                    wallet.balance += item.seller_amount
                    wallet.total_earned += item.seller_amount
                    wallet.save()
