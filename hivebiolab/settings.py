import sys
from pathlib import Path

import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────
# Core security
# ─────────────────────────────

SECRET_KEY = config("SECRET_KEY", default="django-insecure-local-only")

DEBUG = config("DEBUG", default=False, cast=bool)
TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

DEFAULT_ALLOWED_HOSTS = "127.0.0.1 localhost .onrender.com .up.railway.app"
ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default=f"{DEFAULT_ALLOWED_HOSTS} api.biolab.kumasihive.com",
    )
    .replace(",", " ")
    .split()
    if host.strip()
]


# ─────────────────────────────
# CORS / CSRF
# ─────────────────────────────

FRONTEND_ORIGINS_SETTING = config(
    "FRONTEND_ORIGINS",
    "http://localhost:8080 http://127.0.0.1:8080 https://biolab.kumasihive.com",
).strip()

ALLOW_ALL_ORIGINS = FRONTEND_ORIGINS_SETTING == "*"

CORS_ALLOW_CREDENTIALS = True

if ALLOW_ALL_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        origin for origin in FRONTEND_ORIGINS_SETTING.split() if origin
    ]

CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in config(
        "CSRF_TRUSTED_ORIGINS",
        FRONTEND_ORIGINS_SETTING,
    ).split()
    if origin
]

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
# Database (host-provided SQL database, SQLite locally by default)
# ─────────────────────────────

if TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),  # MUST be 'db'
        "PORT": config("DB_PORT"),
    }
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


# ─────────────────────────────
# Static files
# ─────────────────────────────

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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
