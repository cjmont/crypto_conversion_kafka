"""
Base settings to build other settings files upon.
"""
import environ
from datetime import timedelta
from datetime import timedelta
from pathlib import Path
import configparser
from django.utils.translation import gettext_lazy as _

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "notbank"

env = environ.Env()
env.read_env(str(ROOT_DIR / ".env"))


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/4.0/ref/settings/#language-code
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', _('Español')),
    ('en', _('Inglés')),
    ('pt', _('Portugués')),
]
LANGUAGE_COOKIE_NAME = "notbank_language"

# https://docs.djangoproject.com/en/4.0/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
LOCALE_VERSION = 1

# https://docs.djangoproject.com/en/4.0/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#use-l10n
USE_L10N = False
# https://docs.djangoproject.com/en/4.0/ref/settings/#use-tz
USE_TZ = False

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_NAME'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# https://docs.djangoproject.com/en/4.0/ref/settings/#disable-server-side-cursors
DISABLE_SERVER_SIDE_CURSORS = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/4.0/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.forms',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_yasg',
]

LOCAL_APPS = [
    'notbank.base.apps.BaseConfig',
    'notbank.tasks',
    'notbank.transactions.apps.TransactionsConfig',
]

# https://docs.djangoproject.com/en/4.0/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'ratelimit.middleware.RatelimitMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

# https://docs.djangoproject.com/en/4.0/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = []
# https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#media-root
MEDIA_ROOT = "media"
# https://docs.djangoproject.com/en/4.0/ref/settings/#media-url
MEDIA_URL = '/external/file/s/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/4.0/ref/settings/#template-dirs
        "DIRS": [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            # https://docs.djangoproject.com/en/4.0/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/4.0/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/4.0/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# https://docs.djangoproject.com/en/4.0/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CSRF_USE_SESSIONS
CSRF_USE_SESSIONS = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/4.0/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'SAMEORIGIN'

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-failure-view
CSRF_FAILURE_VIEW = 'notbank.base.views.errors.csrf'
RATELIMIT_VIEW = 'notbank.base.views.errors.locked'

# CELERY
# -------------------------------------------------------------------------------
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/4.0/ref/settings/#email-backend
EMAIL_BACKEND = env.str(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.smtp.EmailBackend'
)

# https://docs.djangoproject.com/en/4.0/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/4.0/ref/settings/#admins
ADMINS = [
    ("""Rafael Meruane""", "rafael@notbank.app"),
    ("""Pedro Bustamante""", "pablo@notbank.app")
]
# https://docs.djangoproject.com/en/4.0/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#logging
rotating_file_handler = 'logging.handlers.RotatingFileHandler'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s.%(msecs)03d] [%(name)s:%(lineno)s] %(levelname)-12s %(message)s",
            'datefmt': "%Y/%m/%d %H:%M:%S",
        },
        'simple': {
            'format': '[%(levelname)-7s] %(asctime)s.%(msecs)03d - %(message)s',
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'app_file': {
            'level': 'DEBUG',
            'class': rotating_file_handler,
            'maxBytes': 1024 * 1024 * 1,  # 1 MB
            'backupCount': 10,
            'filename': str(ROOT_DIR / 'logs' / 'app.log'),
            'formatter': 'verbose',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': rotating_file_handler,
            'maxBytes': 1024 * 1024 * 1,  # 1 MB
            'backupCount': 10,
            'filename': str(ROOT_DIR / 'logs' / 'warning.log'),
            'formatter': 'verbose',
        },
        'kafka_consumer_file': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': rotating_file_handler,
            'maxBytes': 1024 * 1024 * 1,  # 1 MB,
            'filename': str(ROOT_DIR / 'logs' / 'kafka_consumer.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': False,
        }
    },
    'loggers': {
        'app': {
            'handlers': ['app_file'],
            'propagate': True,
        },
        'django': {
            'handlers': ['warning_file'],
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'kafka_consumer': {
            'handlers': ['kafka_consumer_file'],
            'propagate': True,
        }
    },
}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 2,
    'EXCEPTION_HANDLER': 'notbank.base.decorators.throttling_api.custom_exception_handler',
    'DEFAULT_METADATA_CLASS': 'notbank.base.meta_data.MinimalMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'notbank.base.authentication.NotBankSessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',

    ],
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': [
        # "rest_framework.permissions.IsAuthenticated",

    ]
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=500),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'secretos',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    # 'ISSUER': 'da5ccdeb-f668-4ed3-a76f-f7be1f1ba36a',
    'ISSUER': '583e87c9-871a-404d-810d-3aa124661e65',
    'JWK_URL': None,
    'LEEWAY': 0,


    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',


    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Cache config
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}


# Fee Config
config = configparser.ConfigParser()
config.read('/home/user/backend/config/config.cfg')
FEE_CONFIG = config['config']['fee']

# Task Config (celery)
DEPOSIT = 'deposit'
GET_FEE = 'get_fee'

# config cron job delete execute conversion previous
DATE = timedelta(hours=2)

KAFKA_CELERY_GROUP = 'some'
# TODO: change to notbank-sync or similar
KAFKA_NOTBANK_SYNC_TOPIC = 'notbank-sync'
KAFKA_BALANCE_MANAGER_TASK_TOPIC = 'notbank-balance-manager'
KAFKA_BALANCE_MANAGER_STATUS_TOPIC = 'balance-manager-status'
# TODO: change to real one before deployment
KAFKA_USER_DATA_TOPIC = 'notbank-user-data'
KAFKA_PUSH_TOPIC = 'notbank-push'  # TODO: change to real one before deployment
KAFKA_QUOTE_SERVICE_NANOBANCO_QUOTE = 'nanobanco-quote'
# TODO: change to real one before deployment
KAFKA_QUOTE_SERVICE_TOPIC = 'quote-service'
# TODO: change to the real one before deployment
KAFKA_QUOTE_SERVICE_RESULT_TOPIC = 'quote-service-result'
# TODO: change to the real one before deployment
KAFKA_QUOTE_LISTENER_TOPIC = 'quote-listener'
KAFKA_NOTIFY_TRANSACTION_TOPIC = 'notify-transaction'
KAFKA_TOPIC_GET_FEE = 'get-fee'
KAFKA_RETURN_FEE_TOPIC = 'return-fee'
KAFKA_NOTBANK_APP_SOCKET_TOPIC = 'notbank-app-socket'


# for docker, the server is broker:29092
KAFKA_NOTBANK_SERVERS = ['broker:29092']
