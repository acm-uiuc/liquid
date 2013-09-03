from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from quotedb.forms import QuoteForm
from quotedb.models import Quote
from django.conf import settings

# Create your views here.
def main(request):
     
   # Get paginator and page
   page = 1
   pageArg = request.GET.get("page")
   if pageArg and pageArg.isdigit():
      page = int(pageArg)
   paginator = Paginator(Quote.objects.all(), settings.QUOTES_PER_PAGE)
   page = min(paginator.num_pages, page)
   page = max(1, page)
   quotePage = paginator.page(page)
   
   return render_to_response('quotedb/main.html',{"section":"intranet","page":"quotedb","quotePage":quotePage,"request":request},context_instance=RequestContext(request))

def add(request):

   if request.method == 'POST':

      #-- Handle new quotes --
      quoteForm = QuoteForm(request.POST)
      quoteForm.save()

      # -- Handle old quotes --
      
      # Get paginator
      paginator = Paginator(Quote.objects.all(), settings.QUOTES_PER_PAGE)
      quotePage = paginator.page(1)

      return render_to_response('quotedb/main.html',{"section":"intranet","page":'quotedb',"quotePage":quotePage,"request":request},context_instance=RequestContext(request))
   else:
   
      # -- Handle quote adding --
      return render_to_response('quotedb/add.html',{"section":"intranet","page":'quotedb',"form":QuoteForm},context_instance=RequestContext(request))
      
# Helper function (gets a string list of quote page numbers)
def getPages():
   
   # Misc. values used to set up quote pages
   quotes_total = len(Quote.objects.all())
   page_list = "1"
   active_page = 1
   
   # Get string of quote page numbers
   while (settings.QUOTES_PER_PAGE * active_page < quotes_total):
   
      page_list = page_list + str(active_page + 1)
      active_page = active_page + 1
      
   return page_list
