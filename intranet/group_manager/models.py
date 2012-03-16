from django.db import models
from django.contrib.auth.models import User
import settings

TYPE_CHOICES = (('S', 'SIG'),('C', 'Committee'))

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=30)
	chair = models.ManyToManyField(User, related_name="group_chair_set")
	members = models.ManyToManyField(User, through="GroupMember")
	date_formed = models.DateField()
	description = models.TextField()
	meeting_time = models.DateTimeField()
	url = models.URLField()
	active = models.BooleanField()
	logo = models.FileField(upload_to=settings.MEDIA_ROOT)
	mailing_list = models.EmailField(max_length=60)
	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	
class GroupMember(models.Model):
  SIG = models.ForeignKey(Group)
  user = models.ForeignKey(User)
  date_joined = models.DateField()
  is_admin = models.BooleanField()
  is_banks_editor = models.BooleanField()

class Project(models.Model):
	name = models.CharField(max_length=30)
	lead = models.ForeignKey(User, related_name="project_lead_set")
	sigs = models.ManyToManyField(Group, blank=True, related_name="project_group_set")
	members = models.ManyToManyField(User, blank=True, related_name="project_members_set")
	description = models.TextField(blank=True)
	url = models.URLField()