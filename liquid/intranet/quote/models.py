from django.db import models
from django.contrib.auth.models import User, UserManager, Group as DjangoGroup
import datetime, re, string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import html
from intranet.models import Member

# Create your models here.
class Quote(models.Model):

   # Fields
   quote_text = models.TextField(max_length=700)
   quote_sources = models.CharField(max_length=100) # The sources of the quote (not displayed on the page, purely for recordkeeping)
   quote_source_html = models.CharField(max_length=200) # The HTML that represents the quote source (and is displayed with the quote)
   quote_posters = models.CharField(max_length=100, blank=True)
   quote_poster_html = models.CharField(max_length=200)
   created_at = models.DateTimeField(auto_now_add=True)
   
   def save(self, *args, **kwargs):
   
      # HTML-Escape quote/author text (since this text is displayed with auto-escape disabled)
      self.quote_text = html.escape(self.quote_text)
      self.quote_sources = "," + html.escape(re.sub(",\s+", ",", self.quote_sources).strip(",")) + ","
   
      # Hyperlink hashtags
      self.quote_text = re.sub("(^|(?<=(\.|\s|\:)))#(?P<tag>\w+)", "<a href='/intranet/quote/?q=%23\g<tag>'>#\g<tag></a>", self.quote_text)
   
      # Turn newlines into <br>'s
      self.quote_text = re.sub("(\r|)\n", "<br />", self.quote_text)

      # Hyperlink authors
      authors = self.quote_sources.strip(",").split(",")
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
      
         # Add to authors list HTML
         self.quote_source_html += "<a href='/intranet/quote/?author=" + author_netid + "'>" + author + "</a>" 
           
      # Hyperlink posters (people who edited the quote but didn't say anything noteworthy)
      if len(self.quote_posters) != 0: # Posters were not recorded for some earlier quotes
         self.quote_posters = "," + html.escape(re.sub(",\s+", ",", self.quote_posters).strip(",")) + ","
         posters = self.quote_posters.strip(",").split(",")
      else:
         posters = dict() # Posters should contain no elements if self.quote_posters is blank
         
      # If the quote posters are different than the quote authors, create the quote poster HTML
      posters_are_authors = len(posters) == len(authors) or len(posters) == 0; # Posters were not recorded for some earlier quotes
      if posters_are_authors:
         
         # Poster --> author check (since the counts are equal, we only need to check in one direction)
         for poster in posters:
            posters_are_authors = posters_are_authors and poster in authors;
            if not posters_are_authors:
               break
      
      if not posters_are_authors:
      
         # Create quote poster HTML
         self.quote_poster_html = " (Posted by "
         
         poster_count = 0
         for poster_netid in posters:
         
            poster_count += 1
            
            # Convert poster's netid to their name (if possible)
            poster_obj = Member.objects.get(username=poster_netid)
            poster = poster_obj.full_name()
            if poster == None or len(poster) == 0:
               poster = poster_netid
            
            # Quote separators (commas and ands)
            if poster_count != 1:
               if poster_count == len(posters):
                  self.quote_poster_html += " and "
               else:
                  self.quote_poster_html += ", "
            
            # Add to posters list HTML
            self.quote_poster_html += "<a href='/intranet/quote/?author=" + poster_netid + "'>" + poster + "</a>"
              
         self.quote_poster_html += ")"
 
      # Save quote (or updates to it, if it has already been instantiated)
      super(Quote, self).save(*args, **kwargs)
