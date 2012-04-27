import os, sys
sys.path.insert(0,'/var/www/liquid/liquid/env/lib/python2.6/site-packages')
sys.path.append('/var/www/liquid/liquid')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
