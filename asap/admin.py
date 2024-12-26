from django.contrib import admin
from .models import Bank, Profile 

# Register the models to appear in the Django admin interface
admin.site.register(Bank)
admin.site.register(Profile) 
