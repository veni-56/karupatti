from .models import Wishlist


def wishlist_count(request):
    """Add wishlist count to all templates"""
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            return {'wishlist_count': wishlist.item_count}
        except Wishlist.DoesNotExist:
            return {'wishlist_count': 0}
    return {'wishlist_count': 0}
