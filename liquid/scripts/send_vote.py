import sys,os,time
sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ 
import settings 
setup_environ(settings)


from django.core.mail import send_mail
from intranet.models import Member, Group
from vote.models import Vote
from django.utils.crypto import get_random_string


members = Member.objects.all()

poll=int(raw_input("Poll id: "))

for m in members:
   key = get_random_string(length=32,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
   v = Vote(user=m,key=key,poll=poll)
   v.save()
   email = """Dear %s,

We've been working on updating the ACM constitution to better reflect how we currently operate and to incorporate some new ideas. Under the guidelines of the current constitution, amendments have to be approved by our executive council and then by our membership. The proposed changes have been approved by exec, so now we're sending it out to you so that you can take a look at it and vote on it. 

Here's a link to the new constitution https://www-s.acm.uiuc.edu/confluence/display/general/ACM+Constitution+-+Draft; there's also a summary of the changes below. 

Amendment highlights:
-Classifying members as undergraduate members, graduate members, faculty/staff members, active members and alumni members
-Updating duties of officers
-Not allowing officers to run for a second consecutive term in the same position 
-Making it possible for individuals to get funding for a project in addition to SIGs
-Defining what committees are and how they're run
-Requiring 5 members to start a SIG
-Allowing for a designated proxy for SIG leadership at exec meetings 
-Defining the requirements of an active SIG and what happens when they're no longer active 

The vote is open for the next week, and can be accessed through this link: http://acm.uiuc.edu/vote/%s/%s. 

If you have any questions, feel free to email top4@acm.uiuc.edu. 

Thanks!

Brianna Birman
ACM@UIUC Chair""" % (v.user.full_name(),v.user.username,v.key)
   
   try:
      send_mail('Vote on ACM constitution', email, 'Brianna Birman<top4@acm.uiuc.edu>',[m.email], fail_silently=False)
      print "Email sent to %s" % m.full_name()
   except Exception as inst:
      print "Error sending email to %s" % m.full_name()
      print inst
   time.sleep(.05)
