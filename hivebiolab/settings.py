import os
import sys
from pathlib import Path

import cloudinary
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


def config_bool(name: str, default: bool = False) -> bool:
    value = config(name, default=None)

    if value is None or value == "":
        return default

    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on", "dev", "development", "local"}:
        return True
    if normalized in {"0", "false", "no", "off", "prod", "production", "release"}:
        return False

    raise ValueError(f"Invalid truth value for {name}: {value}")


def config_list(name: str, default: str = "") -> list[str]:
    value = config(name, default=default)
    return [
        item.strip()
        for item in str(value).replace(",", " ").split()
        if item.strip()
    ]


# ─────────────────────────────
# Core security
# ─────────────────────────────

SECRET_KEY = config("SECRET_KEY", default="django-insecure-local-only")

DEBUG = config_bool("DEBUG", default=False)
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
BUILDING = config_bool("DJANGO_BUILD", default=False)

ALLOWED_HOSTS = config_list("ALLOWED_HOSTS", default="biolab-api.kumasihive.com")


# ─────────────────────────────
# CORS / CSRF
# ─────────────────────────────

FRONTEND_ORIGINS_SETTING = config(
    "FRONTEND_ORIGINS",
    "https://biolab.kumasihive.com https://www.biolab.kumasihive.com",
).strip()

ALLOW_ALL_ORIGINS = FRONTEND_ORIGINS_SETTING == "*"
FRONTEND_ORIGINS = config_list(
    "FRONTEND_ORIGINS",
    default="https://biolab.kumasihive.com https://www.biolab.kumasihive.com",
)

CORS_ALLOW_CREDENTIALS = True

if ALLOW_ALL_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = FRONTEND_ORIGINS

CSRF_TRUSTED_ORIGINS = config_list(
    "CSRF_TRUSTED_ORIGINS",
    default=FRONTEND_ORIGINS_SETTING,
)

USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default=True, cast=bool)


# ─────────────────────────────
# Production security (HTTPS)
# ─────────────────────────────

if not DEBUG and not TESTING:
    SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
    SESSION_COOKIE_SAMESITE = config("SESSION_COOKIE_SAMESITE", default="Lax")

    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
    CSRF_COOKIE_SAMESITE = config("CSRF_COOKIE_SAMESITE", default="Lax")
    CSRF_COOKIE_HTTPONLY = config("CSRF_COOKIE_HTTPONLY", default=True, cast=bool)

    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=3600, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        default=True,
        cast=bool,
    )
    SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default="DENY")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ─────────────────────────────
# Applications
# ─────────────────────────────

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "corsheaders",
    "training",
    "newsletter",
    "contact",
]


# ─────────────────────────────
# Middleware
# ─────────────────────────────

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "hivebiolab.urls"

WSGI_APPLICATION = "hivebiolab.wsgi.application"


# ─────────────────────────────
# Templates
# ─────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ─────────────────────────────
# Database
# ─────────────────────────────

DATABASE_CONN_MAX_AGE = config("DATABASE_CONN_MAX_AGE", default=600, cast=int)
DATABASE_URL = config("DATABASE_URL", default="").strip()

if TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
elif DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=DATABASE_CONN_MAX_AGE,
            ssl_require=config("DATABASE_SSL_REQUIRE", default=False, cast=bool),
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="biolab"),
            "USER": config("DB_USER", default="africaosh"),
            "PASSWORD": config("DB_PASSWORD", default=""),
            "HOST": config("DB_HOST", default="db"),
            "PORT": config("DB_PORT", default="5432"),
            "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
        }
    }


# Cloudinary settings
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY", default="")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", default="")
CLOUDINARY_CONFIGURED = all(
    [CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]
)

if not DEBUG and not TESTING and not BUILDING and not CLOUDINARY_CONFIGURED:
    raise ValueError(
        "Cloudinary credentials are required in production. Set "
        "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET."
    )

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
    "SECURE": True,
}


# Static files
MEDIA_URL = (
    f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload/f_auto,q_auto/"
    if CLOUDINARY_CLOUD_NAME
    else "/media/"
)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if CLOUDINARY_CONFIGURED
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": config("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": True,
        },
        "newsletter.views": {
            "handlers": ["console"],
            "level": config("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}


# ─────────────────────────────
# Auth / i18n
# ─────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ─────────────────────────────
# Jazzmin
# ─────────────────────────────

JAZZMIN_SETTINGS = {
    "site_title": "HiveBiolab Admin",
    "site_header": "HiveBiolab",
    "site_brand": "HiveBiolab",
    "welcome_sign": "Manage newsletter, contact, and training submissions",
    "copyright": "HiveBiolab © 2025 • Trusted Biotech",
    "order_with_respect_to": ["training", "newsletter", "contact"],
    "icons": {
        "training": "fas fa-microscope",
        "newsletter": "fas fa-envelope-open-text",
        "contact": "fas fa-comments",
    },
}
