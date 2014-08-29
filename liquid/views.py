from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import urllib
import simplejson
import datetime
from intranet.models import Event

def main(request):
   next_seven_days = datetime.date.today() + datetime.timedelta(days=5)
   events = Event.objects.filter(endtime__gte=datetime.date.today(),starttime__lte=next_seven_days).order_by('starttime')

   event_days = []
   for i in range(5):
      event_days.append({'date':datetime.date.today() + datetime.timedelta(days=i),'events':[]})

   for e in events:
      event_offset = (e.starttime.date() - datetime.date.today()).days
      if event_offset < 0:
         event_offset = 0
      event_days[event_offset]['events'].append(e)

   return render_to_response('main.html',{"event_days":event_days,"events":events},context_instance=RequestContext(request))
	
def contact(request):
   return render_to_response('contact.html',{"section":"contact"},context_instance=RequestContext(request))
  
def conference(request):
   return render_to_response('conf.html',{"section":"conference"},context_instance=RequestContext(request))

def vpnRequired(request):
   return render_to_response('vpn_required.html')
