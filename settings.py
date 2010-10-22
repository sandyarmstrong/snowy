# STOP STOP STOP STOP STOP STOP STOP STOP
# Every time you edit settings.py directly, $DEITY kills a kitten.
#
# Please, think of the kittens.
#
# Seriously now, edit local_settings.py for any site specific settings.
# STOP STOP STOP STOP STOP STOP STOP STOP

import os.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

RECAPTCHA_ENABLED = False
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

URI_SCHEME = 'http'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('zh_CN', 'Chinese (Simplified)'),
    ('en', 'English'),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2n17f16%vd2^x=q6&7a)s*$ft@vtp572-4+)@6spfxpe^^7^j6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'snowy.core.context_processors.current_site',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfViewMiddleware',
    'django.contrib.csrf.middleware.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'snowy.accounts.middleware.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'reversion.middleware.RevisionMiddleware',
    'recaptcha_django.middleware.ReCaptchaMiddleware',
    'pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'snowy.urls'

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "templates"),
]

# Add the lib/ directory to the path for external apps
EXTERNAL_APPS_PATH = os.path.join(PROJECT_ROOT, "lib")

import sys
sys.path.append(EXTERNAL_APPS_PATH)

INSTALLED_APPS = [
    # Local apps
    'core',
    'api',
    'accounts',
    'django_openid_auth',
    'notes',

    # System apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.messages',

    # External apps
    'registration',
    'south',
    #'reversion',
    'gravatar',
    'autoslug',
    'piston',
    'pagination',
]

# Maximum number of notes to show on the notes_detail list.
SNOWY_LIST_MAX_NOTES = 18

ACCOUNT_ACTIVATION_DAYS = 15

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# we create users ourselves after they have given more details
OPENID_CREATE_USERS = False

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/openid/login/'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                           'django_openid_auth.auth.OpenIDBackend',
                           #'socialauth.auth_backends.TwitterBackend',
                           #'socialauth.auth_backends.FacebookBackend',
                           )


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
