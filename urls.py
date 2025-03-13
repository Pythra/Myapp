from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]