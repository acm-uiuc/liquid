from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import settings
import datetime
import ldap
import logging
import os
from django.core.files.storage import FileSystemStorage
from utils.fields import ContentTypeRestrictedFileField
from utils.django_mailman.models import List
from subprocess import check_call


# Create your models here.
MEMBER_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))

GROUP_TYPE_CHOICES = (('S', 'SIG'),('C', 'Committee'),('O','Other'))
GROUP_DAY_CHOICES = ((0,'Sunday'),(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'))
GROUP_MEMBER_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))
GROUP_STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))

EVENT_TYPE_CHOICES = (('a','ACM General'),('g','Group'),('d','Department'),('c','Corporate'),('o','Other'))

EMAIL_STATUS_CHOICES = (('defer','Defer'),('approve','Approve'),('discard','Discard'))

RESUME_PERSON_LEVEL = (('u','Undergraduate'),('m','Masters'),('p','PhD'))

RESUME_PERSON_SEEKING = (('f','Full Time'),('i','Internship/Co-op'))

RESUME_PERSON_GRADUATION = []

current_year = datetime.datetime.now().year

for i in range(-1,6):
   RESUME_PERSON_GRADUATION.append((datetime.date(current_year+i, 5, 1),'May %d'%(current_year+i)))
   RESUME_PERSON_GRADUATION.append((datetime.date(current_year+i, 12, 1),'December %d'%(current_year+i)))

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
  
   def get_vending(self):
      return self.vending_set.all()[0]

   def __unicode__(self):
      return self.full_name()
#change username to netid in member
Member._meta.get_field('username').verbose_name = 'netid'

@receiver(pre_save, sender=Member)
def new_member(sender, **kwargs):
   user = kwargs['instance']
   logging.debug('user: %s' % user)
   logging.debug('username: %s' % user.username)
   if not user.id:
      l = ldap.initialize('ldap://ldap.uiuc.edu')
      u = l.search_s('ou=people,dc=uiuc,dc=edu',ldap.SCOPE_SUBTREE,'uid=%s'%user.username)
      try:
         user.last_name = u[0][1]['sn'][0]
         user.first_name = u[0][1]['givenName'][0]
      except IndexError:
         raise ValueError('Bad Netid', 'Not a valid netid')
      user.email = user.username + "@illinois.edu"
      ## add to mailing lists
      try:
         membership_list = List.objects.get(name='Membership-l')
         job_list = List.objects.get(name='Jobs-l')
      except:
         pass
      membership_list.subscribe(user)
      job_list.subscribe(user)

@receiver(post_save, sender=Member)
def new_member_post_save(sender, **kwargs):
      user = kwargs['instance']
      ## add vending account
      try:
         Vending.objects.get(user=user)
      except Vending.DoesNotExist:
         v = Vending(user=user,balance=5)
         v.save()

class Vending(models.Model):
   user = models.ForeignKey(Member,primary_key=True,db_column='uid')
   balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   calories = models.IntegerField(max_length=11,default=0)
   caffeine = models.FloatField(default=0)
   spent = models.DecimalField(max_digits=10, decimal_places=2,default=0)
   sodas = models.IntegerField(max_length=11,default=0)
   
   class Meta:
      db_table = 'vending'

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
      chairs = []
      for c in self.members.filter(groupmember__is_chair=True).order_by('last_name'):
         chairs.append(c.full_name())
      
      return ", ".join(chairs)

   def active_members(self):
      return self.members.filter(groupmember__status='active').order_by('last_name')

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
def new_groupmember(sender, **kwargs):
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

   def pretty_time(self):
      time = self.starttime.strftime('%A, %b %d, %Y %I:%M%p')
      if self.starttime.date() == self.endtime.date():
         time += "-%s"%(self.endtime.strftime('%I:%M%p'))
      else:
         time += "-%s"%(self.endtime.strftime('%A, %b %d, %Y %I:%M%p'))
      return time

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

class ResumePerson(models.Model):
   netid = models.CharField(max_length=255)
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   graduation = models.DateField(choices=RESUME_PERSON_GRADUATION)
   level = models.CharField(max_length=1,choices=RESUME_PERSON_LEVEL)
   seeking = models.CharField(max_length=1,choices=RESUME_PERSON_SEEKING)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   ldap_name = models.CharField(max_length=255)

@receiver(pre_save, sender=ResumePerson)
def new_resume_person(sender, **kwargs):
   person = kwargs['instance']
   if not person.id:
      l = ldap.initialize('ldap://ldap.uiuc.edu')
      u = l.search_s('ou=people,dc=uiuc,dc=edu',ldap.SCOPE_SUBTREE,'uid=%s'%person.netid)
      try:
         person.ldap_name = u[0][1]['cn'][0]
      except IndexError:
         raise ValueError('Bad Netid', 'Not a valid netid')

# Wher to store the resumes
fs = FileSystemStorage(location=settings.RESUME_STORAGE_LOCATION)

def create_resume_file_name(instance,filename):
   return "%s/%s-%s.pdf"%(settings.RESUME_STORAGE_LOCATION,
                          instance.person.netid,
                          os.urandom(16).encode('hex'))

class Resume(models.Model):
   person = models.ForeignKey(ResumePerson,null=True)
   approved = models.BooleanField(default=False)
   resume = ContentTypeRestrictedFileField(upload_to=create_resume_file_name,
                                                  storage=fs,
                                                  content_types=['application/pdf'],
                                                  max_upload_size=1048576)
   created_at = models.DateTimeField(auto_now_add=True)

   def thumbnail_location(self):
      return "%s/thumbnails/%d.png"%(settings.RESUME_STORAGE_LOCATION, self.id)

   def thumbnail_top_location(self):
      return "%s/thumbnails/%d-top.png"%(settings.RESUME_STORAGE_LOCATION, self.id)

   def generate_thumbnails(self):
      if not os.path.exists(self.thumbnail_location()) or not os.path.exists(self.thumbnail_top_location()):
         try:
            pdf = "%s[0]"%self.resume.path
            png = self.thumbnail_location()
            png_top = self.thumbnail_top_location()
            check_call(["convert", "-quality", "100%", "-resize", "102x132", pdf, png])
            check_call(["convert", "-quality", "100%", "-resize", "544x704", "-crop", "544x100+0+0", "+repage", pdf, png_top])
         except:
            pass

@receiver(post_save, sender=Resume)
def new_resume(sender, **kwargs):
   resume = kwargs['instance']
   resume.generate_thumbnails()
   