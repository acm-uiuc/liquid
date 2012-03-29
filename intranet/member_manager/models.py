from django.db import models
from django.contrib.auth.models import User
import settings

# Create your models here.
class Member(models.Model):
  class Meta:
    db_table="users"
    
  STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))
  
  uid = models.IntegerField(max_length=20,primary_key=True)
  netid = models.CharField(max_length=30,unique=True)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  uin = models.CharField(max_length=9)
  joined = models.DateTimeField()
  left_uiuc = models.DateField()
  status = models.CharField(max_length=255,choices=STATUS_CHOICES)
	
  def full_name(self):
    return self.first_name + " " + self.last_name