from django.db import models

# Create your models here.
class SIG(models.Model):
	name = models.CharField(max_length=30)
	chair = models.ManyToManyField(User, related_name="sig_chair_set")
	members = models.ManyToManyField(User, through="SIGMember")
	date_formed = models.DateField()
	description = models.TextField()
	meeting_time = models.DateTimeField()
	url = models.URLField()
	active = models.BooleanField()
	
class SIGMember(models.Model):
  SIG = models.ForeighnKey(SIG)
  user = models.ForeignKey(User)
  date_joined = models.DateField()
  is_admin = models.BooleanField()
  is_banks_editor = model.BooleanField()

class Project(models.Model):
	name = models.CharField(max_length=30)
	lead = models.ForeignKey(User, related_name="project_lead_set")
	sigs = models.ManyToManyField(SIG, blank=True, related_name="project_sigs_set")
	members = models.ManyToManyField(User, blank=True, related_name="project_members_set")
	description = models.TextField(blank=True)
	url = models.URLField()