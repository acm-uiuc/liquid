from django.db import models
from django.contrib.auth.models import User
import settings
import ldap
import datetime

# Create your models here.
class Member(User):
  class Meta:
    db_table="users"
    
  STATUS_CHOICES = (('active','active'),('inactive','inactive'),('frozen','frozen'))
  
  uid = models.AutoField(max_length=20,primary_key=True)
  netid = models.CharField(max_length=30,unique=True)
  first_name = models.CharField(max_length=30,blank=True)
  last_name = models.CharField(max_length=30,blank=True)
  uin = models.CharField(max_length=9)
  joined = models.DateTimeField(default=datetime.date.today)
  left_uiuc = models.DateField(null=True,blank=True)
  status = models.CharField(max_length=255,choices=STATUS_CHOICES,default='active')
  
  def save(self, *args, **kwargs):
    if not self.uid:
      l = ldap.initialize('ldap://ldap.uiuc.edu')
      u = l.search_s('ou=people,dc=uiuc,dc=edu',ldap.SCOPE_SUBTREE,'uid=%s'%self.netid)
      try:
        self.last_name = u[0][1]['sn'][0]
        self.first_name = u[0][1]['givenName'][0]
      except IndexError:
        raise ValueError('Bad Netid', 'Not a valid netid')
      ## perform other first save operations (caffiene)
    super(Member, self).save(*args, **kwargs)

  def full_name(self):
    return self.first_name + " " + self.last_name

  def __unicode__(self):
    return self.netid
