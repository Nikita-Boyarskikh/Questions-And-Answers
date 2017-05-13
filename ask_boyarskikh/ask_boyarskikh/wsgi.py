"""
WSGI config for questandansw project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from config import Configuration
config = Configuration()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config.config_get('boot', 'app') + '.settings')

application = get_wsgi_application()
