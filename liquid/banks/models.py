from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import settings
import datetime
import ldap
import logging
import os
from django.core.files.storage import FileSystemStorage
from utils.fields import ContentTypeRestrictedFileField
from subprocess import check_call
from django.db.models import Count
from django.db.models import Q

#create your models here

class Post(models.Model):
  title = models.charField(max_length=255)
  subtitle = models.charField(max_length=255)

  content = models.charField()
  creator = models.ForeignKey(Member)
  created_at = models.DateTimeField(auto_now_add=True)
