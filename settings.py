import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Administrators who should receive Python tracebacks for errors
ADMINS = (
    ('Jon Mooring', 'jon.mooring@cpcc.edu'),
)

MANAGERS = ADMINS

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'osp',
        'USER': 'osp',
        'PASSWORD': 'osp',
        'HOST': '',
        'PORT': '',
    }
}

# Server time zone
TIME_ZONE = 'America/New_York'

# django.contrib.site ID
SITE_ID = 1

# i18n and l10n
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Absolute path to the directory that holds uploaded media
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT
# This does not have to include the site's FQDN
MEDIA_URL = '/media/'

# URL prefix for admin media
# Same rules as MEDIA_URL
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Salt for hashing of passwords and such
# This needs to be changed for each individual installation
SECRET_KEY = 'Chac-8#haCa_Ra-e?-e+ucrur=gEFRasejayasaC?meMe!AC-a'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'osp.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'osp.core',
    'osp.surveys',
    'osp.assessments',
    'osp.notes',
    'osp.reports',
)
