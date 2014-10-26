from defaults import *

DEBUG = True


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobs_manager_app',
    'debug_toolbar',
)

STATIC_ROOT = 'static-dev/'

STATIC_URL = '/static-dev/'

MEDIA_ROOT = 'static-dev/media-dev/'

MEDIA_URL = '/static-dev/media-dev/'
