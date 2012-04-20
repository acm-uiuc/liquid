from django.db import models
from intranet.models import Member
import json

class Animation(models.Model):
   name = models.CharField(max_length=255)
   description = models.TextField()
   creator = models.CharField(max_length=255)
   identifier = models.CharField(max_length=255)

class Play(models.Model):
   animation = models.ForeignKey(Animation,null=True)
   member = models.ForeignKey(Member)
   timestamp = models.DateTimeField(auto_now_add=True, blank=True)
   