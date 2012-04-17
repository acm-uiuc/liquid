from django.shortcuts import render_to_response
from django.http import HttpResponse
from intranet.models import Event
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime


# Create your views here.
def main(request,page=1):
   events = Event.objects.filter(endtime__gte=datetime.datetime.now()).order_by('starttime')
   paginator = Paginator(events, 10)
   
   try:
      events = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      events = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      events = paginator.page(paginator.num_pages)

   return render_to_response('cal/main.html',{"section":"calendar","events":events},context_instance=RequestContext(request))
   
def details(request,id):
   event = Event.objects.get(id=id)
   return render_to_response('cal/details.html',{"section":"calendar","event":event},context_instance=RequestContext(request))