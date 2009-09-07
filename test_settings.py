# Test Django Settings

from settings import *

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.remove('django.contrib.csrf.middleware.CsrfViewMiddleware')
MIDDLEWARE_CLASSES.remove('django.contrib.csrf.middleware.CsrfResponseMiddleware')