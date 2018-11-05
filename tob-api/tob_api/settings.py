"""
Django settings for tob_api project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import os.path

from pathlib import Path

from . import permissions
from . import authentication

try:
    from . import database
except:
    import database

try:
    from . import haystack
except:
    import haystack

def parse_bool(val):
    return val and val != '0' and str(val).lower() != "false"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    "75f46345-af2d-497d-a3ec-b6f05e5266f4",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = parse_bool(os.getenv("DJANGO_DEBUG", "True"))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # Add your apps here to enable them
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "haystack",
    "rest_framework",
    "drf_generators",
    "drf_yasg",
    "auditable",
    "api",
    "tob_api",
    "api_v2",
    "corsheaders",
]

HAYSTACK_CONNECTIONS = {"default": haystack.config()}

if os.getenv("ENABLE_REALTIME_INDEXING"):
    print("Enabling realtime indexing ...")
    HAYSTACK_SIGNAL_PROCESSOR = "api_v2.signals.RelatedRealtimeSignalProcessor"
else:
    print("Realtime indexing has been disabled ...")

HAYSTACK_DOCUMENT_FIELD = "document"

MIDDLEWARE_CLASSES = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "tob_api.urls"

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ORIGIN_ALLOW_ALL = True

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
            ]
        },
    }
]

WSGI_APPLICATION = "wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {"default": database.config()}

OPTIMIZE_TABLE_ROW_COUNTS = parse_bool(os.getenv("OPTIMIZE_TABLE_ROW_COUNTS", "True"))

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

AUTH_USER_MODEL = "api.User"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "tob_api.pagination.EnhancedPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": authentication.defaults(),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
    "USE_SESSION_AUTH": True,
}

LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/api/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "api": {
            "handlers": ["console_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["console_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console_handler"],
        "level": str(os.getenv("DJANGO_LOG_LEVEL", "INFO")).upper(),
        "propagate": False,
    },
}


if os.getenv("SQL_DEBUG"):
    LOGGING["filters"]["require_debug_true"] = {
        "()": "django.utils.log.RequireDebugTrue"
    }
    LOGGING["handlers"]["console"] = {
        "level": "DEBUG",
        "filters": ["require_debug_true"],
        "class": "logging.StreamHandler",
    }
    LOGGING["loggers"]["django.db.backends"] = {
        "level": "DEBUG",
        "handlers": ["console"],
    }

INDY_HOLDER_ID = "TheOrgBook_Holder"

APPLICATION_URL = os.getenv("APPLICATION_URL") or "http://localhost:8080"

API_METADATA = {
    "title": "TheOrgBook API",
    "description":
        "TheOrgBook is a public, searchable directory of digital records for registered "
        "businesses in the Province of British Columbia. Over time, other government "
        "organizations and businesses will also begin to issue digital records through "
        "TheOrgBook. For example, permits and licenses issued by various government services.",
    "terms": {
        "url": "https://www2.gov.bc.ca/gov/content/data/open-data",
    },
    "contact": {
        "email": "bcdevexchange@gov.bc.ca",
    },
    "license": {
        "name": "Open Government License - British Columbia",
        "url": "https://www2.gov.bc.ca/gov/content/data/open-data/api-terms-of-use-for-ogl-information",
    },
}

custom_settings_file = Path(
    BASE_DIR,
    "custom_settings_" + str(os.getenv("TOB_THEME")).lower() + ".py",
)
if custom_settings_file.exists():
    with open(custom_settings_file) as source_file:
        print(
            "Loading custom settings file: {}".format(custom_settings_file.name)
        )
        exec(source_file.read())
