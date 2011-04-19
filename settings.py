import os
import ldap

from django_auth_ldap.config import LDAPSearch

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
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT
# This does not have to include the site's FQDN
MEDIA_URL = '/media/'

# URL prefix for admin media
# Same rules as MEDIA_URL
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Salt for hashing of passwords and such
# This needs to be changed for each individual installation
SECRET_KEY = 'Chac-8#haCa_Ra-e?-e+ucrur=gEFRasejayasaC?meMe!AC-a'

# Determine which authentication backend we'll be using
# Choices are 'CAS' and 'LDAP'
AUTHENTICATION_BACKEND = 'CAS'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

LDAP_AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CAS_AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
]

if AUTHENTICATION_BACKEND == 'CAS':
    AUTHENTICATION_BACKENDS = CAS_AUTHENTICATION_BACKENDS
    MIDDLEWARE_CLASSES.append('django_cas.middleware.CASMiddleware')
elif AUTHENTICATION_BACKEND == 'LDAP':
    AUTHENTICATION_BACKENDS = LDAP_AUTHENTICATION_BACKENDS

# Generic django.contrib.auth settings
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# LDAP authentication backend settings
# Please see http://packages.python.org/django-auth-ldap/ for documentation
AUTH_LDAP_SERVER_URI = 'ldap://'
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_SEARCH = LDAPSearch('ou=,dc=cpcc,dc=edu',
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail'
}

# CAS authentication backend settings
# Please see http://code.google.com/p/django-cas/ for documentation
CAS_VERSION = '1'
CAS_SERVER_URL = 'https://cas.cpcc.edu/cas/'
CAS_IGNORE_REFERER = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
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
    'osp.assessments',
    'osp.core',
    'osp.profiles',
    'osp.reports',
    'osp.surveys',
    'osp.visits',
)

# API credentials
API_USERNAME = 'test'
API_PASSWORD = 'test'

# Debug setting to dump tracebacks into development server console
# DEBUG_PROPAGATE_EXCEPTIONS = True

# Current year and term
CURRENT_TERM = 'SP'
CURRENT_YEAR = 2011
