from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
import requests
from .models import Profile, Bank, GiftCard, GiftCardDeposit, GiftCardImage, Notification, Crypto, CryptoDeposit
from .serializers import ProfileSerializer, BankSerializer, GiftCardImageSerializer, NotificationSerializer, CryptoSerializer, CryptoDepositSerializer, GiftCardSerializer, GiftCardDepositSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
from rest_framework.response import Response 
from django.core.mail import send_mail 
from django.views.decorators.csrf import csrf_exempt 
import random
import string 
import string
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

User = get_user_model()

# ✅ Function to generate a 6-digit verification code
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_email_verification(request):
    """Sends a verification email with a code."""
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists
    if User.objects.filter(email=email).exists():
        return Response({"email_exists": True, "error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Generate and store verification code in cache
    verification_code = generate_verification_code()
    cache_key = f"email_verification_{email}"
    cache.set(cache_key, verification_code, timeout=600)

    subject = "Your Asap Pay Email Verification Code"
    message = f"Your verification code is: {verification_code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        print("📨 Sending email to:", email) 
        print(verification_code) # Debugging
        send_mail(subject, message, from_email, [email])
        print("✅ Email sent!")  # Debugging
        return Response({"message": "Verification code sent successfully"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print("❌ Email sending error:", str(e))  # Debugging
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
    """Resends a new verification code via email."""
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Generate a new verification code
    verification_code = generate_verification_code()
    cache_key = f"email_verification_{email}"
    cache.set(cache_key, verification_code, timeout=600)

    subject = "Your New Asap Pay Email Verification Code"
    message = f"Your new verification code is: {verification_code}"
    from_email = "Asap Pay Support <Support@useasappay.com>"

    try:
        send_mail(subject, message, from_email, [email])
        return Response({"message": "New verification code sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username') 
        password = request.data.get('password')
        email = request.data.get('email')  

        if not all([username, password, email]):
            return Response(
                {"error": "Username, password, email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "A user with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Password validation
        if not self.validate_password(password, username):
            return Response(
                {"error": "Password must be at least 8 characters long, not similar to your username, and not entirely numeric."},
                status=status.HTTP_400_BAD_REQUEST, 
            )

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Generate a unique 7-character referral code
        referral_code = self.generate_referral_code()

        # Create the profile
        profile = Profile(
            id=user.id,
            user=user, 
            email=email, 
            referral_code=referral_code,
        )
        
        profile.save()

        # Generate an authentication token
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {"message": "User created successfully.", "token": token.key, "referral_code": referral_code},
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def validate_password(password, username):
        """Validates password requirements."""
        return (
            len(password) >= 8 and
            username.lower() not in password.lower() and 
            not password.isdigit()
        )

    @staticmethod
    def generate_referral_code():
        """Generates a unique 7-character referral code."""
        import random
        import string
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            if not Profile.objects.filter(referral_code=code).exists():
                return code

    @staticmethod
    def validate_password(password, username):
        return (
            len(password) >= 8 and
            username.lower() not in password.lower() and 
            not password.isdigit()
        )

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request): 
        if request.user.auth_token:
            request.user.auth_token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny] 

 
class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

 
class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[AllowAny] 
    
class BankListView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class BankCreateView(generics.CreateAPIView):
    serializer_class = BankSerializer
    permission_classes = [AllowAny]
 

class BankDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)


class CryptoViewSet(ModelViewSet):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer

class CryptoDepositViewSet(ModelViewSet):
    queryset = CryptoDeposit.objects.all()
    serializer_class = CryptoDepositSerializer

class GiftCardViewSet(ModelViewSet):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer

class GiftCardDepositViewSet(ModelViewSet):
    queryset = GiftCardDeposit.objects.all()
    serializer_class = GiftCardDepositSerializer
class GiftCardImageViewSet(ModelViewSet):
    queryset = GiftCardImage.objects.all()
    serializer_class = GiftCardImageSerializer

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
 
@api_view(['DELETE'])
def delete_user(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({'error': 'Authorization header is improperly formatted'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data

        # Extract current and new passwords
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if all fields are provided
        if not current_password or not new_password or not confirm_password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the current password
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if new password matches confirmation
        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    token = auth_header.split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        user.delete()  # Deletes the user
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
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

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Authorization header is improperly formatted'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract token and validate it
        token = auth_header.split(' ')[1]
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data

        # Extract current and new passwords
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if all fields are provided
        if not current_password or not new_password or not confirm_password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the current password
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if new password matches confirmation
        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

def get_usd_to_ngn_rate():
    url = "https://v6.exchangerate-api.com/v6/ccb35bc50cdaaf2139965393/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["conversion_rates"]["NGN"]
        return round(exchange_rate, 2)  

    return None  # Return None if the request fails


@csrf_exempt
@require_http_methods(["GET"])
def exchange_rate_api(request):
    """
    API endpoint to get USD to NGN exchange rate with crypto adjustments
    """
    # Get base exchange rate
    usd_to_ngn = get_usd_to_ngn_rate()
    
    if usd_to_ngn is None:
        return JsonResponse({
            "success": False,
            "error": "Failed to fetch exchange rate"
        }, status=500)
    
    # Calculate rates for different cryptocurrencies
    rates = {
        "BTC": usd_to_ngn + 30,
        "USDT": usd_to_ngn + 40,
        "ETH": usd_to_ngn - 10,
        "USDC": usd_to_ngn + 40,
        "BNB": usd_to_ngn - 10,
        "LTC": usd_to_ngn - 10,
        "SOL": usd_to_ngn - 10,
        "DOGE": usd_to_ngn - 10,
        "DEFAULT": usd_to_ngn
    }
    
    # Return the rates
    return JsonResponse({
        "success": True,
        "base_rate": usd_to_ngn,
        "rates": rates
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    user = authenticate(username=identifier, password=password)

    if user is None:
        try:
            user = User.objects.get(email=identifier)
            if not user.check_password(password):
                user = None
        except User.DoesNotExist:
            user = None

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': {'id': user.id, 'username': user.username, 'email': user.email}})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)