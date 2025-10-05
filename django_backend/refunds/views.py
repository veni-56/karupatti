from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import RefundRequest, Refund, StoreCredit
from orders.models import Order, OrderItem
from decimal import Decimal


@login_required
def refund_request_list(request):
    """List user's refund requests"""
    refund_requests = RefundRequest.objects.filter(user=request.user).select_related('order', 'order_item')
    
    context = {
        'refund_requests': refund_requests,
    }
    return render(request, 'refunds/refund_request_list.html', context)


@login_required
def refund_request_detail(request, request_number):
    """View refund request details"""
    refund_request = get_object_or_404(RefundRequest, request_number=request_number, user=request.user)
    
    context = {
        'refund_request': refund_request,
    }
    return render(request, 'refunds/refund_request_detail.html', context)


@login_required
def create_refund_request(request, order_number):
    """Create a refund request for an order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Check if order is eligible for refund
    if order.status not in ['delivered', 'completed']:
        messages.error(request, 'This order is not eligible for refund yet.')
        return redirect('orders:order_detail', order_number=order_number)
    
    # Check if refund already exists
    if RefundRequest.objects.filter(order=order, status__in=['pending', 'approved', 'processing']).exists():
        messages.error(request, 'A refund request already exists for this order.')
        return redirect('orders:order_detail', order_number=order_number)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description')
        order_item_id = request.POST.get('order_item_id')
        image = request.FILES.get('image')
        
        if not reason or not description:
            messages.error(request, 'Please provide reason and description.')
            return redirect('refunds:create_refund_request', order_number=order_number)
        
        # Determine refund amount
        if order_item_id:
            order_item = get_object_or_404(OrderItem, id=order_item_id, order=order)
            refund_amount = order_item.subtotal
        else:
            order_item = None
            refund_amount = order.total_amount
        
        # Create refund request
        refund_request = RefundRequest.objects.create(
            order=order,
            order_item=order_item,
            user=request.user,
            reason=reason,
            description=description,
            images=image,
            refund_amount=refund_amount
        )
        
        messages.success(request, f'Refund request {refund_request.request_number} submitted successfully.')
        return redirect('refunds:refund_request_detail', request_number=refund_request.request_number)
    
    context = {
        'order': order,
    }
    return render(request, 'refunds/create_refund_request.html', context)


@login_required
def cancel_refund_request(request, request_number):
    """Cancel a refund request"""
    if request.method == 'POST':
        refund_request = get_object_or_404(RefundRequest, request_number=request_number, user=request.user)
        
        if refund_request.status == 'pending':
            refund_request.status = 'cancelled'
            refund_request.save()
            messages.success(request, 'Refund request cancelled.')
        else:
            messages.error(request, 'This refund request cannot be cancelled.')
    
    return redirect('refunds:refund_request_list')


@login_required
def store_credit_balance(request):
    """View store credit balance"""
    store_credit, created = StoreCredit.objects.get_or_create(user=request.user)
    transactions = store_credit.transactions.all()
    
    context = {
        'store_credit': store_credit,
        'transactions': transactions,
    }
    return render(request, 'refunds/store_credit.html', context)
