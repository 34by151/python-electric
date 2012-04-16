import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = PROJECT_PATH.split(os.sep)[-1]

DEBUG = False

TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = '127.0.0.1'

ADMINS = (
    ('name', 'email@email.com'),
)

MANAGERS = ADMINS

#PRODUCTION SETTINGS... USE LOCAL_SETTINGS.PY FOR YOUR LOCAL MACHINE...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = os.path.join (PROJECT_PATH, 'media')  # new settings in django 1.4

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
STATIC_URL = '/media/' # new settings in django 1.4

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l%)e7f$#tom$@)p_yd3y(djm$@)p_yd3y(dj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.i18n',
	'django.core.context_processors.debug',
#	'python_electric.tools.context_processors.menu',
	'python_electric.tools.context_processors.settings',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = "%s.urls" % PROJECT_DIR
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, "templates"),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'python_electric.apps.electric',


)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True

CONTACT_LIST = ["email@gmail.com", "email@email.com"]


###############################

# import local settings overriding the defaults
try:
    from local_settings import *
except ImportError:
    print "Using production settings"
else:
    print "Using DEVELOPMENT settings"