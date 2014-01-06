import re, string
from django import forms
from django.shortcuts import render_to_response, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from intranet.quote.forms import QuoteForm
from intranet.quote.models import Quote
from django.conf import settings
from django.core.exceptions import PermissionDenied
from intranet.models import Member
import HTMLParser

def main(request, quote_id = 0):
  
   # Get list of quotes to show
   text_search_arg = request.GET.get("q")
   author_search_arg = request.GET.get("author")
   if author_search_arg != None:
      author_search_arg += ","
   quote_list = Quote.objects.all().order_by("-created_at")
   
   # Quote filtering
   if quote_id == 0:
   
      # -- Text search
      if text_search_arg and len(text_search_arg) != 0:
          quote_list = quote_list.filter(quote_text__icontains=text_search_arg)
          
      # -- Author search
      if author_search_arg and len(author_search_arg) != 0:
          quote_list = quote_list.filter(quote_sources__icontains=author_search_arg)
   else:
      # Don't use get_object_or_404 here - quote_list can be empty and shouldn't cause problems if it is
      quote_list = Quote.objects.filter(pk=quote_id)
  
   # Determine which quotes are editable by the current user
   user = request.user
   for q in quote_list:
      quote_sources = q.quote_sources.split(",")
      quote_posters = q.quote_posters.split(",")
      q.canEdit = (not user.is_anonymous() and (user.username in quote_sources or user.username in quote_posters)) or (user.is_top4())
  
   # Get paginator and page
   page = 1
   page_arg = request.GET.get("page")
   if page_arg and page_arg.isdigit():
      page = int(page_arg)
   paginator = Paginator(quote_list, 10)
   page = min(paginator.num_pages, page)
   page = max(1, page)
   quotePage = paginator.page(page)
   
   return render_to_response('intranet/quote/main.html',{"section":"intranet","page":"quote","quotePage":quotePage,"request":request,"searchArg":text_search_arg},context_instance=RequestContext(request))

def add(request):

   quote_form = None
   if request.method == 'POST':

      #-- Handle new quotes --
      # Save quote (if it's valid; otherwise do nothing)
      request.POST['quote_posters'] = request.user.username # So altering this in the POST request does nothing
      quote_form = QuoteForm(request.POST)
      if quote_form.is_valid():
         quote_form.save()
         return redirect('/intranet/quote/')
   else:

      # -- Handle quote adding --
      # Make new form and prepopulate it with poster name
      quote_form = QuoteForm()
      
   # Hide quote_posters (since the user shouldn't see it and can't modify it)
   quote_form.fields["quote_posters"].widget = forms.HiddenInput()
      
   # Return form to user (either a new form, or a form with their invalid input in it if such input was provided)
   return render_to_response('intranet/quote/add.html',{"section":"intranet","page":'quote',"form":quote_form,"members":Member.objects.all(),"user":request.user},context_instance=RequestContext(request))
      
def edit(request, quoteId = 1): 
   
   # Quote deletion logic
   if (request.method == 'POST') and ('delete' in request.POST):
   
      # --- Handle delete requests ---
      quote_in_question = get_object_or_404(Quote, pk=quoteId)
      quote_in_question.delete()
      
      return redirect('/intranet/quote/')
   
   # Quote editing logic
   author_usernames = ""
   if (request.method == 'POST'):

      # --- Handle save requests (from edit form to quote list) ---
      quote_in_question = get_object_or_404(Quote, pk=quoteId)
      
      # Add current user to _posters list, if necessary
      if not ("," + request.user.username + ",") in quote_in_question.quote_posters:
      
         # Strip is used to provide backwards compatibility with old quotes
         quote_in_question.quote_posters = "," + quote_in_question.quote_posters.strip(",") + "," + request.user.username + "," 
      
      quote_form = QuoteForm(request.POST,
                            instance=quote_in_question)
      author_usernames = request.POST["quote_sources"].strip(",").split(",")
      if quote_form.is_valid():
         quote_form.save()
         return redirect('/intranet/quote/')
        
   # --- Logic for new quote forms/those with invalid data 
   # Make sure quote editor can actually edit the current quote (and reject their request if they can't)
   user = request.user
   quote_obj = get_object_or_404(Quote, pk=quoteId)

   # New-form-only (i.e. not just when user submits invalid data) logic
   if (request.method != 'POST'):
      author_usernames = quote_obj.quote_sources.strip(",").split(",")
      poster_usernames = quote_obj.quote_posters.strip(",").split(",")
       
      canEdit = (not user.is_anonymous() and (user.username in author_usernames) or (user.username in poster_usernames)) or (user.is_top4())
       
      if (not canEdit):
         raise PermissionDenied # Current user cannot edit this quote
    
      # Unescape escaped quote text
      quote_obj.quote_text = HTMLParser.HTMLParser().unescape(quote_obj.quote_text)

      # Remove hashtags/authortags in text
      quote_obj.quote_text = string.replace(re.sub("<a href='.+?'>", "", quote_obj.quote_text), "</a>", "")
      
      # Convert <br />'s into newlines (\n - TODO?: this may cause issues for Windows users)
      quote_obj.quote_text = string.replace(quote_obj.quote_text, "<br />", "\n")
 
      quote_form = QuoteForm(instance=quote_obj)

   quote_form.fields["quote_posters"].widget = forms.HiddenInput()
   
   # --- Return form (either a new one, or one with existing data if user has provided invalid data) ---
   print author_usernames    
   quoteMembers = Member.objects.filter(username__in=author_usernames) # Get authors' Member objects
   
   return render_to_response('intranet/quote/edit.html',{"section":"intranet","page":'quote',"form":quote_form, "members":Member.objects.all(),"quoteMembers":quoteMembers,"quote_id":quoteId,"user":request.user},context_instance=RequestContext(request))  
      
