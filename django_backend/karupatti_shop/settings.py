import os
from pathlib import Path
import dj_database_url  # for Render Postgres support

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- SECURITY --------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ("1", "true", "yes")

# -------------------- HOSTS --------------------
_render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if _render_host:
    ALLOWED_HOSTS.append(_render_host)
ALLOWED_HOSTS.append(".onrender.com")

# -------------------- APPS --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # your apps
    "accounts",
    "shops",
    "dashboard",
    "store",
    "payments",
    "wishlist",
    "orders",
    "sellers",
    "promotions",
    "chat",
    "refunds",
]

# -------------------- MIDDLEWARE --------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for static in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "karupatti_shop.urls"

# -------------------- TEMPLATES --------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wishlist.context_processors.wishlist_count",
            ],
        },
    },
]

# -------------------- DATABASE --------------------
if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------- AUTH --------------------
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTH_PASSWORD_VALIDATORS = []

# -------------------- I18N --------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------- STATIC & MEDIA --------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------- LOGIN --------------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# -------------------- CSRF --------------------
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")

# -------------------- STRIPE --------------------
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
