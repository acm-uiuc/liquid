import re, string
from django.shortcuts import render_to_response, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from intranet.quote.forms import QuoteForm
from intranet.quote.models import Quote
from django.conf import settings
from django.core.exceptions import PermissionDenied
from intranet.models import Member

# Create your views here.
def main(request, quote_id = 0):
  
   # Get list of quotes to show
   textSearchArg = request.GET.get("q")
   authorSearchArg = request.GET.get("author")
   quote_list = Quote.objects.all().order_by("-created_at")
   
   # Quote filtering
   if quote_id == 0:
   
      # -- Text search
      if textSearchArg and len(textSearchArg) != 0:
          quote_list = quote_list.filter(quote_text__icontains=textSearchArg)
          
      # -- Author search
      if authorSearchArg and len(authorSearchArg) != 0:
          quote_list = quote_list.filter(quote_sources__icontains=authorSearchArg)
   else:
        quote_list = Quote.objects.filter(pk=quote_id)
  
   # Determine which quotes are editable by the current user
   user = request.user
   for q in quote_list:
      quoteSources = q.quote_sources.split(",")
      q.canEdit = (not user.is_anonymous() and user.username in quoteSources) or (user.is_top4())
  
   # Get paginator and page
   page = 1
   pageArg = request.GET.get("page")
   if pageArg and pageArg.isdigit():
      page = int(pageArg)
   paginator = Paginator(quote_list, 10)
   page = min(paginator.num_pages, page)
   page = max(1, page)
   quotePage = paginator.page(page)
   
   return render_to_response('intranet/quote/main.html',{"section":"intranet","page":"quote","quotePage":quotePage,"request":request,"searchArg":textSearchArg},context_instance=RequestContext(request))

def add(request):

   if request.method == 'POST':

      #-- Handle new quotes --
      # Save quote
      quoteForm = QuoteForm(request.POST)
      quoteForm.save()

      return redirect('/intranet/quote/')
   else:

      # -- Handle quote adding --
      return render_to_response('intranet/quote/add.html',{"section":"intranet","page":'quote',"form":QuoteForm(),"members":Member.objects.all()},context_instance=RequestContext(request))
      
def edit(request, quote_id = 1): 
   
   # Quote editing/modification logic
   if (request.method == 'POST') and ('delete' in request.POST):
   
      # --- Handle delete requests ---
      quoteInQuestion = Quote.objects.get(pk=quote_id)
      quoteInQuestion.delete()
      
      return redirect('/intranet/quote/')
   
   elif (request.method == 'POST'):

      # --- Handle save requests (from edit form to quote list) ---
      quoteInQuestion = Quote.objects.get(pk=quote_id)
      
      quoteForm = QuoteForm(request.POST, instance=quoteInQuestion)
      quoteForm.save()

      return redirect('/intranet/quote/')
   else:
    
       # Make sure quote editor can actually edit the current quote (and reject their request if they can't)
       user = request.user
       quoteObj = Quote.objects.filter(pk=quote_id).values()[0]
       quoteUsernames = quoteObj["quote_sources"].split(",")
       
       canEdit = (not user.is_anonymous() and user.username in quoteUsernames) or (user.is_top4())
       
       if (not canEdit):
          raise PermissionDenied # Current user cannot edit this quote
    
       # --- Handle edit page requests (from quote list to edit form) ---
       
       # Get authors' Member objects
       quoteMembers = Member.objects.filter(username__in=quoteUsernames)
       
       # Remove hashtags in text
       quoteObj["quote_text"] = string.replace(re.sub("<a href='.+'>", "", quoteObj["quote_text"]), "</a>", "")
       
       quoteForm = QuoteForm(quoteObj)
       
       # -- Handle quote editing --
       return render_to_response('intranet/quote/edit.html',{"section":"intranet","page":'quote',"form":quoteForm, "members":Member.objects.all(),"quoteMembers":quoteMembers,"quote_id":quote_id},context_instance=RequestContext(request))  
      
