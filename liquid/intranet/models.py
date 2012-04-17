from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import settings
import datetime
import ldap


# Create your models here.
MEMBER_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))

GROUP_TYPE_CHOICES = (('S', 'SIG'),('C', 'Committee'),('O','Other'))
GROUP_DAY_CHOICES = ((0,'Sunday'),(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'))
GROUP_MEMBER_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))
GROUP_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))

EVENT_TYPE_CHOICES = (('a','ACM General'),('g','Group'),('d','Department'))

EMAIL_STATUS_CHOICES = (('defer','Defer'),('approve','Approve'),('discard','Discard'))

class Member(User):
   uin = models.CharField(max_length=9,null=True)
   left_uiuc = models.DateField(null=True,blank=True)
   status = models.CharField(max_length=255,choices=MEMBER_STATUS_CHOICES,default='active')

   def full_name(self):
      return self.first_name + " " + self.last_name
      
   def full_name_and_netid(self):
      return self.full_name() + " (" + self.username + ")"
      
   def is_group_admin(self,group):
      user_groups = self.groupmember_set.filter(is_admin__exact=True).filter(group__name__iexact=group)
      return len(user_groups) > 0
      
   def is_top4(self):
      return self.is_group_admin('Top4')
      
   def is_admin(self):
      return len(self.groupmember_set.filter(is_admin__exact=True)) > 0
   
   def __unicode__(self):
      return self.full_name()
#change username to netid in member
Member._meta.get_field('username').verbose_name = 'netid'

@receiver(pre_save, sender=Member)
def new_member(sender, **kwargs):
   user = kwargs['instance']
   if not user.id:
      l = ldap.initialize('ldap://ldap.uiuc.edu')
      u = l.search_s('ou=people,dc=uiuc,dc=edu',ldap.SCOPE_SUBTREE,'uid=%s'%user.username)
      try:
         user.last_name = u[0][1]['sn'][0]
         user.first_name = u[0][1]['givenName'][0]
      except IndexError:
         raise ValueError('Bad Netid', 'Not a valid netid')
      user.email = username + "@illinois.edu"
      ## perform other first save operations (caffiene)

class Group(models.Model):
   type = models.CharField(max_length=1, choices=GROUP_TYPE_CHOICES)
   name = models.CharField(max_length=30)
   members = models.ManyToManyField(Member, through="GroupMember",blank=True)
   date_formed = models.DateField()
   description = models.TextField()
   meeting_time = models.TimeField(null=True,blank=True)
   meeting_day = models.IntegerField(null=True,blank=True,choices=GROUP_DAY_CHOICES)
   meeting_location = models.CharField(max_length=255,null=True,blank=True)
   url = models.URLField(null=True,blank=True)
   logo = models.URLField(null=True,blank=True)
   mailing_list = models.EmailField(max_length=60)
   status = models.CharField(max_length=255,choices=GROUP_STATUS_CHOICES,default='active')

   def __unicode__(self):
      return self.name

   def chairs(self):
      return self.members.filter(groupmember__is_chair=True)

   def active_members(self):
      return self.members.filter(groupmember__status='active')

class GroupMember(models.Model):
   class Meta:
      unique_together = ('group','member')
   group = models.ForeignKey(Group,related_name='membership')
   member = models.ForeignKey(Member)
   date_joined = models.DateField(default=datetime.date.today)
   is_chair = models.BooleanField(default=False)
   is_admin = models.BooleanField(default=False)
   status = models.CharField(max_length=255,choices=GROUP_MEMBER_STATUS_CHOICES,default='active')
   
@receiver(pre_save, sender=GroupMember)
def new_member(sender, **kwargs):
   m = kwargs['instance']
   if m.is_chair:
      m.is_admin = True

class Event(models.Model):
   type = models.CharField(max_length=1,choices=EVENT_TYPE_CHOICES,default='g')
   name = models.CharField(max_length=255)
   description = models.TextField(null=True,blank=True)
   starttime = models.DateTimeField()
   endtime = models.DateTimeField()
   location = models.CharField(max_length=255,null=True,blank=True)
   sponsors = models.ManyToManyField(Group,blank=True,null=True)
   creator = models.ForeignKey(Member)

   def __unicode__(self):
      return self.name

   def all_sponsors(self):
      return ', '.join([str(x) for x in self.sponsors.all()])
   
   def has_sponsors(self):
      return len(self.sponsors.all()) > 0

class Job(models.Model):
   job_title = models.CharField(max_length=255)
   company = models.CharField(max_length=255)
   contact_name = models.CharField(max_length=255)
   contact_email = models.EmailField(max_length=255)
   contact_phone = models.CharField(max_length=255)
   type_full = models.BooleanField()
   type_part = models.BooleanField()
   type_intern = models.BooleanField() 
   description = models.TextField()
   timestamp = models.DateTimeField(auto_now_add=True)
   status = models.CharField(max_length=10,choices=EMAIL_STATUS_CHOICES,default='defer')
   sent = models.BooleanField(default=False,blank=True)
   
   def types(self):
      types = []
      if self.type_full:
         types.append("Full time")
      if self.type_part:
         types.append("Part time")
      if self.type_intern:
         types.append("Intern/Co-op")
      return ", ".join(types)
