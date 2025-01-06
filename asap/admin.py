from django.contrib import admin
from .models import Bank, Profile , Notification

# Register the models to appear in the Django admin interface
admin.site.register(Bank)
admin.site.register(Profile) 
admin.site.register(Notification)
