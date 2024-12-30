from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
import requests
from .models import Profile, Bank, Giftcard, Notification
from .serializers import ProfileSerializer, BankSerializer, NotificationSerializer,  GiftcardSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from rest_framework.response import Response 
from django.core.mail import send_mail 
from django.views.decorators.csrf import csrf_exempt 
import random
import string
from django.core.cache import cache
from django.conf import settings


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))
@api_view(['POST'])
@permission_classes([AllowAny])


def initiate_email_verification(request):
    """Send verification code to email before signup"""
    try:
        email = request.data.get('email')
        
        if not email:
            return Response({
                "error": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Generate verification code
        verification_code = generate_verification_code()
        
        # Store the code in cache with 10 minute expiry
        cache_key = f"email_verification_{email}"
        cache.set(cache_key, verification_code, timeout=600)
        
        # Debug: Print email and verification code
        print(f"Sending email verification to: {email}")
        print(f"Verification code: {verification_code}")
        
        # Use settings for email configuration
        send_mail(
            subject='Your Email Verification Code',
            message=f'Your verification code is: {verification_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({
            "message": "Verification code sent successfully"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Log the actual error for debugging
        print(f"Email verification error: {str(e)}")
        return Response({
            "error": "Failed to send verification code. Please try again later."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_code(request):
    """Verify the code sent to email"""
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({
            "error": "Email and verification code are required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cache_key = f"email_verification_{email}"
    stored_code = cache.get(cache_key)
    
    if not stored_code:
        return Response({
            "error": "Verification code has expired"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if code != stored_code:
        return Response({
            "error": "Invalid verification code"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Clear the code from cache
    cache.delete(cache_key)
    
    return Response({
        "message": "Email verified successfully"
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_code(request):
    """Resend verification code to email"""
    email = request.data.get('email')
    
    if not email:
        return Response({
            "error": "Email is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    verification_code = generate_verification_code()
    cache_key = f"email_verification_{email}"
    cache.set(cache_key, verification_code, timeout=600)
    
    try:
        send_mail(
            'Your New Email Verification Code',
            f'Your new verification code is: {verification_code}',
            'noreply@Asappay.com',
            [email],
            fail_silently=False,
        )
        return Response({
            "message": "New verification code sent successfully"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "error": f"Failed to send verification code: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response(
                {"error": "Username, email, and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(id=user.id, user=user, username=username, email=email)
        profile.set_pin(request.data.get('pin'))  # Set the PIN if provided
        profile.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "User created successfully.", "token": token.key}, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = [AllowAny]  # Ensure the user is authenticated
    
    def post(self, request):
        # Check if the user is authenticated before attempting to delete the token
        if request.user and hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny] 

 
class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[AllowAny] 


    
class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[AllowAny] 

class BankListView(generics.ListAPIView):
    serializer_class = BankSerializer
    permission_classes = [AllowAny] 
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)


class BankCreateView(generics.CreateAPIView):
    serializer_class = BankSerializer
    permission_classes = [AllowAny]
 

class BankDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)


class GiftCardListCreateView(ListCreateAPIView):
    queryset = Giftcard.objects.all()
    serializer_class = GiftcardSerializer

# Retrieve, Update, and Delete View
class GiftCardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Giftcard.objects.all()
    serializer_class = GiftcardSerializer
    lookup_field = 'id'  # Default is 'pk', but specifying for clarity
 


class NotificationView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny] 

@api_view(['GET']) 
def fetch_user(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({'error': 'Authorization header is improperly formatted'}, status=status.HTTP_400_BAD_REQUEST)

    token = auth_header.split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        user_data = {
            'id': user.id,
            'username': user.username,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
 
 


@api_view(['GET'])
def get_coins(request):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '43be9fd4-af5b-4dbe-9379-6f749d993f8d',
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        response.raise_for_status()
        coins = response.json()['data']
        return Response({'coins': coins})
        print(coins)

    except requests.exceptions.RequestException as e:
        return Response({
            'error': str(e),
            'coins': []
        }, status=500)