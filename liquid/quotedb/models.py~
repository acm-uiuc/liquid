from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import datetime, re, string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import html

# Create your models here.
class Quote(models.Model):
   quote_text = models.TextField(max_length=500)
   quote_source = models.CharField(max_length=100)
   created_at = models.DateTimeField(auto_now_add=True)
   
   def save(self, *args, **kwargs):
   
      # HTML-Escape quote text (since this text is displayed with auto-escape disabled)
      self.quote_text = html.escape(self.quote_text)
   
      # Hyperlink hashtags
      self.quote_text = re.sub("(^|(?<=\W))#(?P<tag>\w+)", "<a href='/quotedb/?q=%23\g<tag>'>&#35;\g<tag></a>", self.quote_text)
   
      # Save quote
      super(Quote, self).save(*args, **kwargs)
