from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django import forms
from django.forms import ValidationError
from utils.django_mailman.models import List
import simplejson as json

def main(request):
   return render_to_response('conference/landing.html',{"section":"conference","page":'main'},context_instance=RequestContext(request))

def subscribe(request):
   email_field = forms.EmailField()
   try:
      email = email_field.clean(request.GET.get('email'))
   except ValidationError:
      response = {'Error': 'Invalid email address'}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   try:
      s = List.objects.get(name='RP-announce')
      s.subscribe_email(email)
      response = {'Message': 'You have been subscribed'}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   except Exception as e:
      response = {'Error': "%s"%e}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   else:
      raise Http404

