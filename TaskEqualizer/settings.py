"""
Django settings for TaskEqualizer project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import base64
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PRODUCTION = False
CLIENT_HOST = os.getenv("CLIENT_HOST")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if PRODUCTION else True

HOST = "taskequalizer-production.up.railway.app"
ALLOWED_HOSTS = ["taskequalizer-production.up.railway.app"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks_api.apps.TasksApiConfig",
    "ninja",
    "auth_api",
    "corsheaders",
    "subscriptions",
    "emailmanager",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "TaskEqualizer.urls"

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

WSGI_APPLICATION = "TaskEqualizer.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

SUPABASE_USER = os.getenv("SUPABASE_USER")
SUPABASE_HOST = os.getenv("SUPABASE_HOST")
SUPABASE_PORT = os.getenv("SUPABASE_PORT")
SUPABASE_DBNAME = os.getenv("SUPABASE_DBNAME")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

# if PRODUCTION is True:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": SUPABASE_DBNAME,
        "USER": SUPABASE_USER,
        "PASSWORD": SUPABASE_PASSWORD,
        "HOST": SUPABASE_HOST,
        "PORT": SUPABASE_PORT,
    }
}
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ALLOWED_ORIGINS = [CLIENT_HOST]
CORS_ALLOW_CREDENTIALS = True


# Default field to exclude from the schemas
STANDARD_EXCLUDE = ["id", "created_at", "updated_at"]

# Maximum and minimum time for a task
MAX_SECOND_FOR_TASK = 60 * 60 * 2
MIN_SECOND_FOR_TASK = 60 * 1

# Token settings
SECRET_KEY = str(os.getenv("SECRET_KEY"))
TOKEN_NAME = "auth_token"

# Fields restrictions settings
MAX_LENGTH_FAMILY_NAME = 25
MIN_LENGTH_FAMILY_NAME = 2
MAX_LENGTH_USERNAME = 25
MIN_LENGTH_USERNAME = 2
MIN_POSSIBLE_TASK_NAME = 2
MAX_POSSIBLE_TASK_NAME = 13
MIN_EPHERMERAL_TASK_NAME = 2
MAX_EPHERMERAL_TASK_NAME = 25
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
INVITATION_CODE_SIZE = 8


# Stripe
STRIP_PUBLISHABLE_KEY = os.getenv("STRIP_PUBLISHABLE_KEY")
STRIP_SECRET_KEY = os.getenv("STRIP_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Email
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
DOMAIN_EMAIL = os.getenv("DOMAIN_EMAIL")
CONFIRMATION_URL = f"{HOST}/confirm"
REGISTER_WITH_CODE_URL = CLIENT_HOST + "/auth-page/register-with-invitation"
RESET_PASSWORD_URL = CLIENT_HOST + "/auth-page/reset-password"

# Sécurity
AES_KEY = base64.b64decode(os.getenv("AES_KEY"))
