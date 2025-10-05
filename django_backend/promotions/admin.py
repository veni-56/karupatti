from django.contrib import admin
from .models import Event, Coupon, CouponUsage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'discount_percentage', 'start_date', 'end_date', 'is_active', 'is_ongoing']
    list_filter = ['event_type', 'is_active', 'start_date']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['products', 'categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'event_type', 'banner')
        }),
        ('Discount', {
            'fields': ('discount_percentage',)
        }),
        ('Applicable To', {
            'fields': ('products', 'categories')
        }),
        ('Timing', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )
    
    def is_ongoing(self, obj):
        return obj.is_ongoing
    is_ongoing.boolean = True


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'times_used', 'usage_limit', 'valid_from', 'valid_until', 'is_active']
    list_filter = ['discount_type', 'is_active', 'valid_from']
    search_fields = ['code', 'description']
    filter_horizontal = ['products', 'categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description')
        }),
        ('Discount', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Restrictions', {
            'fields': ('min_purchase_amount',)
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_limit_per_user', 'times_used')
        }),
        ('Applicable To', {
            'fields': ('products', 'categories')
        }),
        ('Timing', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'order_number', 'discount_amount', 'used_at']
    list_filter = ['used_at']
    search_fields = ['coupon__code', 'user__username', 'order_number']
    readonly_fields = ['used_at']
