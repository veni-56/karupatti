from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps


def buyer_required(view_func):
    """Decorator to restrict access to buyers only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_buyer:
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def seller_required(view_func):
    """Decorator to restrict access to sellers only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_seller:
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to restrict access to admins only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_user:
            return redirect('accounts:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
