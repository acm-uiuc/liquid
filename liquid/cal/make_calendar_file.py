# This file exists so the calendar can be reused on static pages throughout the website
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from intranet.models import Event
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def make_calendar(request,year,month,day,url,section,show_navigation_urls):
   if year is None:
      start_date = datetime.date.today()
   elif int(year) < 1900 or int(year) > 2100:
     raise Http404
   else:
     try:
       start_date = datetime.date(int(year),int(month),int(day))
     except ValueError:
       raise Http404
   this_week_monday = start_date - datetime.timedelta(days=start_date.weekday())
   two_weeks = this_week_monday + datetime.timedelta(days=14)
   events = Event.objects.filter(endtime__gte=this_week_monday,starttime__lte=two_weeks).order_by('starttime')

   events_grouped = []
   dates = []
   for i in range(12):
      if i > 5:
         i+=1
      date = this_week_monday + datetime.timedelta(days=i)
      date_label = date.strftime('%b. %d')
      if i == 5 or i == 12:
         date_label += (date + datetime.timedelta(days=1)).strftime(' & %d')
      events_grouped.append({'events':[],'date':date_label})


   for e in events:
      date_offset = get_offset(e.starttime.date(),this_week_monday)
      events_grouped[date_offset]['events'].append(e)

   today_offset = get_offset(datetime.date.today(),this_week_monday,True)

   prev_date = this_week_monday - datetime.timedelta(days=7)
   prev_url = None
   if show_navigation_urls and prev_date.year > 1900:
     prev_url =  "/calendar/%d/%d/%d"%(prev_date.year,prev_date.month,prev_date.day)
   next_date = this_week_monday + datetime.timedelta(days=7)
   next_url = None
   if show_navigation_urls and next_date.year < 2100:
     next_url = "/calendar/%d/%d/%d"%(next_date.year,next_date.month,next_date.day)

   return render_to_response(url,{"section":section,"events_grouped":events_grouped,"events":events,"today_offset":today_offset,"prev_url":prev_url,"next_url":next_url,"show_navigation_urls":show_navigation_urls},context_instance=RequestContext(request))

def get_offset(date,from_date,can_neg=False):
   date_offset = (date-from_date).days
   if date_offset < 0 and not can_neg:
      date_offset = 0
   if date_offset == 6 or date_offset == 13:
      date_offset -= 1
   if date_offset > 6:
         date_offset -= 1
   return date_offset
