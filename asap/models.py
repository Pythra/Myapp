from django.contrib.auth.models import User  # Use the default User model
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
)
from requests.exceptions import ConnectionError, HTTPError

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
    id = models.IntegerField(primary_key=True, default=0)  
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    verified = models.BooleanField(default=False)
    allow_notifications = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)  # Username field under Profile
    email = models.EmailField(unique=True, blank=True, null=True)  # Email field under Profile
    pin = models.CharField(max_length=4, null=True, blank=True)  # Hashed PIN field
    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
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
    
class ExpoDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Consistent with other models
    expo_token = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s device"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def send_push_message(token, title, message):
    try:
        response = PushClient().publish(
            PushMessage(
                to=token,
                title=title,
                body=message,
                data={'type': 'notification'}  # You can add custom data here
            )
        )
    except PushServerError as exc:
        print(f"Push server error: {exc}")
        # Handle server errors
        return False
    except (ConnectionError, HTTPError) as exc:
        print(f"Connection error: {exc}")
        # Handle connection errors
        return False
    except DeviceNotRegisteredError:
        # Handle inactive devices
        ExpoDevice.objects.filter(expo_token=token).update(active=False)
        return False
    
    return True

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:  # Only send notification for newly created instances
        # Get all active device tokens
        active_devices = ExpoDevice.objects.filter(active=True)
        
        for device in active_devices:
            send_push_message(
                device.expo_token,
                instance.title,
                instance.content
            )

# Register the signal
post_save.connect(send_notification, sender=Notification)

 

