from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf

# Create your views here.
def main(request):
  return render_to_response('intranet/banks_manager/main.html',{"page":'banks'})