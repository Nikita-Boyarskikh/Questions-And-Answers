# pylint: disable=invalid-name
import multiprocessing

import os
import sys

from config import Configuration
config = Configuration()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR))

# Global settings
ROOT_DIR = config.config_get('boot', 'root_dir')
PROJECT_NAME = config.config_get('boot', 'app')

chdir = os.path.join(ROOT_DIR, PROJECT_NAME)

# Logging
accesslog = os.path.join(ROOT_DIR, PROJECT_NAME, 'log/gaccess.log')
errorlog = os.path.join(ROOT_DIR, PROJECT_NAME, 'log/gerror.log')
loglevel = 'debug'
access_log_format = '%({X-Real-Host}i)s [%(t)s] %(r)s %(s)s %(b)s %(f)s %(a)s %(D)s'
capture_output = True

# Configuration server
workers = multiprocessing.cpu_count() * 2 + 1
treads = 1
bind = ['unix:' + os.path.join(ROOT_DIR, PROJECT_NAME + '.sock')]
daemon = True

# Private settings
user = 'www-data'
group = 'www-data'

reload = True
config = None
