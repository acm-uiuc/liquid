from django.db import models
from intranet.member_manager.models import Member
import settings

TYPE_CHOICES = (('S', 'SIG'),('C', 'Committee'))

# Create your models here.
class Group(models.Model):
	name = models.CharField(max_length=30)
	chairs = models.ManyToManyField(Member, related_name="group_chair_set",blank=True)
	members = models.ManyToManyField(Member, through="GroupMember",blank=True)
	date_formed = models.DateField()
	description = models.TextField()
	meeting_time = models.DateTimeField()
	url = models.URLField()
	active = models.BooleanField()
	logo = models.URLField()
	mailing_list = models.EmailField(max_length=60)
	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	
class GroupMember(models.Model):
	group = models.ForeignKey(Group)
  member = models.ForeignKey(Member)
  date_joined = models.DateField()
  is_admin = models.BooleanField()
  is_banks_editor = models.BooleanField()

class Project(models.Model):
	name = models.CharField(max_length=30)
	lead = models.ForeignKey(Member, related_name="project_lead_set")
	groups = models.ManyToManyField(Group, blank=True, related_name="project_group_set")
	members = models.ManyToManyField(Member, blank=True, related_name="project_members_set")
	description = models.TextField(blank=True)
	url = models.URLField()
	
	
