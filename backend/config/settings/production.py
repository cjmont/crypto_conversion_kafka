from config.settings.base import *
from config.settings.base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["notbank.app"])

LOCAL_IPS = env.list("LOCAL_IPS")
DOMAIN = env.str('DOMAIN')
SITE_URL = env.str('SITE_URL')

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DJANGO_CONN_MAX_AGE", default=60)  # noqa F405

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': env.list('DJANGO_MEMCACHED_LOCATION'),
    }
}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("DJANGO_HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/4.0/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-ht625cz"
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-xmkg578"
# https://docs.djangoproject.com/en/4.0/topics/security/#ssl-https
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = 518400
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/4.0/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
# https://docs.djangoproject.com/en/4.0/ref/settings/#session-cookie-domain
SESSION_COOKIE_DOMAIN = env.str('DJANGO_SESSION_COOKIE_DOMAIN')
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SESSION_COOKIE_SAMESITE
SESSION_COOKIE_SAMESITE = 'Lax'
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CSRF_COOKIE_SAMESITE
CSRF_COOKIE_SAMESITE = 'Lax'

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#static-url
STATIC_URL = f"{SITE_URL}/static/"

# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "storages.backends.sftpstorage.SFTPStorage"
SFTP_STORAGE_HOST = env.str("SFTP_STORAGE_HOSTNAME")
SFTP_STORAGE_ROOT = "/mnt/raid/storage/media/"
SFTP_STORAGE_PARAMS = {
    'port': env.str("SFTP_STORAGE_PORT"),
    'username': env.str("SFTP_STORAGE_USERNAME"),
    'passphrase': env.str("SFTP_STORAGE_PASSPHRASE"),
    'key_filename': f"{env.str('HOME')}/.ssh/{env.str('SFTP_STORAGE_KEY_NAME')}",
    'allow_agent': False,
    'look_for_keys': False,
}

# SESSION
# ------------------------------------------------------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="NotBank <noreply@notbank.app>"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env.str(
    'DJANGO_EMAIL_SUBJECT_PREFIX', default='[NotBank]')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = env.str('SENDGRID_HOST')
EMAIL_HOST_USER = env.str('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = env.str('SENDGRID_PASSWORD')