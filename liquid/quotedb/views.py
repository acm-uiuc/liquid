from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from quotedb.forms import QuoteForm
from quotedb.models import Quote
from django.conf import settings

# Create your views here.
def main(request, page_number=1):
     
   # Get paginator
   paginator = Paginator(Quote.objects.all(), settings.QUOTES_PER_PAGE)
   page_number = min(paginator.num_pages, int(page_number))
   page_number = max(1, page_number)
   quotes = paginator.page(page_number).object_list

   return render_to_response('quotedb/main.html',{"section":"quotedb","page":'main',"pageNumber":page_number,"quotes":quotes},context_instance=RequestContext(request))

def add(request):

   if request.method == 'POST':

      #-- Handle new quotes --
      quoteForm = QuoteForm(request.POST)
      quoteForm.save()

      # -- Handle old quotes --
      
      # Get paginator
      paginator = Paginator(Quote.objects.all(), settings.QUOTES_PER_PAGE)
      quotes = paginator.page(1).object_list

      return render_to_response('quotedb/main.html',{"section":"quotedb","page":'main',"pageNumber":1,"quotes":quotes},context_instance=RequestContext(request))
   else:
   
      # -- Handle quote adding --
      return render_to_response('quotedb/add.html',{"section":"quotedb","page":'add',"form":QuoteForm},context_instance=RequestContext(request))
      
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
   
# Helper function #2 (gets a list of quotes given the request parameters)
def getQuotes(request):

   # Misc. values used to set up quote pages
   quotes_total = len(Quote.objects.all())
   page_list = "1"
   active_page = 1

   # Get page number
   pages = getPages()
   page_number = ""
   page_number_request = request.GET.get("page")
   if page_number_request == None or not page_number_request.isdigit():
      page_number = 1
   else:
      page_number = int(page_number_request)

   # Filter quotes according to page number
   quote_start_index = (page_number - 1) * settings.QUOTES_PER_PAGE
   quote_end_index = min(page_number * settings.QUOTES_PER_PAGE, quotes_total)

   return Quote.objects.all().order_by("-created_at")[quote_start_index:quote_end_index]
