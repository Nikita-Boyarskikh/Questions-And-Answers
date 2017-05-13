"""
Django settings for PROJECT_NAME project.
"""

import os
import socket
from config import Configuration
config = Configuration()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = config.config_get('boot', 'app')

SECRET_KEY = config.config_get('django', 'secret_key')

if socket.gethostname() == config.config_get('Admin', 'name'):
    # Локальная машина разработчика
    
    DEBUG = True
    ALLOWED_HOSTS = [
                        '127.0.0.1',
                        'localhost',
                    ]

else:
    # Продакшн-сервер
    
    DEBUG = False
    ALLOWED_HOSTS = [config.config_get('django', 'allowed_host')]

    ADMINS = [
        (config.config_get('Admin', 'name'), config.config_get('Admin', 'email')),
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.config_get('DB', 'name'),
        'USER': config.config_get('DB', 'user'),
        'PASSWORD': config.config_get('DB', 'passwd'),
        'HOST': config.config_get('DB', 'host'),
        'PORT': config.config_get('DB', 'port'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'applogfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log', PROJECT_NAME + '.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers':['applogfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'app': {
            'handlers': ['applogfile'],
            'level': 'DEBUG',
        },
    }
}

DEFAULT_FROM_EMAIL = config.config_get('Admin', 'email')
SERVER_EMAIL = config.config_get('Admin', 'email')

FIRST_DAY_OF_WEEK = 1

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = 'login'
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'uploads/')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'app', 'static/')
