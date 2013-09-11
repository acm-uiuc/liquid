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
   
      # HTML-Escape quote/author text (since this text is displayed with auto-escape disabled)
      self.quote_text = html.escape(self.quote_text)
      self.quote_source = html.escape(self.quote_source)
   
      # Hyperlink hashtags
      self.quote_text = re.sub("(^|(?<=\W))#(?P<tag>\w+)", "<a href='/intranet/quote/?q=%23\g<tag>'>#\g<tag></a>", self.quote_text)
   
      # Hyperlink author
      self.quote_source = "<a href='/intranet/quote/?author=" + self.quote_source + "'>" + self.quote_source + "</a>"
   
      # Save quote (or updates to it, if it has already been instantiated)
      super(Quote, self).save(*args, **kwargs)
