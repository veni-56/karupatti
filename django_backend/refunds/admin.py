from django.contrib import admin
from django.utils.html import format_html
from .models import RefundRequest, Refund, StoreCredit, StoreCreditTransaction


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'order', 'user', 'reason', 'refund_amount', 'status', 'created_at']
    list_filter = ['status', 'reason', 'created_at']
    search_fields = ['request_number', 'order__order_number', 'user__username']
    readonly_fields = ['request_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('request_number', 'order', 'order_item', 'user', 'refund_amount')
        }),
        ('Request Details', {
            'fields': ('reason', 'description', 'images')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Admin Response', {
            'fields': ('admin_notes', 'processed_by', 'processed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        for refund_request in queryset.filter(status='pending'):
            refund_request.approve(request.user, 'Approved by admin')
        self.message_user(request, f'{queryset.count()} refund requests approved.')
    approve_requests.short_description = 'Approve selected refund requests'
    
    def reject_requests(self, request, queryset):
        for refund_request in queryset.filter(status='pending'):
            refund_request.reject(request.user, 'Rejected by admin')
        self.message_user(request, f'{queryset.count()} refund requests rejected.')
    reject_requests.short_description = 'Reject selected refund requests'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['refund_number', 'order', 'user', 'amount', 'refund_method', 'status', 'created_at']
    list_filter = ['status', 'refund_method', 'created_at']
    search_fields = ['refund_number', 'order__order_number', 'user__username', 'transaction_id']
    readonly_fields = ['refund_number', 'created_at', 'completed_at']
    
    fieldsets = (
        ('Refund Information', {
            'fields': ('refund_number', 'refund_request', 'order', 'user', 'amount')
        }),
        ('Method', {
            'fields': ('refund_method',)
        }),
        ('Status', {
            'fields': ('status', 'transaction_id', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )


@admin.register(StoreCredit)
class StoreCreditAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StoreCreditTransaction)
class StoreCreditTransactionAdmin(admin.ModelAdmin):
    list_display = ['store_credit', 'transaction_type', 'amount', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['store_credit__user__username', 'description']
    readonly_fields = ['created_at']
