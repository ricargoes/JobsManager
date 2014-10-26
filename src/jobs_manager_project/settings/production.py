from defaults import *

DEBUG = False


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobs_manager_app',
)


STATIC_ROOT = 'static/'

STATIC_URL = '/static/'

MEDIA_ROOT = 'static/media/'

MEDIA_URL = '/static/media/'
