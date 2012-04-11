from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from intranet.event_manager.models import Event
from intranet.event_manager.forms import EventForm
import datetime


# Create your views here.
def main(request):
  events = Event.objects.filter(endtime__gte=datetime.datetime.now).order_by('starttime')
  return render_to_response('intranet/event_manager/main.html',{"section":"intranet","page":'event','events':events},context_instance=RequestContext(request))

def new(request):
  if request.method == 'POST': # If the form has been submitted...
    form = EventForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      form.save()
      return HttpResponseRedirect('/intranet/event') # Redirect after POST    
  else:
    form = EventForm() # An unbound form

  return render_to_response('intranet/event_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":'event',
      "page_title":"Create new Event"
    },context_instance=RequestContext(request))

def edit(request,id):
  e = Event.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    form = EventForm(request.POST,instance=e) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      form.save()
      return HttpResponseRedirect('/intranet/event') # Redirect after POST
  else:
    form = EventForm(instance=e)

  
  return render_to_response('intranet/event_manager/form.html',{
    "form":form,
    "section":"intranet",
    "page":'event',
    "page_title":"Edit Event",
    },context_instance=RequestContext(request))

def delete(requset,id):
  e = Event.objects.get(id=id)
  e.delete()
  return HttpResponseRedirect('/intranet/event')


