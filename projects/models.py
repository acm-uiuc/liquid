from django.db import models
from django.contrib.auth.models import User


class SIG(models.Model):
	name = models.CharField(max_length=30)
	chair = models.ForeignKey(User, related_name="sig_chair_set")
	members = models.ManyToManyField(User, blank=True, related_name="sig_members_set")
	date_formed = models.DateField(auto_now=True)
	description = models.TextField(blank=True)
	meeting_time = models.CharField(max_length=50)
	url = models.URLField()
	active = models.BooleanField()

class Project(models.Model):
	name = models.CharField(max_length=30)
	lead = models.ForeignKey(User, related_name="project_lead_set")
	sigs = models.ManyToManyField(SIG, blank=True, related_name="project_sigs_set")
	members = models.ManyToManyField(User, blank=True, related_name="project_members_set")
	description = models.TextField(blank=True)
	url = models.URLField()
	
