from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import datetime, re, string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import html
from intranet.models import Member

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
      self.quote_text = re.sub("(^|(?<=(\.|\s|\:)))#(?P<tag>\w+)", "<a href='/intranet/quote/?q=%23\g<tag>'>#\g<tag></a>", self.quote_text)
   
      # Hyperlink authors
      authors = self.quote_sources.split(",")
      self.quote_source_html = ""
      quote_count = 0
      for author_netid in authors:
      
         quote_count += 1
      
         # Convert author's netid to their name (if possible)
         author_obj = Member.objects.get(username=author_netid)
         author = author_obj.full_name()
         if author == None or len(author) == 0:
            author = author_netid
      
         # ============ In-quote tagged authors ===========          + r"(?=($|(?<=(\.|\s|\:))))"
         self.quote_text = re.sub(r"(^|(?<=(\.|\s|:)))(?P<author>(" + author + "|" + author_obj.first_name + "|" + author_netid + "))", "<a href='/intranet/quote/?author=" + author_netid + "'>\g<author></a>", self.quote_text)  
      
         # ========== Quote sources (HTML) field ==========
         # Quote separators (commas and ands)
         if quote_count != 1:
            if quote_count == len(authors):
               self.quote_source_html += " and "
            else:
               self.quote_source_html += ", "
      
         # Quote material
         self.quote_source_html += "<a href='/intranet/quote/?author=" + author_netid + "'>" + author + "</a>"
         
      # Save quote (or updates to it, if it has already been instantiated)
      super(Quote, self).save(*args, **kwargs)
