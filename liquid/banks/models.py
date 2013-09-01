from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
from django.core.files.storage import FileSystemStorage
from utils.fields import ContentTypeRestrictedFileField
from subprocess import check_call
from django.db.models import Count
from django.db.models import Q
from intranet.models import Member
from markdown import markdown
from django.utils.translation import ugettext as _
import settings
import datetime
import ldap
import logging
import os


class Post(models.Model):

    title = models.CharField(max_length = 255)

    slug = models.SlugField(
      max_length = 255,
      unique = True
    )

    content_markdown = models.TextField()
    content_markup = models.TextField()
    date_publish = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Member)

    class Meta:
      ordering = ['-date_publish']

    def save(self):
      self.slug = slugify(self.title)
      self.content_markup = markdown(self.content_markdown, ['codehilite'])
      super(Post, self).save()

    def __unicode__(self):
      return "%s" % (self.title,)

