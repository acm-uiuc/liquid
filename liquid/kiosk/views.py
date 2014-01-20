from django.shortcuts import render_to_response, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
import HTMLParser

def main(request, quote_id = 0):
  
   return render_to_response('intranet/quote/edit.html',{},context_instance=RequestContext(request))
