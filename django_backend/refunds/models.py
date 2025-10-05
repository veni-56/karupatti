from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from orders.models import Order, OrderItem
from decimal import Decimal


class RefundRequest(models.Model):
    """Refund request for an order or order item"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    REASON_CHOICES = [
        ('defective', 'Defective Product'),
        ('wrong_item', 'Wrong Item Received'),
        ('not_as_described', 'Not as Described'),
        ('damaged', 'Damaged in Shipping'),
        ('changed_mind', 'Changed Mind'),
        ('other', 'Other'),
    ]
    
    # Reference
    request_number = models.CharField(max_length=32, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refund_requests')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='refund_requests', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='refund_requests')
    
    # Request details
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField()
    images = models.ImageField(upload_to='refunds/', blank=True, null=True)
    
    # Refund amount
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin response
    admin_notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_refunds')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund {self.request_number} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            # Generate unique request number
            import uuid
            self.request_number = f"REF{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def approve(self, admin_user, notes=''):
        """Approve refund request"""
        self.status = 'approved'
        self.admin_notes = notes
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.save()
        
        # Create refund transaction
        Refund.objects.create(
            refund_request=self,
            order=self.order,
            user=self.user,
            amount=self.refund_amount,
            status='pending'
        )
    
    def reject(self, admin_user, notes=''):
        """Reject refund request"""
        self.status = 'rejected'
        self.admin_notes = notes
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.save()


class Refund(models.Model):
    """Actual refund transaction"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    REFUND_METHOD_CHOICES = [
        ('original', 'Original Payment Method'),
        ('store_credit', 'Store Credit'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    # Reference
    refund_number = models.CharField(max_length=32, unique=True, editable=False)
    refund_request = models.OneToOneField(RefundRequest, on_delete=models.CASCADE, related_name='refund')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='refunds')
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Method
    refund_method = models.CharField(max_length=20, choices=REFUND_METHOD_CHOICES, default='original')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction details
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund {self.refund_number} - ${self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.refund_number:
            # Generate unique refund number
            import uuid
            self.refund_number = f"RFD{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def complete(self, transaction_id=''):
        """Mark refund as completed"""
        self.status = 'completed'
        self.transaction_id = transaction_id
        self.completed_at = timezone.now()
        self.save()
        
        # Update refund request status
        self.refund_request.status = 'completed'
        self.refund_request.save()


class StoreCredit(models.Model):
    """Store credit for users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='store_credit')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - ${self.balance}"
    
    def add_credit(self, amount, description=''):
        """Add credit to balance"""
        self.balance += amount
        self.save()
        
        StoreCreditTransaction.objects.create(
            store_credit=self,
            transaction_type='credit',
            amount=amount,
            description=description,
            balance_after=self.balance
        )
    
    def deduct_credit(self, amount, description=''):
        """Deduct credit from balance"""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            
            StoreCreditTransaction.objects.create(
                store_credit=self,
                transaction_type='debit',
                amount=amount,
                description=description,
                balance_after=self.balance
            )
            return True
        return False


class StoreCreditTransaction(models.Model):
    """Store credit transaction history"""
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    store_credit = models.ForeignKey(StoreCredit, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - ${self.amount}"
