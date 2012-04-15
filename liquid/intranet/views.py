from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def main(request):
  return render_to_response('intranet/main.html',{"section":"intranet","page":'main'},context_instance=RequestContext(request))
  
def faq(request):
  return render_to_response('intranet/faq.html',{"section":"intranet","page":'faq'},context_instance=RequestContext(request))
 