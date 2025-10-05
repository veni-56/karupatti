from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category

BRAND = "Karupatti Shop"

def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    categories = Category.objects.filter(is_active=True, parent=None)[:6]
    
    context = {
        "brand": BRAND,
        "featured_products": featured_products,
        "categories": categories,
    }
    return render(request, "home.html", context)

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Price sorting
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    context = {
        "products": products,
        "categories": categories,
        "search_query": search_query,
        "category_slug": category_slug,
        "sort_by": sort_by,
    }
    return render(request, "products/product_list.html", context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "products/product_detail.html", context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "products/category_detail.html", context)

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")

def products_api(request):
    items = [
        {"id": 1, "name": "Karupatti (Palm Jaggery) 500g", "price": 6.50},
        {"id": 2, "name": "Karupatti Candy 250g", "price": 3.80},
        {"id": 3, "name": "Karupatti Syrup 300ml", "price": 5.20},
    ]
    return JsonResponse({"brand": BRAND, "products": items})

def cart(request):
    """Display the shopping cart"""
    cart_data = request.session.get('cart', {})
    items = []
    subtotal = 0
    
    for product_id, qty in cart_data.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            line_total = product.price * qty
            subtotal += line_total
            items.append({
                'product': product,
                'qty': qty,
                'line_total': line_total
            })
        except Product.DoesNotExist:
            continue
    
    discount = request.session.get('cart_discount', 0)
    total = subtotal - discount
    
    context = {
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

def cart_add(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        cart_data = request.session.get('cart', {})
        
        if str(product_id) in cart_data:
            cart_data[str(product_id)] += qty
        else:
            cart_data[str(product_id)] = qty
        
        request.session['cart'] = cart_data
        request.session.modified = True
        messages.success(request, f'{product.name} added to cart!')
    
    return redirect('store:cart')

def cart_update(request, product_id):
    """Update product quantity in cart"""
    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        cart_data = request.session.get('cart', {})
        
        if qty > 0:
            cart_data[str(product_id)] = qty
        else:
            cart_data.pop(str(product_id), None)
        
        request.session['cart'] = cart_data
        request.session.modified = True
        messages.success(request, 'Cart updated!')
    
    return redirect('store:cart')

def cart_remove(request, product_id):
    """Remove a product from the cart"""
    cart_data = request.session.get('cart', {})
    cart_data.pop(str(product_id), None)
    
    request.session['cart'] = cart_data
    request.session.modified = True
    messages.success(request, 'Item removed from cart!')
    
    return redirect('store:cart')

def apply_coupon(request):
    """Apply a coupon code to the cart"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        # Simple coupon logic - you can expand this
        if code.upper() == 'SAVE10':
            request.session['cart_discount'] = 10
            messages.success(request, 'Coupon applied! ₹10 discount.')
        else:
            messages.error(request, 'Invalid coupon code.')
    
    return redirect('store:cart')

def checkout(request):
    """Checkout page - redirect to orders checkout"""
    return redirect('orders:checkout')
