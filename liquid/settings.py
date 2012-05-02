import os
import django
# Django settings for acm project.
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Liquid Admins', 'liquid@acm.uiuc.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'database'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
#    'default': {
#        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'acm',                      # Or path to database file if using sqlite3.
#        'USER': 'root',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-1z=(%v80hj+b087v^f_ca60l1uk^1a4g7woj8u-juthol8=x7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'abouta',
    'banks',
    'cal',

    'intranet',
    'intranet.event_manager',
    'intranet.group_manager',
    'intranet.job_manager',
    'intranet.member_database',
    'intranet.chroma',

    'sigs',
    
    'vote',


    'bootstrapform',
    'utils.django_mailman',
    'south',
  )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Append slashes if not found in URLConf
APPEND_SLASH = True

SERVE_STATIC = True


## LDAP STUFF ## should be in local_settings for security

#AD_DNS_NAME='your-ldap-server.com'
# If using non-SSL use these
#AD_LDAP_PORT=389
#AD_LDAP_URL='ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
# If using SSL use these:
#AD_LDAP_PORT=636
#AD_LDAP_URL='ldaps://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
#AD_SEARCH_DN='dc=mygroup,dc=net,dc=com'
#AD_NT4_DOMAIN='YOURDOMAIN'
#AD_SEARCH_FIELDS= ['mail','givenName','sn','sAMAccountName','memberOf']
#AD_MEMBERSHIP_REQ=['Group_Required','Alternative_Group']
#AD_CERT_FILE='/path/to/your/cert.txt'
#AD_DEBUG=True
#AD_DEBUG_FILE='/path/to/writable/log/file/ldap.debug'
AUTHENTICATION_BACKENDS = ('utils.ldapauth.ActiveDirectoryGroupMembershipSSLBackend',)

CUSTOM_USER_MODEL = 'intranet.member_manager.models.Member'

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.contrib.messages.context_processors.messages")

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'utils.loginmiddleware.RequireLoginMiddleware',
 'utils.http.Http403Middleware',)
 
LOGIN_REQUIRED_URLS = (
  r'/intranet/(.*)$',
)


# ldap things
AD_DNS_NAME= 'ldap1.acm.uiuc.edu'
# If using non-SSL use these
AD_LDAP_PORT=389
AD_LDAP_URL='ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
# If using SSL use these:
#AD_LDAP_PORT=636
#AD_LDAP_URL='ldaps://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)
AD_SEARCH_DN='dc=acm,dc=uiuc,dc=edu'
AD_NT4_DOMAIN='ACM.UIUC.EDU'
AD_SEARCH_FIELDS= ['givenName','sn','uid']
AD_MEMBERSHIP_REQ=['acm.users']
AD_CERT_FILE='/path/to/your/cert.txt'
AD_DEBUG=True
AD_DEBUG_FILE='/var/log/apache2/ldap.debug'

try:
  from local_settings import *
except ImportError, exp:
  pass
  

if SERVE_STATIC:
  INSTALLED_APPS += ('django.contrib.staticfiles',)
