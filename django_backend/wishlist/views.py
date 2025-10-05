from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Wishlist, WishlistItem
from store.models import Product


@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product', 'product__shop', 'product__category')
    
    context = {
        'wishlist': wishlist,
        'items': items,
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    # Check if product already in wishlist
    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Added to wishlist',
            'item_count': wishlist.item_count
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist'))


@login_required
def remove_from_wishlist(request, item_id):
    """Remove item from wishlist"""
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    product_name = item.product.name
    item.delete()
    
    messages.success(request, f'{product_name} removed from your wishlist.')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        wishlist = Wishlist.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'message': 'Removed from wishlist',
            'item_count': wishlist.item_count
        })
    
    return redirect('wishlist:wishlist')


@login_required
def clear_wishlist(request):
    """Clear all items from wishlist"""
    if request.method == 'POST':
        wishlist = get_object_or_404(Wishlist, user=request.user)
        wishlist.items.all().delete()
        messages.success(request, 'Your wishlist has been cleared.')
    
    return redirect('wishlist:wishlist')
