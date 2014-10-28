from defaults import *

DEBUG = True


INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)

STATIC_ROOT = 'static-dev/'

STATIC_URL = '/static-dev/'

MEDIA_ROOT = 'media-dev/'

MEDIA_URL = '/media-dev/'
