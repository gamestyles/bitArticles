"""
Django settings for bitArticles project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from os.path import join, exists

try:
    from configs import * # noqa
except ImportError:
    raise ImportError('There is no config file in the root directory.')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = django_settings.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = django_settings.get('DEBUG', False)

ALLOWED_HOSTS = django_settings.get('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])

CSRF_TRUSTED_ORIGINS = django_settings.get('CSRF_TRUSTED_ORIGINS', ['https://localhost'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'coreapi',
    'drf_yasg',
    'api',
    'article',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middlewares.UserFingerprintMiddleware',
]

ROOT_URLCONF = 'bitArticles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bitArticles.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": db.get('POSTGRES_DB_NAME', 'bitpin'),
        "USER": db.get('POSTGRES_DB_USER', 'postgres'),
        "PASSWORD": db.get('POSTGRES_DB_PASSWORD', '123456'),
        "HOST": db.get('POSTGRES_DB_HOST', 'localhost'),
        "PORT": db.get('POSTGRES_DB_PORT', '5432'),
        "CONN_MAX_AGE": db.get('CONN_MAX_AGE', 0),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_config.get('redis_url'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'common.permissions.IsFingerprintAvailable',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (

    ),
    'DEFAULT_FILTER_BACKENDS': [

    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': drf.get('PAGE_SIZE', 10)
}

if not exists('logs'):
    from os import makedirs
    makedirs('logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': django_settings.get('LOG_DIR_NAME'),
            'maxBytes': django_settings.get("LOGGING_FILE_MAX_BYTES", 1024 * 1024 * 5),
            'backupCount': django_settings.get("LOGGING_FILE_BACKUP_COUNT", 5),
            'formatter': 'standard',
        },
        'celery': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': celery_confs.get('CELERY_LOG_DIR_NAME'),
            'maxBytes': celery_confs.get("CELERY_LOGGING_FILE_MAX_BYTES", 1024 * 1024 * 5),
            'backupCount': celery_confs.get("CELERY_LOGGING_FILE_BACKUP_COUNT", 5),
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
        },
        'celery': {
            'handlers': ['celery', 'console'],
            'level': celery_confs.get('CELERY_LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO'),
            'propagate': celery_confs.get('CELERY_LOG_PROPAGATE', True)
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': django_settings.get('LOGGING_LEVEL', 'DEBUG' if DEBUG else 'INFO'),
    },
}


# Celery
CELERY_BROKER_URL = celery_confs.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = celery_confs.get('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = celery_confs.get('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = celery_confs.get('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = celery_confs.get('CELERY_RESULT_SERIALIZER')
CELERY_TIMEZONE = celery_confs.get('CELERY_TIMEZONE')
CELERY_WORKER_CONCURRENCY = celery_confs.get('CELERY_WORKER_CONCURRENCY')
CELERY_WORKER_SEND_TASK_EVENTS = celery_confs.get('CELERY_WORKER_SEND_TASK_EVENTS')
CELERY_TASK_SEND_SENT_EVENT = celery_confs.get('CELERY_TASK_SEND_SENT_EVENT')
HEALTHCHECK_CELERY_QUEUE_TIMEOUT = celery_confs.get('HEALTHCHECK_CELERY_QUEUE_TIMEOUT', 3)


# Additional Configs
API_VERSION = api.get('API_VERSION', 'v1')
API_PREFIX = "api/" + API_VERSION + "/"

# swagger
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'API-KEY': {
        'type': 'fingerprintID',
        'name': 'X-FINGERPRINT-ID',
        'in': 'header'
      }
   }
}
