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
