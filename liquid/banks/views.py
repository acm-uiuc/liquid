from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext



# Create your views here.
def main(request):
  return render_to_response('banks/main.html',{"section":"banks","page":'main'},context_instance=RequestContext(request))