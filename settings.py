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
AUTHENTICATION_BACKEND = 'LDAP'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'osp.core.middleware.http.Http403Middleware',
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
AUTH_PROFILE_MODULE = 'core.UserProfile'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# LDAP authentication backend settings
# Please see http://packages.python.org/django-auth-ldap/ for documentation
AUTH_LDAP_SERVER_URI = 'ldap://'
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''
AUTH_LDAP_USER_SEARCH = LDAPSearch('ou=,dc=,dc=edu',
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail'
}

# CAS authentication backend settings
# Please see http://code.google.com/p/django-cas/ for documentation
CAS_VERSION = '1'
CAS_SERVER_URL = 'https://'
CAS_IGNORE_REFERER = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'osp.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'osp.core.context_processors.base_template',
    'osp.core.context_processors.classes',
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
    'osp.rosters',
    'osp.surveys',
    'osp.visits',
)

# API credentials. This should be a randomly generated username and password.
API_USERNAME = '2rUph4cu'
API_PASSWORD = 'phayekE3'

# Current/previous year and term
CURRENT_TERM = 'SP'
CURRENT_YEAR = 2011

PREVIOUS_TERM = 'FA'
PREVIOUS_YEAR = 2010

# Mail server settings
EMAIL_HOST = ''
EMAIL_PORT = 25

# Customize enrollment statuses here. Be sure to leave the "Active"
# status, as certain application functions depend on it.
ENROLLMENT_STATUS_CHOICES = (
    ('A', 'Active'),
    ('DFNP', 'Dropped for Non-Payment'),
    ('DBS', 'Dropped by Student'),
    ('DBI', 'Dropped by Instructor'),
    ('C', 'Complete'),
)

ENROLLMENT_GRADE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('F', 'F'),
    ('W', 'W'),
    ('I', 'I'),
    ('N/A', 'N/A'),
)
VISIT_CAMPUS_CHOICES = (
    ('CE', 'Central'),
    ('LV', 'Levine'),
    ('CA', 'Cato'),
    ('NO', 'North'),
    ('HP', 'Harper'),
    ('HA', 'Harris'),
)
VISIT_CONTACT_TYPE_CHOICES = (
    ('IN', 'In Person'),
    ('EM', 'Email'),
    ('TE', 'Telephone'),
    ('ON', 'Online'),
    ('GR', 'Group Session'),
)
VISIT_REASON_CHOICES = (
    ('NEWA', 'New Student Admission'),
    ('ACAD', 'Academic Advising'),
    ('CNSL', 'Counseling'),
    ('PECO', 'Personal Counseling'),
    ('ERLY', 'Early Alert Referral'),
    ('GRAD', 'Graduation Assessment Review'),
    ('CACO', 'Career Counseling'),
    ('WORK', 'Workshops, Class Presentations'),
    ('A111', 'ACA 111'),
    ('A118', 'ACA 118'),
    ('COCO', 'College Connection'),
    ('ERLC', 'Early Alert Counseling'),
    ('DAIN', 'Disability Intake'),
    ('DACO', 'Disability Counseling'),
    ('FAAD', 'Faculty Advising'),
    ('ACWA', 'Academic Warning'),
    ('ACPR', 'Academic Probation'),
    ('1ACS', 'First Academic Suspension'),
    ('FACS', 'Final Academic Suspension'),
)
VISIT_DEPARTMENT_CHOICES = (
    ('AA', 'Academic Advising'),
    ('CS', 'Career Services'),
    ('CO', 'Counseling Services'),
    ('DS', 'Disability Services'),
    ('FA', 'Faculty'),
    ('SS', 'Student Success Center'),
    ('TE', 'Transcript Evaluation'),
    ('TR', 'Transfer Resource Center'),
    ('AS', 'Advising / Student Success Center'),
    ('DC', 'Disability Counseling'),
    ('VR', 'Veterans Resource Center'),
)
VISIT_CAREER_SERVICES_OUTCOME_CHOICES = (
    ('NC', 'No Contact'),
    ('EM', 'Email'),
    ('PH', 'Phone'),
    ('SA', 'Scheduled Appointment with Career Services'),
    ('NS', 'No Show for Appointment'),
    ('TC', 'Took Career Assessment(s)'),
    ('MC', 'Met with Career Counselor'),
    ('CD', 'Career Decision in Process'),
    ('CP', 'Career and Program Decision Completed'),
    ('RP', 'Referred for Program Update'),
    ('PU', 'Program Updated'),
)
