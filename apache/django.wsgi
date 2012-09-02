import os, sys, logging
sys.path.insert(0,'/afs/acm.uiuc.edu/project/liquid/liquid/liquid/env/lib/python2.6/site-packages')
sys.path.append('/afs/acm.uiuc.edu/project/liquid/liquid/liquid')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

logging.critical("I hate Dylan and everyone who uses servers, and my path is %s" %sys.path)
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
