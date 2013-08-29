from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
from django.core.files.storage import FileSystemStorage
from utils.fields import ContentTypeRestrictedFileField
from subprocess import check_call
from django.db.models import Count
from django.db.models import Q
from intranet.models import Member
import settings
import datetime
import ldap
import logging
import os

class BanksPost(models.Model):
  title = models.CharField(max_length=255)
  subtitle = models.CharField(max_length=255)
  body = models.TextField()
  creator = models.ForeignKey(Member)
  created = models.DateTimeField(auto_now_add=True)

  #def __unicode__(self):
   # return self.title

class Comment(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  author = models.CharField(max_length=60)
  body = models.TextField()
  post = models.ForeignKey(BanksPost)

  #def __unicode__(self):
  #  return unicode("%s: %s" % (self.post, self.body[:60]))