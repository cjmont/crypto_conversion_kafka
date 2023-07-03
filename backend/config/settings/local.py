from config.settings.base import *
from config.settings.base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="onMH3PPHV^JOaJ97$dww$%9vV7aE78yf",
)
# https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts
LOCAL_IPS = env.list(
    "LOCAL_IPS", default=[
        "localhost", "0.0.0.0", "127.0.0.1"
    ]
)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=LOCAL_IPS)

# PLATFORM
# ------------------------------------------------------------------------------
DOMAIN = '127.0.0.1:8000'
SITE_URL = 'http://127.0.0.1:8000'

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
    # this cache backend will be used by django-debug-panel
    'debug-panel': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/debug-panel-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 200
        }
    }
}

# https://docs.djangoproject.com/en/4.0/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#session-cookie-domain
SESSION_COOKIE_DOMAIN = "127.0.0.1"

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

KAFKA_CELERY_KEY= "abaababaababaac" # TODO poner una key generada válidamente