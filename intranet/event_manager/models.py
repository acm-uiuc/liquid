from django.db import models
from intranet.group_manager.models import Group

TYPE_CHOICES = (('a','ACM General'),('g','Group'),('d','Department'))

# Create your models here.
class Event(models.Model):
	type = models.CharField(max_length=1,choices=TYPE_CHOICES)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True,blank=True)
	starttime = models.DateTimeField()
	endtime = models.DateTimeField()
	location = models.CharField(max_length=255,null=True,blank=True)
	sponsors = models.ManyToManyField(Group, blank=True)

	def __unicode__(self):
		return self.name

	def all_sponsors(self):
		print self.sponsors.all()
		return ', '.join([str(x) for x in self.sponsors.all()])
