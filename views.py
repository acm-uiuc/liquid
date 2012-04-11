from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import urllib
import simplejson

def main(request):
  return render_to_response('main.html',{},context_instance=RequestContext(request))
	
def contact(request):
  return render_to_response('contact.html',{"section":"contact"},context_instance=RequestContext(request))

