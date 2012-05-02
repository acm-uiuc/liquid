import sys,os
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)


from django.core.mail import send_mail
from intranet.models import Member, Group
from vote.models import Vote
from django.utils.crypto import get_random_string


top4 = Group.objects.get(name="Top4")
members = top4.members.all()

poll=int(raw_input("Poll id: "))

for m in members:
   key = get_random_string(length=32,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
   v = Vote(user=m,key=key,poll=poll)
   v.save()
   email = """Dear %s,
   
   You are recieving this email because....
   
   To vote for this constitution please visit: http://acm.uiuc.edu/vote/%s/%s
   
   Thanks,
   Reed La Botz
   Secretary, ACM@UIUC
   """ % (v.user.full_name(),v.user.username,v.key)
   
   try:
      send_mail('ACM Constitution', email, 'Reed La Botz<labotz1@illinois.edu>',[m.email], fail_silently=False)
      print "Email sent to %s" % m.full_name()
   except Exception as inst:
      print "Error sending email to %s" % m.full_name()
      print inst
