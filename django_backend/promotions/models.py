from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from store.models import Product, Category
from decimal import Decimal


class Event(models.Model):
    """Flash sales and special events"""
    EVENT_TYPE_CHOICES = [
        ('flash_sale', 'Flash Sale'),
        ('seasonal', 'Seasonal Sale'),
        ('clearance', 'Clearance'),
        ('special', 'Special Event'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='flash_sale')
    
    # Discount
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Banner/Image
    banner = models.ImageField(upload_to='events/', blank=True, null=True)
    
    # Products
    products = models.ManyToManyField(Product, related_name='events', blank=True)
    categories = models.ManyToManyField(Category, related_name='events', blank=True)
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    
    @property
    def is_upcoming(self):
        return self.is_active and self.start_date > timezone.now()
    
    @property
    def is_expired(self):
        return self.end_date < timezone.now()
    
    def get_discounted_price(self, original_price):
        """Calculate discounted price"""
        discount_amount = original_price * (self.discount_percentage / Decimal('100'))
        return original_price - discount_amount


class Coupon(models.Model):
    """Discount coupons"""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    # Discount
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Restrictions
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Usage limits
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Total times this coupon can be used")
    usage_limit_per_user = models.PositiveIntegerField(default=1, help_text="Times each user can use this coupon")
    times_used = models.PositiveIntegerField(default=0)
    
    # Applicable to
    products = models.ManyToManyField(Product, related_name='coupons', blank=True)
    categories = models.ManyToManyField(Category, related_name='coupons', blank=True)
    
    # Timing
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from > now or self.valid_until < now:
            return False
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False
        return True
    
    def can_use(self, user, cart_total):
        """Check if user can use this coupon"""
        if not self.is_valid:
            return False, "Coupon is not valid"
        
        if cart_total < self.min_purchase_amount:
            return False, f"Minimum purchase amount is ${self.min_purchase_amount}"
        
        # Check user usage
        user_usage = CouponUsage.objects.filter(coupon=self, user=user).count()
        if user_usage >= self.usage_limit_per_user:
            return False, "You have already used this coupon"
        
        return True, "Coupon is valid"
    
    def calculate_discount(self, cart_total):
        """Calculate discount amount"""
        if self.discount_type == 'percentage':
            discount = cart_total * (self.discount_value / Decimal('100'))
        else:
            discount = self.discount_value
        
        # Apply max discount limit
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        
        # Don't exceed cart total
        discount = min(discount, cart_total)
        
        return discount


class CouponUsage(models.Model):
    """Track coupon usage"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='coupon_usages')
    order_number = models.CharField(max_length=32)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.user.username} used {self.coupon.code}"
