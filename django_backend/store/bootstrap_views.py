from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import Product  # assumes Product model exists; if not, I can add it
from decimal import Decimal

def _get_cart(session):
    cart = session.get("cart", {})
    # cart structure: { product_id: { "qty": int, "price": "str-decimal", "name": str } }
    return cart

def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True

def home(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by("-id")[:12]
    return render(request, "bootstrap_home.html", {"products": products, "page_title": "Karupatti Shop"})

def products_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by("-id")
    return render(request, "products_list.html", {"products": products, "page_title": "All Products - Karupatti Shop"})

def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product, "page_title": f"{product.name} - Karupatti Shop"})

@require_POST
def add_to_cart(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    qty = int(request.POST.get("qty", 1))
    cart = _get_cart(request.session)
    pid = str(product.pk)
    if pid not in cart:
        cart[pid] = {
            "qty": qty,
            "price": str(product.price),  # store as string to be JSON/session-safe
            "name": product.name,
        }
    else:
        cart[pid]["qty"] += qty
    _save_cart(request.session, cart)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "count": sum(item["qty"] for item in cart.values())})
    return redirect("store_bootstrap:cart")

def cart_view(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    items = []
    total = Decimal("0.00")
    for pid, info in cart.items():
        try:
            product = Product.objects.get(pk=int(pid))
        except Product.DoesNotExist:
            # prune missing products
            continue
        price = Decimal(info["price"])
        qty = int(info["qty"])
        line_total = price * qty
        total += line_total
        items.append({"product": product, "qty": qty, "price": price, "line_total": line_total})
    return render(request, "cart.html", {"items": items, "total": total, "page_title": "Your Cart - Karupatti Shop"})

@require_POST
def update_cart(request: HttpRequest, pk: int) -> HttpResponse:
    qty = max(0, int(request.POST.get("qty", 1)))
    cart = _get_cart(request.session)
    pid = str(pk)
    if pid in cart:
        if qty == 0:
            cart.pop(pid, None)
        else:
            cart[pid]["qty"] = qty
        _save_cart(request.session, cart)
    return redirect("store_bootstrap:cart")

def remove_from_cart(request: HttpRequest, pk: int) -> HttpResponse:
    cart = _get_cart(request.session)
    cart.pop(str(pk), None)
    _save_cart(request.session, cart)
    return redirect("store_bootstrap:cart")

def checkout_view(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request.session)
    if not cart:
        return redirect("store_bootstrap:home")
    if request.method == "POST":
        # TODO: integrate payment & order creation models if required
        request.session["cart"] = {}
        request.session.modified = True
        return render(request, "checkout_success.html", {"page_title": "Order Placed - Karupatti Shop"})
    # compute totals for display
    total = sum(Decimal(item["price"]) * int(item["qty"]) for item in cart.values())
    return render(request, "checkout.html", {"total": total, "page_title": "Checkout - Karupatti Shop"})
