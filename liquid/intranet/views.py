from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def main(request):
   groups = request.user.group_set.all()
   return render_to_response('intranet/main.html',{"section":"intranet","page":'main',"groups":groups},context_instance=RequestContext(request))
