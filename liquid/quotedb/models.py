from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Quote(models.Model):
   quote_text = models.TextField(max_length=500)
   quote_source = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
