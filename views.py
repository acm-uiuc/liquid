from django.shortcuts import render_to_response
from django.http import HttpResponse
import urllib
import simplejson

def main(request):
  return render_to_response('main.html',{'user':request.user})
	
def contact(request):
  return render_to_response('contact.html',{"section":"contact"})
	

