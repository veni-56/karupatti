from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'subtotal', 'seller_amount', 'platform_fee']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'payment_method', 'payment_status', 'status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'paid_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'notes')
        }),
        ('Shipping Information', {
            'fields': ('shipping_full_name', 'shipping_phone', 'shipping_street', 
                      'shipping_city', 'shipping_state', 'shipping_country', 'shipping_postal_code')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'payment_id', 'paid_at')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'subtotal', 'shop']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product_name']
