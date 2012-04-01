from django.shortcuts import render_to_response
from django.http import HttpResponse
import urllib
import simplejson

def main(request):
  user = None
  if 'REMOTE_USER' in request.META:
    user = request.META['REMOTE_USER']
  return render_to_response('main.html',{'user':user})
	
def contact(request):
  return render_to_response('contact.html',{"section":"contact"})
	

