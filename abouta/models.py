from django.db import models
from django.forms import ModelForm

# Create your models here.
class Job(models.Model):
  job_title = models.CharField(max_length=255)
  company = models.CharField(max_length=255)
  contact_name = models.CharField(max_length=255)
  contact_email = models.CharField(max_length=255)
  contact_phone = models.CharField(max_length=255)
  type_full = models.BooleanField()
  type_part = models.BooleanField()
  type_intern = models.BooleanField() 
  description = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  
class JobForm(ModelForm):
  class Meta:
      model = Job