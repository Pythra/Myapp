from rest_framework import serializers
from .models import Profile, Bank, Giftcard, Notification

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user','email', 'phone', 'first_name', 'last_name', 'pin', 'verified', 'joined']
        extra_kwargs = {
            'user': {'read_only': True},   
            'joined': {'read_only': True},
        }

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'user', 'bank_name', 'account_name', 'bvn', 'joined']
        extra_kwargs = {
            'user': {'read_only': True},   
            'joined': {'read_only': True},
        }


class GiftcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giftcard
        fields = '__all__'

        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

