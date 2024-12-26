from django.contrib.auth.models import User  # Use the default User model
from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to default User model
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
        return self.username


class Bank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to default User model
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    bvn = models.CharField(max_length=15, null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)
