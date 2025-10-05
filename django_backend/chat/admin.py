from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'seller', 'shop', 'product', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['buyer__username', 'seller__username', 'shop__name']
    raw_id_fields = ['buyer', 'seller', 'shop', 'product']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message', 'sender__username']
    raw_id_fields = ['conversation', 'sender']
    
    def message_preview(self, obj):
        return obj.message[:50]
    message_preview.short_description = 'Message'
