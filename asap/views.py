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
import re


POSTMARK_API_URL = "https://api.postmarkapp.com/email"
POSTMARK_API_TOKEN = "c63c358d-8bc7-4c50-a152-e7ead3290119"
POSTMARK_FROM_EMAIL = "support@useasappay.com"

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_email_verification(request):
    """Send verification code to email before signup using Postmark."""
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate verification code
    verification_code = generate_verification_code()
    
    # Store the code in cache with 10-minute expiry
    cache_key = f"email_verification_{email}"
    cache.set(cache_key, verification_code, timeout=600)

    # Email payload for Postmark
    payload = {
        "From": POSTMARK_FROM_EMAIL,
        "To": email,
        "Subject": "Your Email Verification Code",
        "HtmlBody": f"<p>Your verification code is: <strong>{verification_code}</strong></p>",
        "MessageStream": "outbound"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_TOKEN
    }

    try:
        # Send the POST request to Postmark
        response = requests.post(POSTMARK_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Failed to send email: {response.text}"}, status=response.status_code)
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_code(request):
    """Verify the code sent to email."""
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({"error": "Email and verification code are required"}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f"email_verification_{email}"
    stored_code = cache.get(cache_key)

    if not stored_code:
        return Response({"error": "Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)

    if code != stored_code:
        return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

    # Clear the code from cache
    cache.delete(cache_key)

    return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_code(request):
    """Resend verification code to email using Postmark."""
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate a new verification code
    verification_code = generate_verification_code()
    cache_key = f"email_verification_{email}"
    cache.set(cache_key, verification_code, timeout=600)

    # Email payload for Postmark
    payload = {
        "From": POSTMARK_FROM_EMAIL,
        "To": email,
        "Subject": "Your New Email Verification Code",
        "HtmlBody": f"<p>Your new verification code is: <strong>{verification_code}</strong></p>",
        "MessageStream": "outbound"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_TOKEN
    }

    try:
        # Send the POST request to Postmark
        response = requests.post(POSTMARK_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return Response({"message": "New verification code sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Failed to send email: {response.text}"}, status=response.status_code)
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class SignupView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not all([first_name, last_name, password, email, phone]):
            return Response(
                {"error": "First name, last name, email, phone, and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate username
        username = f"{first_name.lower()}_{last_name.lower()}"

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "A user with this first and last name already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Profile.objects.filter(phone=phone).exists():
            return Response(
                {"error": "Phone number already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Password validation
        if not self.validate_password(password, first_name, last_name):
            return Response(
                {"error": "Password must be at least 8 characters long, not similar to your name, and not entirely numeric."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(
            id=user.id,
            user=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        profile.set_pin(request.data.get('pin'))  # Set the PIN if provided
        profile.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "User created successfully.", "token": token.key}, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_password(password, first_name, last_name):
        return (
            len(password) >= 8 and
            first_name.lower() not in password.lower() and
            last_name.lower() not in password.lower() and
            not password.isdigit()
        )

 
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
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    authentication_classes = [TokenAuthentication] 

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