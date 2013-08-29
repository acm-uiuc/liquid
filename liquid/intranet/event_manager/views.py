from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail
from intranet.models import Event
from intranet.event_manager.forms import EventForm
from utils.group_decorator import group_admin_required
from utils.group_decorator import is_admin
from scripts.events_email import gen_email
import datetime



# Create your views here.
@is_admin()
def main(request):
  events = Event.objects.filter(endtime__gte=datetime.datetime.now()).order_by('starttime')
  mail_text = gen_email()
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

@group_admin_required(['top4'])
def send_email(request):
  email = gen_email()
  addr = request.user.email
  send_mail('ACM@UIUC Weekly Event Email', email, addr ,['membership-l@acm.uiuc.edu'], fail_silently=False)
  messages.add_message(request, messages.SUCCESS, "Email Successfully Sent!")
  return HttpResponseRedirect('/intranet/event')

