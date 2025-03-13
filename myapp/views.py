from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    def get(self, request, *args, **kwargs):
        # Redirect to the app's main screen or any other screen
        return redirect('/app-main-screen/')
