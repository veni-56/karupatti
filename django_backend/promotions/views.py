from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Event, Coupon, CouponUsage
from store.models import Product
from decimal import Decimal


def event_list(request):
    """List all active events"""
    now = timezone.now()
    ongoing_events = Event.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )
    upcoming_events = Event.objects.filter(
        is_active=True,
        start_date__gt=now
    )
    
    context = {
        'ongoing_events': ongoing_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'promotions/event_list.html', context)


def event_detail(request, slug):
    """Event detail page with discounted products"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    # Get products in this event
    products = event.products.filter(is_active=True)
    
    # Also get products from categories in this event
    category_products = Product.objects.filter(
        category__in=event.categories.all(),
        is_active=True
    ).exclude(id__in=products.values_list('id', flat=True))
    
    all_products = list(products) + list(category_products)
    
    # Calculate discounted prices
    for product in all_products:
        product.original_price = product.price
        product.discounted_price = event.get_discounted_price(product.price)
        product.savings = product.original_price - product.discounted_price
    
    context = {
        'event': event,
        'products': all_products,
    }
    return render(request, 'promotions/event_detail.html', context)


@login_required
def apply_coupon(request):
    """Apply coupon code to cart"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        
        if not coupon_code:
            return JsonResponse({'success': False, 'message': 'Please enter a coupon code'})
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code'})
        
        # Calculate cart total
        cart = request.session.get('cart', {})
        cart_total = Decimal('0')
        
        for product_id, item_data in cart.items():
            price = Decimal(str(item_data.get('price', '0')))
            qty = int(item_data.get('qty', 1))
            cart_total += price * qty
        
        # Check if coupon can be used
        can_use, message = coupon.can_use(request.user, cart_total)
        
        if not can_use:
            return JsonResponse({'success': False, 'message': message})
        
        # Calculate discount
        discount = coupon.calculate_discount(cart_total)
        
        # Store coupon in session
        request.session['applied_coupon'] = {
            'code': coupon.code,
            'discount': str(discount),
        }
        
        return JsonResponse({
            'success': True,
            'message': f'Coupon applied! You saved ${discount}',
            'discount': str(discount),
            'new_total': str(cart_total - discount)
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def remove_coupon(request):
    """Remove applied coupon"""
    if 'applied_coupon' in request.session:
        del request.session['applied_coupon']
        return JsonResponse({'success': True, 'message': 'Coupon removed'})
    return JsonResponse({'success': False, 'message': 'No coupon applied'})


def coupons_page(request):
    """Show available coupons"""
    now = timezone.now()
    coupons = Coupon.objects.filter(
        is_active=True,
        valid_from__lte=now,
        valid_until__gte=now
    )
    
    context = {
        'coupons': coupons,
    }
    return render(request, 'promotions/coupons.html', context)
