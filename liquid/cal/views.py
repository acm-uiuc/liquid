from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from intranet.models import Event
from cal.make_calendar_file import make_calendar
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

# Create your views here.
def main(request,year=None,month=None,day=None):

   # See make_calendar_file.py
   return make_calendar(request,year,month,day,'cal/main.html','calendar',True)

def details(request,id):
   try:
      event = Event.objects.get(id=id)
      start_date = event.starttime.date()
      this_week_monday = start_date - datetime.timedelta(days=start_date.weekday())
      return HttpResponseRedirect("/calendar/%d/%d/%d#details/%d"%(this_week_monday.year,this_week_monday.month,this_week_monday.day,event.id))
   except Event.DoesNotExist:
      raise Http404
