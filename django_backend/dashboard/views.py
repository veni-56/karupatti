from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import seller_required, admin_required


@login_required
def buyer_dashboard_view(request):
    """Buyer dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/buyer_dashboard.html', context)


@login_required
@seller_required
def seller_dashboard_view(request):
    """Seller dashboard with shop statistics"""
    shop = getattr(request.user, 'shop', None)
    
    context = {
        'user': request.user,
        'shop': shop,
    }
    
    if shop:
        # Get shop statistics
        from store.models import Product
        from payments.models import Earning, SellerWallet
        
        products = Product.objects.filter(shop=shop)
        total_products = products.count()
        active_products = products.filter(is_active=True).count()
        
        # Get wallet information
        wallet, created = SellerWallet.objects.get_or_create(seller=request.user)
        
        # Get recent earnings
        recent_earnings = Earning.objects.filter(shop=shop).order_by('-created_at')[:10]
        
        context.update({
            'total_products': total_products,
            'active_products': active_products,
            'wallet': wallet,
            'recent_earnings': recent_earnings,
        })
    
    return render(request, 'dashboard/seller_dashboard.html', context)


@login_required
@admin_required
def admin_dashboard_view(request):
    """Admin dashboard with platform statistics"""
    from accounts.models import CustomUser
    from shops.models import Shop
    from store.models import Product
    from payments.models import Payment
    
    # Get statistics
    total_users = CustomUser.objects.count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_sellers = CustomUser.objects.filter(role='seller').count()
    total_shops = Shop.objects.count()
    verified_shops = Shop.objects.filter(is_verified=True).count()
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    # Get recent activity
    recent_users = CustomUser.objects.order_by('-date_joined')[:10]
    recent_shops = Shop.objects.order_by('-created_at')[:10]
    recent_products = Product.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_buyers': total_buyers,
        'total_sellers': total_sellers,
        'total_shops': total_shops,
        'verified_shops': verified_shops,
        'total_products': total_products,
        'active_products': active_products,
        'recent_users': recent_users,
        'recent_shops': recent_shops,
        'recent_products': recent_products,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
