import os
import sys
from pathlib import Path
from urllib.parse import quote

import dj_database_url
from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def env_csv(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)

    return [item.strip() for item in value.split(',') if item.strip()]


def is_static_cmd() -> bool:
    command = ' '.join(sys.argv).lower()

    return 'collectstatic' in command or 'findstatic' in command


RUNNING_STATIC_COMMAND = is_static_cmd()
IS_TESTING = 'test' in sys.argv


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = env_bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = env_csv(
    'DJANGO_ALLOWED_HOSTS',
    '127.0.0.1,localhost,.run.app',
)

CSRF_TRUSTED_ORIGINS = env_csv(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    'http://127.0.0.1,http://localhost,https://*.run.app',
)

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'locations',
    'subscriptions',
    'rest_framework',
    'weather',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]


DATABASE_URL = os.getenv('DATABASE_URL')
INSTANCE_CONNECTION_NAME = os.getenv('INSTANCE_CONNECTION_NAME')

DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

ALLOW_NO_DB = env_bool('DJANGO_ALLOW_NO_DB', False)

if INSTANCE_CONNECTION_NAME and DB_USER and DB_NAME:
    socket_dir = f'/cloudsql/{INSTANCE_CONNECTION_NAME}'
    assembled_url = (
        f'postgresql://{DB_USER}:{quote(DB_PASSWORD)}@/{DB_NAME}'
        f'?host={socket_dir}'
    )

    DATABASES = {
        'default': dj_database_url.parse(
            assembled_url,
            conn_max_age=int(os.getenv('DB_CONN_MAX_AGE', '120')),
            ssl_require=False,
        )
    }

elif DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=int(os.getenv('DB_CONN_MAX_AGE', '120')),
            ssl_require=False,
        )
    }

else:
    if RUNNING_STATIC_COMMAND or ALLOW_NO_DB or IS_TESTING:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
}


if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "update-weather-every-30-minutes": {
        "task": "weather.tasks.update_weather_for_all_cities",
        "schedule": 1800.0,
    },
    "send-due-notifications-every-5-minutes": {
        "task": "subscriptions.tasks.send_due_notifications",
        "schedule": 300.0,
    },
}
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
