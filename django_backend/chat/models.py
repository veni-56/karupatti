from django.db import models
from accounts.models import CustomUser
from store.models import Shop, Product


class Conversation(models.Model):
    """Chat conversation between buyer and seller"""
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer_conversations')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_conversations')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='conversations')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ['buyer', 'shop']
    
    def __str__(self):
        return f"{self.buyer.username} - {self.shop.name}"
    
    @property
    def last_message(self):
        return self.messages.first()
    
    def unread_count(self, user):
        """Get unread message count for a user"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """Individual message in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Content
    message = models.TextField()
    image = models.ImageField(upload_to='chat/', blank=True, null=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"
