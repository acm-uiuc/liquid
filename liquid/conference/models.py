from django.db import models
from intranet.models import Member

# Create your models here.
class Vote(models.Model):
   user = models.ForeignKey(Member)
   poll = models.IntegerField()
   key = models.CharField(max_length=32)
   vote = models.NullBooleanField(null=True)
