import json
import decimal
from decimal import Decimal
from typing import Dict, Any, List

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Payment, SellerWallet, Earning, PayoutRequest

# We expect store app to provide access to cart, order, and order items.
# If your store app differs, update the import paths here:
try:
    from store.models import Order, OrderItem, Product  # type: ignore
except Exception:
    Order = None
    OrderItem = None
    Product = None

def _get_cart_items_from_session(request) -> List[Dict[str, Any]]:
    """
    Return a list of items from session cart with keys:
    id, name, price, quantity, seller_id
    """
    cart = request.session.get("cart", {})
    items = []
    for pid, item in cart.items():
        # expected item: {'name': ..., 'price': '12.99', 'qty': 1, 'seller_id': user_id}
        items.append({
            "id": str(pid),
            "name": item.get("name", f"Product {pid}"),
            "price": Decimal(str(item.get("price", "0"))),
            "quantity": int(item.get("qty", 1)),
            "seller_id": item.get("seller_id"),
        })
    return items

@login_required
def create_checkout_session(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    items = _get_cart_items_from_session(request)
    if not items:
        return JsonResponse({"error": "Cart is empty"}, status=400)

    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []
    amount_total = Decimal("0")
    currency = "usd"
    for it in items:
        unit_amount = int((it["price"] * 100).quantize(Decimal("1")))
        line_items.append({
            "price_data": {
                "currency": currency,
                "product_data": {"name": it["name"]},
                "unit_amount": unit_amount,
            },
            "quantity": it["quantity"],
        })
        amount_total += (it["price"] * it["quantity"])

    success_url = f"{settings.SITE_URL}{reverse('payments:success')}"
    cancel_url = f"{settings.SITE_URL}{reverse('payments:cancel')}"

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": str(request.user.id),
            "cart_json": json.dumps(items, default=str),
        },
    )

    Payment.objects.create(
        order_id="pending",
        stripe_session_id=session.id,
        amount=amount_total,
        currency=currency,
        status="created",
    )

    return JsonResponse({"id": session.id, "publishableKey": settings.STRIPE_PUBLISHABLE_KEY})

def checkout_success(request):
    # Optional: clear session cart
    request.session["cart"] = {}
    return render(request, "payments/checkout_success.html")

def checkout_cancel(request):
    return render(request, "payments/checkout_cancel.html")

@csrf_exempt
def stripe_webhook(request):
    import stripe
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        try:
            payment = Payment.objects.get(stripe_session_id=session_id)
        except Payment.DoesNotExist:
            return HttpResponse(status=200)

        # Create/mark order as paid; if Order model exists, persist it
        cart_items = json.loads(session.get("metadata", {}).get("cart_json", "[]"))
        user_id = session.get("metadata", {}).get("user_id")

        # If your store has its own checkout/order creation, hook into it here.
        order_id = payment.order_id
        if Order is not None and order_id == "pending":
            # Create a minimal order if not already created
            order = Order.objects.create(user_id=user_id, total_amount=payment.amount, status="paid")
            order_id = str(order.pk)

        # Mark payment
        payment.status = "paid"
        payment.order_id = order_id
        payment.save()

        # Distribute earnings per item
        fee_percent = Decimal(str(getattr(settings, "PLATFORM_FEE_PERCENT", 10))) / Decimal("100")
        for it in cart_items:
            seller_id = it.get("seller_id")
            price = Decimal(str(it.get("price", "0")))
            qty = Decimal(str(it.get("quantity", 1)))
            gross = (price * qty).quantize(Decimal("0.01"))
            platform_fee = (gross * fee_percent).quantize(Decimal("0.01"))
            seller_amount = (gross - platform_fee).quantize(Decimal("0.01"))

            if seller_id:
                Earning.objects.create(
                    seller_id=seller_id,
                    order_id=order_id,
                    order_item_id=str(it.get("id")),
                    amount=seller_amount,
                    platform_fee=platform_fee,
                )
                wallet, _ = SellerWallet.objects.get_or_create(seller_id=seller_id)
                wallet.balance = (wallet.balance + seller_amount).quantize(Decimal("0.01"))
                wallet.total_earned = (wallet.total_earned + seller_amount).quantize(Decimal("0.01"))
                wallet.save()

    return HttpResponse(status=200)

@login_required
def seller_payouts(request):
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    payouts = PayoutRequest.objects.filter(seller=request.user).order_by("-created_at")
    return render(request, "payments/seller_payouts.html", {"wallet": wallet, "payouts": payouts})

@login_required
def request_payout(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    try:
        amount = Decimal(str(request.POST.get("amount", "0")))
    except decimal.InvalidOperation:
        return HttpResponseBadRequest("Invalid amount")
    if amount <= 0 or amount > wallet.balance:
        return HttpResponseForbidden("Insufficient balance")
    PayoutRequest.objects.create(seller=request.user, amount=amount, status="pending", method="manual")
    return redirect("payments:seller_payouts")
