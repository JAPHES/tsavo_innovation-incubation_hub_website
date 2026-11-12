"""Django settings for the Tsavo Innovation & Incubation Hub website."""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


IS_VERCEL = env_bool("VERCEL", False)
DEBUG = env_bool("DJANGO_DEBUG", not IS_VERCEL)
if IS_VERCEL and DEBUG:
    raise ImproperlyConfigured("DJANGO_DEBUG must be False on Vercel deployments.")
SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-development-only-change-me"
    else:
        raise ImproperlyConfigured("SECRET_KEY must be set when DEBUG=False.")

vercel_hosts = [os.getenv("VERCEL_URL", ""), os.getenv("VERCEL_PROJECT_PRODUCTION_URL", "")]
default_hosts = ",".join(["127.0.0.1", "localhost", *[host for host in vercel_hosts if host]])
default_csrf_origins = ""
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", default_hosts).split(",") if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", default_csrf_origins).split(",") if origin.strip()]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "django.contrib.sitemaps", "apps.core.apps.CoreConfig", "apps.services.apps.ServicesConfig",
    "apps.projects.apps.ProjectsConfig", "apps.team.apps.TeamConfig",
    "apps.events.apps.EventsConfig", "apps.contact.apps.ContactConfig",
    "axes", "django_mfa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django_mfa.middleware.MfaMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tsavo_hub.security.PublicContentSecurityPolicyMiddleware", "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"
AXES_ONLY_ADMIN_SITE = True
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]
AXES_CLIENT_IP_CALLABLE = "tsavo_hub.security.trusted_client_ip"
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_RESET_COOLOFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_ACCESS_FAILURE_LOG_PER_USER_LIMIT = 100
AXES_NEVER_LOCKOUT_GET = True
AXES_ENABLE_RETRY_AFTER_HEADER = True

MFA_FACTORS = ["totp", "recovery_codes"]
MFA_ISSUER_NAME = "Tsavo Innovation & Incubation Hub"
MFA_PROTECT_ADMIN = True
MFA_BASE_TEMPLATE = "admin/mfa_base.html"
MFA_EXEMPT_PATHS = ["/sign-out/"]
MFA_RATE_LIMIT_BACKEND = "database"
MFA_RATE_LIMIT_FAIL_OPEN = False
MFA_CLIENT_IP_RESOLVER = "tsavo_hub.security.trusted_client_ip"

ROOT_URLCONF = "tsavo_hub.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages", "apps.core.context_processors.site_context",
    ]},
}]
WSGI_APPLICATION = "tsavo_hub.wsgi.application"

DATABASES = {"default": dj_database_url.config(
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600 if not DEBUG else 0,
    conn_health_checks=not DEBUG,
)}
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = env_bool("DISABLE_SERVER_SIDE_CURSORS", IS_VERCEL)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# A remembered admin login expires after one working day, not Django's 14-day default.
SESSION_COOKIE_AGE = 8 * 60 * 60

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
BLOB_READ_WRITE_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN", "")
if BLOB_READ_WRITE_TOKEN:
    STORAGES["default"] = {"BACKEND": "tsavo_hub.storage.VercelBlobStorage"}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "web@localhost")
CONTACT_NOTIFICATION_EMAIL = os.getenv("CONTACT_NOTIFICATION_EMAIL", "tiih@ttu.ac.ke")

vercel_origin_host = os.getenv("VERCEL_PROJECT_PRODUCTION_URL") or os.getenv("VERCEL_URL", "")
SITE_ORIGIN = os.getenv("SITE_ORIGIN", f"https://{vercel_origin_host}" if vercel_origin_host else "").rstrip("/")
CONTACT_RATE_LIMIT = int(os.getenv("CONTACT_RATE_LIMIT", "5"))
PROJECT_DETAILS_ENABLED = env_bool("PROJECT_DETAILS_ENABLED", False)
MAX_IMAGE_UPLOAD_SIZE = int(os.getenv("MAX_IMAGE_UPLOAD_SIZE", str(5 * 1024 * 1024)))

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", not DEBUG)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", not DEBUG)
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
