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
from utils.slugs import unique_slugify

import settings
import datetime
import ldap
import logging
import os


class BanksPost(models.Model):

    title = models.CharField(max_length = 255)
    subtitle = models.CharField(max_length = 255, default='')

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
      unique_slugify(self, self.title)
      self.subtitle = ''
      self.content_markup = markdown(self.content_markdown, ['codehilite'])
      super(BanksPost, self).save()

    def __unicode__(self):
      return "%s" % (self.title,)