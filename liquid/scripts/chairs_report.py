import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)


from intranet.models import Group

groups = Group.objects.filter(status='active')

for g in groups:
   chairs = g.members.filter(groupmember__is_chair=True)
   chair_netids = []
   for c in chairs:
      chair_netids.append(c.full_name_and_netid())
   print "%s: %s" %(g.name,", ".join(chair_netids))
