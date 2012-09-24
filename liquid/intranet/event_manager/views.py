from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.contrib import messages
from intranet.models import Event
from intranet.event_manager.forms import EventForm
import datetime
from utils.group_decorator import is_admin


# Create your views here.
@is_admin()
def main(request):
  events = Event.objects.filter(endtime__gte=datetime.datetime.now()).order_by('starttime')


  seven_days = datetime.timedelta(days=7)
  next_week = datetime.datetime.now() + seven_days
  mail_events = Event.objects.filter(endtime__gte=datetime.datetime.now()).filter(starttime__lte=next_week).order_by('starttime')

  mail_text = "Schedule for the week:\n"

  i = 1
  for e in mail_events:
     mail_text += "%d. %s - %s\n" %(i,e.name,e.starttime.strftime('%m/%d/%y'))
     i += 1

  for e in mail_events:
     mail_text += "\n========================================================================\n\n"
     
     mail_text += "%s\n%s\n%s\n\n%s" % (e.name,e.pretty_time(),e.location,e.description)
  mail_text += "\n\n========================================================================\n\n"


  mail_subject = "Events of the week, %s"%(datetime.date.today().strftime("%m/%d/%y"))

  return render_to_response('intranet/event_manager/main.html',{
    "section":"intranet",
    "page":'event',
    'events':events,
    "mail_text":mail_text,
    "mail_subject":mail_subject,
    "user": request.user
  },context_instance=RequestContext(request))

@is_admin()
def new(request):
   if request.method == 'POST': # If the form has been submitted...
      e = Event(creator=request.user)
      form = EventForm(request.POST,instance=e) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
         form.save()
         messages.add_message(request, messages.SUCCESS, 'Event created')
         return HttpResponseRedirect('/intranet/event') # Redirect after POST    
   else:
      form = EventForm() # An unbound form

   return render_to_response('intranet/event_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":'event',
      "page_title":"Create new Event"
    },context_instance=RequestContext(request))

@is_admin()
def edit(request,id):
  e = Event.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    form = EventForm(request.POST,instance=e) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Event changed')
      return HttpResponseRedirect('/intranet/event') # Redirect after POST
  else:
    form = EventForm(instance=e)

  
  return render_to_response('intranet/event_manager/form.html',{
    "form":form,
    "section":"intranet",
    "page":'event',
    "page_title":"Edit Event",
    },context_instance=RequestContext(request))

@is_admin()
def delete(request,id):
  e = Event.objects.get(id=id)
  e.delete()
  messages.add_message(request, messages.SUCCESS, 'Event deleted')
  return HttpResponseRedirect('/intranet/event')


