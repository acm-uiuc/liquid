from django.db import models
from django.contrib.auth.models import User
from liquid.intranet.group_manager import GroupMember

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
    groups = models.OneToManyField(GroupMember)
