from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import get_coins, fetch_user, delete_user, exchange_rate_api, GiftCardImageViewSet, ChangePasswordView ,verify_email_code, initiate_email_verification, resend_verification_code, NotificationView, ProfileListCreateView, SignupView, LogoutView, ProfileDetailView,  ProfileView, BankCreateView, BankListView, BankDetailView, CryptoViewSet, CryptoDepositViewSet, GiftCardViewSet, GiftCardDepositViewSet, login, PasswordResetRequestView, PasswordResetConfirmView

from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('user/', fetch_user, name='fetch-user'),
    path('delete/user/', delete_user, name='delete-user'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('profile/list/', ProfileListCreateView.as_view(), name='profile-list'),  
    path('profile/', ProfileView.as_view(), name='profile'),    
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),  
    path('bank/', BankCreateView.as_view(), name='bank-create'),
    path('bank/list/', BankListView.as_view(), name='bank-list'),
    path('bank/<int:pk>/', BankDetailView.as_view(), name='bank-detail'),
    path('coins/', get_coins, name='get_coins'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('initiate-email-verification/', initiate_email_verification, name='initiate_email_verification'),
    path('verify-email-code/', verify_email_code, name='verify_email_code'),
    path('resend-verification-code/', resend_verification_code, name='resend_verification_code'),
    path('notifications/list/', NotificationView.as_view(), name='notification-list'),
    path('exchange-rate/',  exchange_rate_api, name='exchange_rate_api'),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"), 
    path('api/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cryptos/', CryptoViewSet.as_view({'get': 'list', 'post': 'create'}), name='crypto-list-create'),
    path('cryptos/<int:pk>/', CryptoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='crypto-detail'),
    # Crypto Deposit URLs
    path('crypto-deposits/', CryptoDepositViewSet.as_view({'get': 'list', 'post': 'create'}), name='crypto-deposit-list-create'),
    path('crypto-deposits/<int:pk>/', CryptoDepositViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='crypto-deposit-detail'),

    # Gift Card URLs
    path('giftcards/', GiftCardViewSet.as_view({'get': 'list', 'post': 'create'}), name='giftcard-list-create'),
    path('giftcards/<int:pk>/', GiftCardViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='giftcard-detail'),
    path('giftcard-images/', GiftCardImageViewSet.as_view({'post': 'create'}), name='giftcard-image-upload'),

    # Gift Card Deposit URLs
    path('giftcard-deposits/', GiftCardDepositViewSet.as_view({'get': 'list', 'post': 'create'}), name='giftcard-deposit-list-create'),
    path('giftcard-deposits/<int:pk>/', GiftCardDepositViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='giftcard-deposit-detail'),

    # Password Reset URLs
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
