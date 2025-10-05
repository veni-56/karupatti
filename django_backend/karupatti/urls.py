from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    path('orders/', include('orders.urls')),
    path('seller/', include('seller.urls')),
    path('promotions/', include('promotions.urls')),
    path('chat/', include('chat.urls')),
    path('refunds/', include('refunds.urls')),  # Added refunds URLs
    path('wishlist/', include('wishlist.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
