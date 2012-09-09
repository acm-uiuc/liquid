import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)


from intranet.models import Event
import datetime
from django.core.mail import send_mail
from textwrap import wrap
from textwrap import wrap

seven_days = datetime.timedelta(days=7)
next_week = datetime.datetime.now() + seven_days
events = Event.objects.filter(endtime__gte=datetime.datetime.now()).filter(starttime__lte=next_week).order_by('starttime')

text = "Schedule for the week:\n"

i = 1
for e in events:
   text += "%d. %s - %s\n" %(i,e.name,e.starttime.strftime('%m/%d/%y'))
   i += 1

for e in events:
   text += "\n\n========================================================================\n\n"
   
   text += "%s\n%s\n%s\n\n%s" % (e.name,e.pretty_time(),e.location,e.description)
text += "\n\n========================================================================\n\n"

print text
