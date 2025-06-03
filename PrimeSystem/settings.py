import logging
from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # Third party
    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'jalali_date',
    'django_ckeditor_5',
    'hitcount',
    'colorfield',
    'django_json_widget',
    'django_render_partial',
    'nplusone.ext.django',
    # My app
    'apps.account_app.apps.AccountAppConfig',
    'apps.blog_app.apps.BlogAppConfig',
    'apps.home_app.apps.HomeAppConfig',
    'apps.product_app.apps.ProductAppConfig',
    'apps.contact_app.apps.ContactAppConfig',
    'apps.cart_app.apps.CartAppConfig',
    'apps.paymentGateway_app.apps.PaymentgatewayAppConfig',
]

MIDDLEWARE = [
    'nplusone.ext.django.NPlusOneMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PrimeSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.context_processors.base_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'PrimeSystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
SITE_ID = 1

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account_app.CustomUser'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = True
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

NPLUSONE_LOGGER = logging.getLogger('root')
NPLUSONE_LOG_LEVEL = logging.WARN

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",  # Optional: Adds a format for better readability
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {  # Captures Django's internal logs (e.g., server errors)
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,  # Prevent propagation to other loggers
        },
        "django.request": {  # Specifically for HTTP request-related errors (e.g., 500 errors)
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {  # For errors from the development server
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

LOGGER = logging.getLogger("root")

RSI_PUBLIC_KEY = os.path.join(BASE_DIR, '0060546281.txt')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.product_app.pagination.CustomPagination',
    'PAGE_SIZE': 100,
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_AGE = 345600  # 4 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# SMS SETTINGS
from .custom_settings.kavenegar_settings import *

# JAZZMIN ADMIN PANEL SETTING
from .custom_settings.jazzmin_settings import *

# CKEDITOR SETTINGS
from .custom_settings.ckeditor_settings import *

# EMAIL SETTINGS
from .custom_settings.email_settings import *
