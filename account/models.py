from django.db import models
from django.contrib.auth.models import User
from intranet.group_manager.models import GroupMember

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
