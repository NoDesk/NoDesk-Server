"""
Django settings for nodesk_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, ldap, yaml, inspect, sys
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r!y0qlmz!&%f2)l8gp1lqur_79q!3drueaa_+o94@@5e@l^^j1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'nodesk_server',
    'nodesk_template',
    'nodesk_authentication',
    'nodesk_admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'nodesk_server.urls'
#TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

WSGI_APPLICATION = 'nodesk_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = 'media'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = False

CSRF_COOKIE_SECURE = True

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


#FIXME
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True





SETTINGS_YAML_FILEPATH = BASE_DIR + '/nodesk_server/settings.yaml'
with open(SETTINGS_YAML_FILEPATH) as yaml_file :
    settings_yaml = yaml.load(yaml_file.read())

"""
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(5)
"""

# Baseline configuration.
AUTH_LDAP_SERVER_URI = settings_yaml['AUTH_LDAP_SERVER_URI']['set']

AUTH_LDAP_BIND_DN = settings_yaml['AUTH_LDAP_BIND_DN']['set']
AUTH_LDAP_BIND_PASSWORD = settings_yaml['AUTH_LDAP_BIND_PASSWORD']['set']
AUTH_LDAP_USER_SEARCH = LDAPSearch(settings_yaml['AUTH_LDAP_USER_SEARCH']['set'],
    ldap.SCOPE_SUBTREE, settings_yaml['AUTH_LDAP_USER_SEARCH_FILTER']['set'])

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(settings_yaml['AUTH_LDAP_GROUP_SEARCH']['set'],
    ldap.SCOPE_SUBTREE, settings_yaml['AUTH_LDAP_GROUP_SEARCH_FILTER']['set'])
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr=settings_yaml['AUTH_LDAP_GROUP_TYPE']['set'])

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
"""
# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = "cn=nodesk,ou=groups,dc=example,dc=com"
AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=nodesk,ou=groups,dc=example,dc=com"


AUTH_LDAP_PROFILE_ATTR_MAP = {
    "employee_number": "employeeNumber"
}

#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}

#AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#}


# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
"""
