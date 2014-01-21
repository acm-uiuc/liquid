from django.shortcuts import render_to_response, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from cal.make_calendar_file import make_calendar
import HTMLParser

def main(request,quote_id = 0,year=None,month=None,day=None):
  
   return make_calendar(request,year,month,day,'kiosk/main.html','kiosk',False)
