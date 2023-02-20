"""
Django settings for nft_loans project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load environment variables and secrets
DJANGO_ENV = os.environ.get("DJANGO_ENV", "dev")

for dotenv_file in [f".env.{DJANGO_ENV}", f".env.{DJANGO_ENV}.local"]:
    dotenv_file = "nft_loans/configs/" + dotenv_file
    load_dotenv(os.path.join(BASE_DIR, dotenv_file))


# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST_NAME") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

BROKER_HEARTBEAT = 0
BROKER_POOL_LIMIT = None
# BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}
BROKER_CONNECTION_TIMEOUT = 30
BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = 20

# Celery settings
CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TASK_ACKS_LATE = False
CELERY_TASK_QUEUE_MAX_PRIORITY = 10
CELERY_CREATE_MISSING_QUEUES = True
CELERY_TASK_REMOTE_TRACEBACKS = True
CELERY_TASK_DEFAULT_QUEUE = "nft_loans_queue"
CELERY_TASK_RESULT_EXPIRES = 86400
CELERY_RESULT_EXPIRES = 86400
CELERY_ENABLE_UTC = False
CELERY_USE_TZ = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-elhi_*ia$6ur$wwh0$e43)%xras7u#y_ik$i7s4_*pu7bh7!o#"

# SECURITY WARNING: don't run with debug turned on in production!
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
DEBUG = True

ALLOWED_HOSTS = [
    os.getenv("DOMAIN_NAME", "localhost"),
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    # f"http://{os.getenv('DOMAIN_NAME', 'localhost')}",
    # f"https://{os.getenv('DOMAIN_NAME', 'localhost')}",
    "http://*.rensei.xyz",
    "https://*.rensei.xyz",
    # Add any other trusted domains to the list
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "django_celery_results",
    "django_celery_beat",
    "rest_framework",
    # custom apps
    "aggregators.apps.AggregatorsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nft_loans.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nft_loans.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

# django setting.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}
