import os, sys
import site
site.addsitedir('/var/www/liquid/liquid/env/lib/python2.6/site-packages')
sys.path.append("/var/www")
sys.path.append("/var/www/liquid")
sys.path.append("/var/www/liquid/liquid")
os.environ['DJANGO_SETTINGS_MODULE'] = 'liquid.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
