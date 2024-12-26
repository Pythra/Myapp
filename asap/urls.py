from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import fetch_user, SignupView, LogoutView, ProfileListView, ProfileView, BankCreateView, BankListView, BankDetailView
 
 
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
    path('user/', fetch_user, name='fetch-user'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('profile/list/', ProfileListView.as_view(), name='profile-list'),  
    path('profile/', ProfileView.as_view(), name='profile'),  
    path('bank/', BankCreateView.as_view(), name='bank-create'),
    path('bank/list/', BankListView.as_view(), name='bank-list'),
    path('bank/<int:pk>/', BankDetailView.as_view(), name='bank-detail'),
]
