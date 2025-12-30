"""
Django settings for natiportifolio project.
"""

from pathlib import Path
import dj_database_url

# --------------------------------------------------
# BASE DIR
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# CORE SETTINGS
# --------------------------------------------------

DEBUG = True

SECRET_KEY = "django-insecure-oolu!si8e#+ld159_g%$4l_i2=amj7@d^l-b!s=m5se-rbz+s*"

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = "users.User"

# --------------------------------------------------
# MEDIA
# --------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# STATIC
# --------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",

    "apps.users",
    "apps.experience",
    "apps.education",
    "apps.personal_info",
    "apps.resume",
    "apps.project",
    "apps.customer",
    "apps.customeremail",
    "apps.contactreplay",
    "apps.testimonies",
    "apps.tokenWithForgetPassword"
]

import os

RESEND_API_KEY = "re_jGP9YYSN_2HAwtqCcnd86p7urNc24736n"
DEFAULT_FROM_EMAIL = "sandbox@resend.dev"



# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be at the top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# CORS
# --------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "https://natiadmin-production.up.railway.app",
    "https://natifrontend-production.up.railway.app",
]

CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------
# URLS / WSGI
# --------------------------------------------------

ROOT_URLCONF = "natiportifolio.urls"
WSGI_APPLICATION = "natiportifolio.wsgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

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

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://postgres.myeephylmlbtoathshtm:strongpasswordgoodme@aws-1-eu-west-1.pooler.supabase.com:5432/postgres",
        conn_max_age=600,
        ssl_require=True,
    )
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# I18N
# --------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# DEFAULT AUTO FIELD
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
