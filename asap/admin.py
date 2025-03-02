from django.contrib import admin
from .models import Bank, Profile, Notification, GiftCard, GiftCardImage, GiftCardDeposit, Crypto, CryptoDeposit

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'verified', 'joined')
    search_fields = ('user__username', 'email', 'phone')
    list_filter = ('verified', 'joined')

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'account_number', 'active')
    search_fields = ('user__username', 'bank_name', 'account_number')
    list_filter = ('active',)

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'price_range', 'exchange_rate')
    search_fields = ('name', 'country')
    list_filter = ('country',)

@admin.register(GiftCardDeposit)
class GiftCardDepositAdmin(admin.ModelAdmin):
    list_display = ('owner', 'giftcard', 'type', 'price', 'status', 'created_on')
    search_fields = ('owner__username', 'giftcard__name', 'type')
    list_filter = ('status', 'created_on')

@admin.register(GiftCardImage)
class GiftCardImageAdmin(admin.ModelAdmin):
    list_display = ('gift_card', 'image')

@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'logo')
    search_fields = ('name',)

@admin.register(CryptoDeposit)
class CryptoDepositAdmin(admin.ModelAdmin):
    list_display = ('depositor', 'crypto', 'quantity', 'amount', 'naira', 'status', 'created_on')
    search_fields = ('depositor__username', 'crypto')
    list_filter = ('status', 'created_on')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ('title', 'content')
    list_filter = ('created',)
 