from django.shortcuts import render_to_response
from django.http import HttpResponse
from intranet.models import Event
from django.template import RequestContext
import datetime


# Create your views here.
def main(request):
   futer = datetime.datetime.now() + datetime.timedelta(days=7)
   events = Event.objects.filter(endtime__gte=datetime.datetime.now()).filter(starttime__lte=futer).order_by('starttime')
   return render_to_response('cal/main.html',{"section":"calendar","events":events},context_instance=RequestContext(request))
   
def details(request,id):
   event = Event.objects.get(id=id)
   return render_to_response('cal/details.html',{"section":"calendar","event":event},context_instance=RequestContext(request))