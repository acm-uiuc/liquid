import os

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_BACKEND', 'django.db.backends.sqlite3'), # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DB_NAME','/liquid.db'),                      # Or path to database file if using sqlite3.
        'USER': os.environ.get('DB_USER', ''),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DB_PASSWORD',''),                  # Not used with sqlite3.
        'HOST': os.environ.get('DB_HOST', ''),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.environ.get('DB_PORT',''),                      # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)

MAILMAN_URL = os.environ.get('MAILMAN_URL', 'https://www-s.acm.uiuc.edu/mailman/')
MAILMAN_PASSWORD =  os.environ.get('MAILMAN_PASSWORD', '')
MAILMAN_ENCODING = 'us-ascii'

RESUME_STORAGE_LOCATION =  os.environ.get('RESUME_STORAGE_LOCATION', '/tmp/resume') # you should set this
LOGO_STORAGE_LOCATION =  os.environ.get('LOGO_STORAGE_LOCATION', '/tmp/resume') # you should set this
