from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("shops/", include("shops.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("orders/", include("orders.urls")),
    path("sellers/", include("sellers.urls")),
    path("promotions/", include("promotions.urls")),
    path("chat/", include("chat.urls")),
    path("refunds/", include("refunds.urls")),
    path("payments/", include("payments.urls")),
    path("", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
