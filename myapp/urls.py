from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomPasswordChangeDoneView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('asap.urls')),
    path('accounts/password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
