from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import datetime, re, string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import html

# Create your models here.
class Quote(models.Model):
   quote_text = models.TextField(max_length=700)
   quote_sources = models.CharField(max_length=100) # The sources of the quote (not displayed on the page, purely for recordkeeping)
   quote_source_html = models.CharField(max_length=200) # The HTML that represents the quote source (and is displayed with the quote)
   created_at = models.DateTimeField(auto_now_add=True)
   
   def save(self, *args, **kwargs):
   
      # HTML-Escape quote/author text (since this text is displayed with auto-escape disabled)
      self.quote_text = html.escape(self.quote_text)
      self.quote_sources = html.escape(re.sub(",\s+", ",", self.quote_sources))
   
      # Hyperlink hashtags
      self.quote_text = re.sub("(^|(?<=\W))#(?P<tag>\w+)", "<a href='/intranet/quote/?q=%23\g<tag>'>#\g<tag></a>", self.quote_text)
   
      # Hyperlink authors
      authors = self.quote_sources.split(",")
      self.quote_source_html = ""
      quote_count = 0
      for author in authors:
      
         quote_count += 1
      
         # Quote separators (commas and ands)
         if quote_count != 1:
            if quote_count == len(authors):
               self.quote_source_html += " and "
            else:
               self.quote_source_html += ", "
      
         # Quote material
         self.quote_source_html += "<a href='/intranet/quote/?author=" + author + "'>" + author + "</a>"
         
      # Save quote (or updates to it, if it has already been instantiated)
      super(Quote, self).save(*args, **kwargs)
