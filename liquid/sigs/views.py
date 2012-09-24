from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from intranet.models import Group
from django import forms
from django.forms import ValidationError
import simplejson as json

# Create your views here.
def main(request):
  sigs = Group.objects.filter(type='S').filter(status='active').order_by('name')
  return render_to_response('sigs/main.html',{"section":"sigs",'sigs':sigs},context_instance=RequestContext(request))

def details(request,id):
	s = Group.objects.get(id=id)
	section = 'about'
	if s.type == 'S':
		section = 'sigs'
	return render_to_response('sigs/details.html',{"section":section,"s":s},context_instance=RequestContext(request))

def subscribe(request,id):
   s = Group.objects.get(id=id)
   email_field = forms.EmailField()
   try:
      email = email_field.clean(request.GET.get('email'))
   except ValidationError:
      response = {'Error': 'Invalid email address'}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   if s.type == 'S':
      try:
        s.subscribe(email)
        response = {'Message': 'You have been subscribed'}
        return HttpResponse(json.dumps(response), mimetype="application/json")
      except Exception as e:
        response = {'Error': "%s"%e}
        return HttpResponse(json.dumps(response), mimetype="application/json")
   else:
      raise Http404
