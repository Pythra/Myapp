from pathlib import Path

import pymysql
BASE_DIR = Path(__file__).resolve().parent.parent
  
SECRET_KEY = 'django-insecure-58k)g(oj3c!ry(!v_g5z8tow&4ozd)&s4&*wck^c+c+5@d60wf'
 
DEBUG = True
ALLOWED_HOSTS = ['www.useasappay.com', 'useasappay.com', 'www.apprite.pythonanywhere.com', 'apprite.pythonanywhere.com', 'localhost', '127.0.0.1']
 
CORS_ALLOW_ALL_ORIGINS = True  # Allows requests from any origin during development
 
INSTALLED_APPS = [
    'corsheaders',  # Add CORS headers app
    'asap',  # Your custom app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST framework
    'rest_framework.authtoken',  # Token authentication
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware at the top
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files in production
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myapp.wsgi.application'
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u890283758_api_db',  # Database name
        'USER': 'u890283758_Support',  # Database user
        'PASSWORD': 'Ibra@9000',  # Replace with your actual password
        'HOST': 'localhost',  # Or use Hostinger’s MySQL host if provided
        'PORT': '3306',  # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
 
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
 
STATIC_URL = 'static/'
 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  


EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.hostinger.com"
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER="Support@useasappay.com"
EMAIL_HOST_PASSWORD="Ibra@9000"
DEFAULT_FROM_EMAIL="Asap Pay Support <Support@useasappay.com>"

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 