from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from decimal import Decimal
from .models import Order, OrderItem
from accounts.models import Address
from store.models import Product
from promotions.models import Coupon, CouponUsage
import json


@login_required
def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')
    
    # Calculate cart totals
    cart_items = []
    subtotal = Decimal('0')
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            if isinstance(item_data, dict):
                quantity = item_data.get('qty', 1)
            else:
                quantity = item_data  # item_data is already an int
            
            item_total = product.price * quantity
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            subtotal += item_total
        except Product.DoesNotExist:
            continue
    
    # Calculate totals
    shipping_cost = Decimal('10.00')
    tax = subtotal * Decimal('0.08')
    
    discount = Decimal('0')
    applied_coupon = request.session.get('applied_coupon')
    if applied_coupon:
        discount = Decimal(str(applied_coupon.get('discount', '0')))
    
    total = subtotal + shipping_cost + tax - discount
    
    # Get user addresses
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'discount': discount,
        'total': total,
        'addresses': addresses,
        'default_address': default_address,
        'applied_coupon': applied_coupon,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def create_order(request):
    """Create order from cart"""
    if request.method != 'POST':
        return redirect('orders:checkout')
    
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('store:product_list')
    
    # Get form data
    payment_method = request.POST.get('payment_method')
    address_id = request.POST.get('address_id')
    
    if not payment_method or not address_id:
        messages.error(request, 'Please select payment method and shipping address.')
        return redirect('orders:checkout')
    
    # Get address
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Calculate totals
    subtotal = Decimal('0')
    cart_items = []
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            if isinstance(item_data, dict):
                quantity = item_data.get('qty', 1)
            else:
                quantity = item_data  # item_data is already an int
            
            item_total = product.price * quantity
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            subtotal += item_total
        except Product.DoesNotExist:
            continue
    
    shipping_cost = Decimal('10.00')
    tax = subtotal * Decimal('0.08')
    
    discount = Decimal('0')
    applied_coupon = request.session.get('applied_coupon')
    coupon_code = None
    
    if applied_coupon:
        discount = Decimal(str(applied_coupon.get('discount', '0')))
        coupon_code = applied_coupon.get('code')
    
    total = subtotal + shipping_cost + tax - discount
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        shipping_address=address,
        shipping_full_name=address.full_name,
        shipping_phone=address.phone,
        shipping_street=address.street_address,
        shipping_city=address.city,
        shipping_state=address.state,
        shipping_country=address.country,
        shipping_postal_code=address.postal_code,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax=tax,
        discount=discount,
        total_amount=total,
        payment_method=payment_method,
    )
    
    # Create order items
    platform_fee_percent = Decimal('0.10')
    
    for item in cart_items:
        product = item['product']
        quantity = item['quantity']
        item_subtotal = item['total']
        
        platform_fee = item_subtotal * platform_fee_percent
        seller_amount = item_subtotal - platform_fee
        
        OrderItem.objects.create(
            order=order,
            product=product,
            shop=product.shop,
            product_name=product.name,
            product_price=product.price,
            quantity=quantity,
            subtotal=item_subtotal,
            seller_amount=seller_amount,
            platform_fee=platform_fee
        )
        
        # Update product stock
        product.stock -= quantity
        product.save()
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            CouponUsage.objects.create(
                coupon=coupon,
                user=request.user,
                order_number=order.order_number,
                discount_amount=discount
            )
            coupon.times_used += 1
            coupon.save()
            
            # Clear coupon from session
            del request.session['applied_coupon']
        except Coupon.DoesNotExist:
            pass
    
    # Handle payment method
    if payment_method == 'cod':
        order.status = 'processing'
        order.save()
        
        # Clear cart
        request.session['cart'] = {}
        messages.success(request, f'Order {order.order_number} placed successfully! Pay on delivery.')
        return redirect('orders:order_detail', order_number=order.order_number)
    
    elif payment_method == 'stripe':
        request.session['pending_order_id'] = order.id
        return redirect('orders:stripe_checkout', order_number=order.order_number)
    
    elif payment_method == 'paypal':
        request.session['pending_order_id'] = order.id
        return redirect('orders:paypal_checkout', order_number=order.order_number)
    
    return redirect('orders:order_detail', order_number=order.order_number)


@login_required
def order_list(request):
    """List user's orders"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    
    context = {
        'orders': orders
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_number):
    """Order detail page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def stripe_checkout(request, order_number):
    """Stripe checkout session"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_number=order_number)
    
    context = {
        'order': order,
        'stripe_publishable_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
    }
    return render(request, 'orders/stripe_checkout.html', context)


@login_required
def paypal_checkout(request, order_number):
    """PayPal checkout page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_number=order_number)
    
    context = {
        'order': order,
        'paypal_client_id': getattr(settings, 'PAYPAL_CLIENT_ID', ''),
    }
    return render(request, 'orders/paypal_checkout.html', context)


@login_required
def cancel_order(request, order_number):
    """Cancel an order"""
    if request.method == 'POST':
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        if order.status in ['pending', 'processing']:
            order.status = 'cancelled'
            order.save()
            
            # Restore product stock
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
            
            messages.success(request, f'Order {order_number} has been cancelled.')
        else:
            messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('orders:order_detail', order_number=order_number)
