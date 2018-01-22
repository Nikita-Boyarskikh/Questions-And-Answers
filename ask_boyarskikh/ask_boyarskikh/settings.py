"""
Django settings for PROJECT_NAME project.
"""

import os
import socket

from django.utils.translation import ugettext_lazy as _
from config import Configuration
CFG = Configuration()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = CFG.config_get('boot', 'app')

SECRET_KEY = CFG.config_get('django', 'secret_key')

if socket.gethostname() == CFG.config_get('Admin', 'name'):
    # Локальная машина разработчика

    DEBUG = True
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
    ]

else:
    # Продакшн-сервер

    DEBUG = False
    ALLOWED_HOSTS = [CFG.config_get('django', 'allowed_host')]

    ADMINS = [
        (CFG.config_get('Admin', 'name'), CFG.config_get('Admin', 'email')),
    ]


AUTH_USER_MODEL = 'app.Profile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # custom
    'channels',

    # own
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates'),
        ],
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

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

DATABASES = {
    'default': {
        'NAME': CFG.config_get('DB', 'name'),
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': CFG.config_get('DB', 'mycnf_path'),
            'init_command': 'SET sql_mode=STRICT_ALL_TABLES',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:' + os.path.join(BASE_DIR, 'memcached.sock'),
        'TIMEOUT': 30 * 60,
    }
}

CACHE_MIDDLEWARE_SECONDS = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log', PROJECT_NAME + '.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['applogfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'app': {
            'handlers': ['applogfile'],
            'level': 'DEBUG',
        },
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'ask_boyarskikh.routing.channel_routing',
    }
}

DEFAULT_FROM_EMAIL = CFG.config_get('Admin', 'email')
SERVER_EMAIL = CFG.config_get('boot', 'app') + '@' + socket.gethostname()

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

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

FIRST_DAY_OF_WEEK = 1
LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'app', 'locale'),
)

USE_TZ = True
TIME_ZONE = 'Europe/Moscow'

USE_X_FORWARDED_HOST = True

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/user'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'uploads')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'app', 'static')
