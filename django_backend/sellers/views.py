from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from accounts.decorators import seller_required
from store.models import Product, ProductImage, Category
from orders.models import Order, OrderItem
from payments.models import SellerWallet, Earning
from .forms import ProductForm, ProductImageForm


@login_required
@seller_required
def seller_dashboard(request):
    """Seller dashboard with analytics"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first to access the seller dashboard.')
        return redirect('shops:create_shop')
    
    shop = request.user.shop
    
    # Get wallet
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    
    # Get products
    products = Product.objects.filter(shop=shop)
    total_products = products.count()
    active_products = products.filter(is_active=True).count()
    out_of_stock = products.filter(stock=0).count()
    
    # Get orders
    order_items = OrderItem.objects.filter(shop=shop)
    total_orders = order_items.values('order').distinct().count()
    
    # Recent orders
    recent_orders = order_items.select_related('order', 'product').order_by('-created_at')[:10]
    
    # Earnings this month
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_earnings = Earning.objects.filter(
        seller=request.user,
        created_at__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'shop': shop,
        'wallet': wallet,
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'month_earnings': month_earnings,
    }
    return render(request, 'sellers/dashboard.html', context)


@login_required
@seller_required
def product_list(request):
    """List seller's products"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    shop = request.user.shop
    products = Product.objects.filter(shop=shop)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status = request.GET.get('status', '')
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    elif status == 'out_of_stock':
        products = products.filter(stock=0)
    
    context = {
        'products': products,
        'search_query': search_query,
        'status': status,
    }
    return render(request, 'sellers/product_list.html', context)


@login_required
@seller_required
def product_create(request):
    """Create a new product"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    shop = request.user.shop
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('sellers:product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    return render(request, 'sellers/product_form.html', context)


@login_required
@seller_required
def product_update(request, slug):
    """Update a product"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    product = get_object_or_404(Product, slug=slug, shop=request.user.shop)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('sellers:product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'action': 'Update',
        'product': product,
    }
    return render(request, 'sellers/product_form.html', context)


@login_required
@seller_required
def product_delete(request, slug):
    """Delete a product"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    product = get_object_or_404(Product, slug=slug, shop=request.user.shop)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('sellers:product_list')
    
    context = {
        'product': product,
    }
    return render(request, 'sellers/product_confirm_delete.html', context)


@login_required
@seller_required
def product_images(request, slug):
    """Manage product images"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    product = get_object_or_404(Product, slug=slug, shop=request.user.shop)
    images = product.images.all()
    
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()
            messages.success(request, 'Image added successfully!')
            return redirect('sellers:product_images', slug=slug)
    else:
        form = ProductImageForm()
    
    context = {
        'product': product,
        'images': images,
        'form': form,
    }
    return render(request, 'sellers/product_images.html', context)


@login_required
@seller_required
def delete_product_image(request, image_id):
    """Delete a product image"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    image = get_object_or_404(ProductImage, id=image_id, product__shop=request.user.shop)
    slug = image.product.slug
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    
    return redirect('sellers:product_images', slug=slug)


@login_required
@seller_required
def order_list(request):
    """List seller's orders"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    shop = request.user.shop
    order_items = OrderItem.objects.filter(shop=shop).select_related('order', 'product').order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        order_items = order_items.filter(order__status=status)
    
    context = {
        'order_items': order_items,
        'status': status,
    }
    return render(request, 'sellers/order_list.html', context)


@login_required
@seller_required
def order_detail(request, order_number):
    """View order details"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    order = get_object_or_404(Order, order_number=order_number)
    
    # Check if seller has items in this order
    order_items = order.items.filter(shop=request.user.shop)
    if not order_items.exists():
        messages.error(request, 'You do not have access to this order.')
        return redirect('sellers:order_list')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'sellers/order_detail.html', context)


@login_required
@seller_required
def earnings(request):
    """View earnings and wallet"""
    if not hasattr(request.user, 'shop'):
        messages.info(request, 'Please create your shop first.')
        return redirect('shops:create_shop')
    
    wallet, _ = SellerWallet.objects.get_or_create(seller=request.user)
    earnings_list = Earning.objects.filter(seller=request.user).order_by('-created_at')
    
    # Monthly earnings
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_earnings = earnings_list.filter(created_at__gte=month_start).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'wallet': wallet,
        'earnings': earnings_list[:50],
        'month_earnings': month_earnings,
    }
    return render(request, 'sellers/earnings.html', context)
