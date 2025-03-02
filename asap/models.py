from django.contrib.auth.models import User  # Use the default User model
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from decimal import Decimal 


STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Crypto(models.Model):
    name = models.CharField(max_length=22)
    rate = models.DecimalField(max_digits=10, default=0.00, decimal_places=2,)
    logo = models.ImageField(upload_to='crypto_logos/', null=True, blank=True)   

class CryptoDeposit(models.Model):
    status = models.CharField(choices=STATUS, max_length=25, default='pending')
    depositor = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=15, decimal_places=8, default=0.00, blank=True, null=True)  
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)  
    naira = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, blank=True, null=True)  
    created_on = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to='deposit_screenshots/', null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.depositor} deposited ({self.quantity} {self.crypto})"
    
 
class GiftCard(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, default="", null=True, blank=True)  # e.g., Physical, E-code
    country = models.CharField(max_length=100, default="", null=True, blank=True)  
    price_range = models.CharField(max_length=100, default="", null=True, blank=True)  # e.g., $10-$500
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Rate in naira
    logo = models.ImageField(upload_to='giftcard_logos/', null=True, blank=True)   

    def __str__(self):
        return f"{self.name} {self.country} - {self.price_range} @ ₦{self.exchange_rate} {self.id}"

class GiftCardDeposit(models.Model): 
    type = models.CharField(max_length=50, verbose_name="Cart Type") 
    status = models.CharField(choices=STATUS, max_length=25, default='pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    giftcard = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, default="", null=True, blank=True) 
    pin = models.CharField(max_length=15, default="", blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    naira = models.DecimalField(max_digits=25, decimal_places=2, default=0.00, blank=True, null=True)  
    created_on = models.DateTimeField(auto_now_add=True)  
  
    def save(self, *args, **kwargs):
    # Change from category to giftcard to match the field name
        if self.giftcard and self.price:
            self.naira = Decimal(str(self.price)) * self.giftcard.exchange_rate
        super().save(*args, **kwargs)

    def __str__(self):
    # Fix indentation and field reference (from category to giftcard)
        return f"{self.owner}: {self.giftcard.name} - ${self.price}"
    

class GiftCardImage(models.Model):
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='giftcard_images/')

    def __str__(self):
        return f"Gift card image for {self.gift_card.name}"

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    id = models.IntegerField(primary_key=True, default=0)  
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    verified = models.BooleanField(default=False)
    allow_notifications = models.BooleanField(default=False) 
    gender = models.CharField(max_length=150, choices=GENDER_CHOICES, blank=True,)  # Username field under Profile
    email = models.EmailField(unique=True, blank=True, null=True)  # Email field under Profile
    pin = models.CharField(max_length=4, null=True, blank=True)  # Hashed PIN field
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)  # New field
    referral_code = models.CharField(max_length=7, unique=True, null=True, blank=True)  # Referral code field
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def set_pin(self, raw_pin):
        """Hashes and sets the PIN."""
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        """Validates the provided PIN against the stored hash."""
        return check_password(raw_pin, self.pin)

    def __str__(self):
        return str(self.user)


class Bank(models.Model): 
    id = models.IntegerField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=12, blank=True, null=True)
    bvn = models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)
    

class Notification(models.Model): 
    title = models.TextField(max_length=120)
    content = models.TextField(max_length=220, unique=True, verbose_name="Content")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
    def __str__(self):
        return str(self.title) 