from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import settings
import datetime
import ldap
import logging
import os
from uuid import uuid4
from django.core.files.storage import FileSystemStorage
from utils.fields import ContentTypeRestrictedFileField
from utils.django_mailman.models import List
from subprocess import check_call
from django.db.models import Count
from django.db.models import Q
from utils.resume_download_helper import generate_resume_download

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

   def is_group_member(self, group):
      user_groups = self.groupmember_set.filter(group__name__iexact=group)
      return len(user_groups) > 0

   def is_top4(self):
      return self.is_group_admin('Top4')

   def is_acm_admin(self):
      return self.is_group_admin('Admin')

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

class PreMember(models.Model):
   first_name = models.CharField(max_length=32)
   last_name = models.CharField(max_length=32)
   uin = models.CharField(max_length=9)
   netid = models.CharField(max_length=16,unique=True)
   created_at = models.DateTimeField(auto_now_add=True)

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
   mailing_list = models.ForeignKey(List)
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

   def subscribe(self,email):
      if self.mailing_list.public:
         self.mailing_list.subscribe_email(email)

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
   RESUME_PERSON_GRADUATION = []

   current_year = datetime.datetime.now().year

   for i in range(-1,6):
      RESUME_PERSON_GRADUATION.append((datetime.date(current_year+i, 5, 1),'May %d'%(current_year+i)))
      RESUME_PERSON_GRADUATION.append((datetime.date(current_year+i, 12, 1),'December %d'%(current_year+i)))

   netid = models.CharField(max_length=255)
   first_name = models.CharField(max_length=255)
   last_name = models.CharField(max_length=255)
   graduation = models.DateField(choices=RESUME_PERSON_GRADUATION)
   level = models.CharField(max_length=1,choices=RESUME_PERSON_LEVEL)
   seeking = models.CharField(max_length=1,choices=RESUME_PERSON_SEEKING)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   resume_reminded_at = models.DateTimeField(default=datetime.datetime.now())
   resume_reminder_subscribed = models.BooleanField(default=True)
   ldap_name = models.CharField(max_length=255)

   # Helper method needed so that South works correctly
   def generate_uuid():
      return str(uuid4())

   resume_uuid = models.CharField(max_length=255, default=generate_uuid)

   def latest_resume(self):
      return self.resume_set.filter(approved=True).latest('created_at')

   def full_name(self):
      return "%s, %s"%(self.last_name, self.first_name)

   def acm_member(self):
      exist_count = Member.objects.filter(username=self.netid).count()
      return ("Yes" if exist_count > 0 else "No")

@receiver(pre_save, sender=ResumePerson)
def new_resume_person(sender, **kwargs):
   person = kwargs['instance']
   person.netid = person.netid.lower()
   if not person.id:
      l = ldap.initialize('ldap://ldap.uiuc.edu')
      u = l.search_s('ou=people,dc=uiuc,dc=edu',ldap.SCOPE_SUBTREE,'uid=%s'%person.netid)
      try:
         person.ldap_name = u[0][1]['cn'][0]
      except IndexError:
         raise ValueError('Bad Netid', 'Not a valid netid')

class PreResumePerson(ResumePerson):
   number = models.IntegerField()

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

   def thumbnail_large_location(self):
      return "%s/thumbnails/%d-large.png"%(settings.RESUME_STORAGE_LOCATION, self.id)

   def generate_thumbnails(self):
	   png = self.thumbnail_location()
	   png_top = self.thumbnail_top_location()
	   png_large = self.thumbnail_large_location()
	   if not os.path.exists(png) or not os.path.exists(png_top) or not os.path.exists(png_large):
		   try:
			   pdf = "%s[0]"%self.resume.path
			   check_call(["convert", "-quality", "100%", "-resize", "102x132", pdf, png])
			   check_call(["convert", "-quality", "100%", "-resize", "544x704", "-crop", "544x100+0+0", "+repage", pdf, png_top])
			   check_call(["convert", "-quality", "100%", "-resize", "544x704",  pdf, png_large])
		   except:
			   pass

@receiver(post_save, sender=Resume)
def new_resume(sender, **kwargs):
   resume = kwargs['instance']
   resume.generate_thumbnails()

@receiver(post_delete, sender=Resume)
def delete_resume(sender, **kwargs):
   resume = kwargs['instance']
   fs.delete(resume.resume.path)
   fs.delete(resume.thumbnail_location())
   fs.delete(resume.thumbnail_top_location())

class Recruiter(User):
   expires = models.DateField()
   objects = UserManager()

@receiver(post_save, sender=Recruiter)
def new_recruiter(sender, **kwargs):
   recruiter = kwargs['instance']
   if recruiter.groups.filter(name='Recruiter').count() == 0:
      group = DjangoGroup.objects.get(name="Recruiter")
      recruiter.groups.add(group)
      recruiter.save()


class ResumeDownloadSet(models.Model):
   owner = models.ForeignKey(User)
   level = models.CharField(max_length=64,null=True)
   seeking = models.CharField(max_length=64,null=True)
   acm = models.NullBooleanField(null=True)
   graduation_start = models.DateField(null=True)
   graduation_end = models.DateField(null=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def get_people(self,extra_filter=None,resume_extra_filter=None):
      level = None
      if self.level != None:
         level = list(self.level)

      seeking = None
      if self.seeking != None:
         seeking = list(self.seeking)

      acm = self.acm

      approved_resumes = Resume.objects.filter(approved=True)

      if resume_extra_filter != None:
         approved_resumes = approved_resumes.filter(resume_extra_filter)

      people = ResumePerson.objects.filter(resume__in=approved_resumes).annotate(resume_count=Count('resume')).filter(resume_count__gt=0)

      if level != None and level != "":
         people = people.filter(level__in=level)

      if seeking != None and seeking != "":
         people = people.filter(seeking__in=seeking)

      if self.graduation_start != None:
         people = people.filter(graduation__gte=self.graduation_start)

      if self.graduation_end != None:
         people = people.filter(graduation__lte=self.graduation_end)

      if acm == True:
         netids = Member.objects.all().values_list('username', flat=True)
         people = people.filter(netid__in=netids)


      if extra_filter != None:
         people = people.filter(extra_filter)

      people = people.order_by('last_name','first_name')

      return people

   def show_undergraduate(self):
      return self.level != None and self.level.find('u') >= 0

   def show_masters(self):
      return self.level != None and self.level.find('m') >= 0

   def show_phd(self):
      return self.level != None and self.level.find('p') >= 0

   def show_full_time(self):
      return self.seeking != None and self.seeking.find('f') >= 0

   def show_internship(self):
      return self.seeking != None and self.seeking.find('i') >= 0

   def show_acm(self):
      return self.acm != None and self.acm

   def generate_download(self):
      if self.get_new_count() > 0 or self.resumedownload_set.count() == 0:
         download = ResumeDownload(set=self)
         download.save()
      else:
         download = self.resumedownload_set.latest('created_at')
      return download

   def get_new_count(self):
      query = None
      if self.resumedownload_set.count() > 0:
         download = self.resumedownload_set.latest('created_at')
         query = Q(created_at__gt=download.created_at)
      people = self.get_people(None,query)
      return people.count()

   def get_display(self):
      out = []
      levels = {'u':'Undergraduate','m':'Masters','p':'PhD'}
      seekings = {'f':'Full Time','i':'Internship/Co-op'}
      if self.level != None:
         level_out = []
         for l in list(self.level):
            level_out.append(levels[l])
         out.append(" or ".join(level_out))
      if self.seeking != None:
         seeking_out = []
         for s in list(self.seeking):
            seeking_out.append(seekings[s])
         out.append(" or ".join(seeking_out))
      if self.acm == True:
         out.append("ACM@UIUC members")
      if self.graduation_start != None:
         out.append("Graduating after %s %d"%(self.graduation_start.strftime('%B'),self.graduation_start.year))
      if self.graduation_end != None:
         out.append("Graduating before %s %d"%(self.graduation_end.strftime('%B'),self.graduation_end.year))

      if len(out) == 0:
         return "All resumes"

      return " and ".join(out)



class ResumeDownload(models.Model):
   set = models.ForeignKey(ResumeDownloadSet)
   created_at = models.DateTimeField(auto_now_add=True)

   def file_path(self):
      return "%s/packets/%d.pdf"%(settings.RESUME_STORAGE_LOCATION,self.id)

   def diff_file_path(self):
      return "%s/packets/diff-%d.pdf"%(settings.RESUME_STORAGE_LOCATION,self.id)

   def generate(self):
      if os.path.exists(self.file_path()):
         return

      people = self.set.get_people()

      generate_resume_download(people,self.set.get_display(),self.created_at,self.file_path())


   def generate_diff(self):
      if os.path.exists(self.diff_file_path()):
         return

      query = None
      interested_set = self.set.resumedownload_set.exclude(id=self.id)
      if interested_set.count() > 0:
         download = interested_set.latest('created_at')
         query = Q(created_at__gt=download.created_at)
      people = self.set.get_people(None,query)

      generate_resume_download(people,"Only new or updated %s"%self.set.get_display(),self.created_at,self.diff_file_path())

   def update_count(self):
      query = None
      interested_set = self.set.resumedownload_set.exclude(id=self.id)
      if interested_set.count() > 0:
         download = interested_set.latest('created_at')
         query = Q(created_at__gt=download.created_at)
      people = self.set.get_people(None,query)
      return people.count()
