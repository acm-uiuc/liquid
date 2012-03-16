from django.shortcuts import render_to_response
from django.http import HttpResponse


# Create your views here.
def about(request):
  return render_to_response('about/about.html',{"page":'about'})
  
def join(request):
  return render_to_response('about/join.html',{"page":'join'})
  
def committees(request):
  return render_to_response('about/committees.html',{"page":'committees'})
  
def corporate(request):
  return render_to_response('about/corporate.html',{"page":'corporate'})
  
def job(request):
  return render_to_response('about/job.html',{"page":'corporate'})
  
def members(request):
  return render_to_response('about/members.html',{"page":'members'})