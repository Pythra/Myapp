from rest_framework import serializers
from .models import Profile, Bank

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone', 'first_name', 'last_name', 'pin','joined'] 


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'user', 'bank_name', 'account_name', 'bvn', 'joined']

