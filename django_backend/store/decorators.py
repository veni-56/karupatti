from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        seller = getattr(request.user, "seller_profile", None)
        if not request.user.is_authenticated or not seller:
            messages.error(request, "Seller account required.")
            return redirect("store:seller-register")
        return view_func(request, *args, **kwargs)
    return _wrapped
