from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import get_coins, fetch_user, delete_user, ChangePasswordView, verify_email_code, initiate_email_verification, resend_verification_code, NotificationView, ProfileListCreateView, SignupView, LogoutView, ProfileDetailView, GiftCardDetailView, GiftCardListCreateView, ProfileView, BankCreateView, BankListView, BankDetailView
 
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
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
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),,
    path('giftcards/', GiftCardListCreateView.as_view(), name='giftcard-list-create'),
    path('giftcards/<int:id>/', GiftCardDetailView.as_view(), name='giftcard-detail'),
    path('initiate-email-verification/', initiate_email_verification, name='initiate_email_verification'),
    path('verify-email-code/', verify_email_code, name='verify_email_code'),
    path('resend-verification-code/', resend_verification_code, name='resend_verification_code'),
    path('notifications/list/', NotificationView.as_view(), name='notification-list'),
]
