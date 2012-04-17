from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from intranet.models import Group

# Create your views here.
def main(request):
  sigs = Group.objects.filter(type='S').filter(status='active')
  return render_to_response('sigs/main.html',{"section":"sigs",'sigs':sigs},context_instance=RequestContext(request))

def details(request,id):
	s = Group.objects.get(id=id)
	section = 'about'
	if s.type == 'S':
		section = 'sigs'
	return render_to_response('sigs/details.html',{"section":section,"s":s},context_instance=RequestContext(request))
