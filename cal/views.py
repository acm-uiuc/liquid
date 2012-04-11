from django.shortcuts import render_to_response
from django.http import HttpResponse
from intranet.event_manager.models import Event
from django.template import RequestContext


# Create your views here.
def main(request):
  events = Event.objects.all()
  return render_to_response('cal/main.html',{"section":"calendar","page":'main',"events":events},context_instance=RequestContext(request))