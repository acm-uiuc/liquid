from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from intranet.group_manager.models import Group

# Create your views here.
def main(request):
  sigs = Group.objects.filter(type='S')
  return render_to_response('sigs/main.html',{"section":"sigs",'sigs':sigs})

def details(request,id):
	g = Group.objects.get(id=id)
	section = 'about'
	if g.type == 'S':
		section = 'sigs'
	return render_to_response('sigs/details.html',{"section":section,"g":g})
