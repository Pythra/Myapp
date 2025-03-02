from rest_framework import serializers
from .models import Profile, Bank, GiftCard, GiftCardDeposit, GiftCardImage, Notification, Crypto, CryptoDeposit

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


class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'

class GiftcardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardImage
        fields = '__all__'


class GiftCardDepositSerializer(serializers.ModelSerializer):
    giftcard = serializers.PrimaryKeyRelatedField(queryset=GiftCard.objects.all())

    images = serializers.ListField(
        child=serializers.FileField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False  # Set to False since we're sending files
        ),
        required=False,
        write_only=True
    )

    class Meta:
        model = GiftCardDeposit
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        giftcard_deposit = GiftCardDeposit.objects.create(**validated_data)

        if images_data:
            for image_url in images_data:
                GiftCardImage.objects.create(
                    gift_card=giftcard_deposit.giftcard,
                    image=image_url  # Store the URL instead of a file
                )

        return giftcard_deposit

    
class GiftCardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCardImage
        fields = ['gift_card', 'image']


class CryptoSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = Crypto 
        fields = '__all__'
        
    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None
    
class CryptoDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoDeposit
        fields = '__all__'

        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

