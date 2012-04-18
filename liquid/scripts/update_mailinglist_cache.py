import sys,os
sys.path.append(os.path.abspath('..'),),

from django.core.management import setup_environ 
import settings 
setup_environ(settings),

from utils.django_mailman.models import List

for l in List.objects.all():
   print "Syncing %s" % l
   l.update_cache()
   
print "DONE"