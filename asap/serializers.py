from rest_framework import serializers
from .models import Profile, Bank, Giftcard, Notification

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
        'user': {'read_only': True},   
        'joined': {'read_only': True},
    }

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'



class GiftcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giftcard
        fields = '__all__'

        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

