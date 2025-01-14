from django.contrib.auth.models import User  # Use the default User model
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
import uuid

class Giftcard(models.Model):
    TYPE_CHOICES = [
        ('Amazon', 'Amazon'),
        ('Steam', 'Steam'),
        ('Google Play', 'Google Play'),
        ('iTunes', 'iTunes'),
        ('Xbox', 'Xbox'),
        ('PlayStation', 'PlayStation'),
        ('Netflix', 'Netflix'),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Cart Type")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giftcards')
    code = models.CharField(max_length=100, unique=True, verbose_name="Cart Code")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Expiration Date")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('redeemed', 'Redeemed')],
        default='active',
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At") 

    def __str__(self):
        return f"{self.type} - {self.code}"

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
        return str(self.id)


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
        return str(self.user)

class Crypto(models.Model): 
    name = models.TextField(max_length=100, unique=True, verbose_name="Content")
    price = models.PositiveIntegerField(default=1610)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
 

