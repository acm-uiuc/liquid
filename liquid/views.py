from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import urllib
import simplejson
import datetime
from intranet.models import Event

def main(request):
   events = Event.objects.filter(endtime__gte=datetime.datetime.now()).order_by('starttime')[:5]
   return render_to_response('main.html',{"events":events},context_instance=RequestContext(request))
	
def contact(request):
   return render_to_response('contact.html',{"section":"contact"},context_instance=RequestContext(request))
  
def conference(request):
   return render_to_response('conf.html',{"section":"conference"},context_instance=RequestContext(request))
