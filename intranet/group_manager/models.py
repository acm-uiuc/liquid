from django.db import models
from intranet.member_manager.models import Member
import settings
import datetime

TYPE_CHOICES = (('S', 'SIG'),('C', 'Committee'),('O','Other'))
DAY_CHOICES = ((0,'Sunday'),(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'))
STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))

# Create your models here.
class Group(models.Model):
	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	name = models.CharField(max_length=30)
	members = models.ManyToManyField(Member, through="GroupMember",blank=True)
	date_formed = models.DateField()
	description = models.TextField()
	meeting_time = models.TimeField(null=True,blank=True)
	meeting_day = models.IntegerField(null=True,blank=True,choices=DAY_CHOICES)
	meeting_location = models.CharField(max_length=255,null=True,blank=True)
	url = models.URLField(null=True,blank=True)
	logo = models.URLField(null=True,blank=True)
	mailing_list = models.EmailField(max_length=60)
	status = models.CharField(max_length=255,choices=STATUS_CHOICES,default='active')

	def __unicode__(self):
		return self.name

	def chairs(self):
		return self.members.filter(groupmember__is_chair=True)
	
class GroupMember(models.Model):
	class Meta:
		unique_together = ('group','member')
	group = models.ForeignKey(Group)
	member = models.ForeignKey(Member)
	date_joined = models.DateField(default=datetime.date.today)
	is_chair = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	status = models.CharField(max_length=255,choices=STATUS_CHOICES,default='active')

class Project(models.Model):
	name = models.CharField(max_length=30)
	lead = models.ForeignKey(Member, related_name="project_lead_set")
	groups = models.ManyToManyField(Group, blank=True, related_name="project_group_set")
	members = models.ManyToManyField(Member, blank=True, related_name="project_members_set")
	description = models.TextField(blank=True)
	url = models.URLField()
	