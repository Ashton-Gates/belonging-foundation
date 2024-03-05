from pathlib import Path
from dotenv import load_dotenv
import os

AUTH_USER_MODEL = 'accounts.CustomUser'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mq@((#x!tz0)v5bojl!ymb6s*5#s((h$ve9y88+j1(m%u427*o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','belonging.foundation', 'www.belonging.foundation', 'belonging-foundation.azurewebsites.net']
#'belonging.foundation', 'www.belonging.foundation'

# Application definition

INSTALLED_APPS = [
    'applicant',
    'belonging',
    'referee',    
    'donation',
    'accounts',
    'storages',    
    'auction',
    'customers',
    'djstripe',
    'password_reset',
    'widget_tweaks',
    'django.contrib.auth',    
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'venue',
    'vendor',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.google.GoogleOAuth2',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'accounts' / 'belonging' / 'templates'],
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

WSGI_APPLICATION = 'belonging.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'belonging-prod-database_2024-02-24T22-47Z',
        'USER': 'belo-admin',
        'PASSWORD': 'H1ng3isgro$$',
        'HOST': 'belonging-server.database.windows.net',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'encrypt': True,
            'trust_server_certificate': False,
        },
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to database file
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/




# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_SETTINGS_MODULE = 'belonging.settings'

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# For console backend (development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1
# For SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail use 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ashtonkinnell8@gmail.com'
EMAIL_HOST_PASSWORD = 'wnwl mdow uhlt xexe'
DEFAULT_FROM_EMAIL = 'ashtonkinnell8@gmail.com'
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"


CSRF_COOKIE_SECURE = True

CSRF_COOKIE_DOMAIN = 'belonging.foundation'

CSRF_TRUSTED_ORIGINS = ['https://belonging-foundation.azurewebsites.net','https://belonging.foundation', 'https://www.belonging.foundation']



ROOT_URLCONF = 'belonging.urls'

# Add Google provider configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': '1002728390308-vak0cu5k7mba0jiuf3u70hrm35ivbjv4.apps.googleusercontent.com',
            'secret': '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',
            'key': 'AIzaSyDTvLNzp7bZTN0eMiAaMWmAPXz6T9qCVw0'
        }
    }
}

# allauth specific settings
LOGIN_REDIRECT_URL = '/default_dashboard/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/default_dashboard/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1002728390308-vak0cu5k7mba0jiuf3u70hrm35ivbjv4.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/default_dashboard/'
SOCIAL_AUTH_LOGIN_URL = '/default_dashboard/'


# settings.py of the belonging app
INTERNAL_WEBHOOK_URL = 'https://abc123.ngrok.io/internal/webhook/'


DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AZURE_ACCOUNT_NAME = 'cs2100320034ce6f7de'
AZURE_ACCOUNT_KEY = 'eoOYES2iFvOHO/kbf/Y5KgvZqDW3JAGpVbXAsih1gtP3UJQEd8i9QyF+/9Vd8G50ZCFG2m649Eay+AStbwL+Tg=='
AZURE_CONTAINER = 'staticfiles'



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files settings
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
   ('belonging', os.path.join(BASE_DIR, 'belonging', 'static')),
)
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_51ObDcEKj0Am5FA1U8mu0YIyaYWgntAdOudVoidLPiCJlC9Ynm1WPHkIvrMFgy3Sph8JEOXARvuNDWoYEXNyFL1G30020D0t41u")
STRIPE_PUBLIC_KEY = 'pk_test_51ObDcEKj0Am5FA1UXZR8BaefNnGDzw6pOrmSSHX499OWIxsrNZCwjxHAG1HbgitVA0c4GhTwOOwaPqLIQazy0o6W00GZroVGqf'
STRIPE_PRIVATE_KEY = 'sk_test_51ObDcEKj0Am5FA1U8mu0YIyaYWgntAdOudVoidLPiCJlC9Ynm1WPHkIvrMFgy3Sph8JEOXARvuNDWoYEXNyFL1G30020D0t41u'
DJSTRIPE_WEBHOOK_SECRET = 'whsec_84219e91f49eaacb54edaedc816f3712bb2afc053b6bbfafe657e5028681b036'
DJSTRIPE_USE_NATIVE_JSONFIELD = True



#SECURE_SSL_REDIRECT = True