from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.views import login
from django.http import HttpResponse, Http404
from django import forms
from django.forms import ValidationError
from utils.django_mailman.models import List
from utils.group_decorator import group_admin_required
import simplejson as json

def main(request):
   return render_to_response('conference/landing.html',{},context_instance=RequestContext(request))

def jobfair(request):
    if request.user.is_authenticated():
        return jobfair_invite(request)
    else:
        return login(request,'conference/job-fair-login.html')

@group_admin_required(['Conference', '!Company'])
def jobfair_invite(request):
    return render_to_response('conference/job-fair-invite.html',{},context_instance=RequestContext(request))

def subscribe(request):
   email_field = forms.EmailField()
   try:
      email = email_field.clean(request.GET.get('email'))
   except ValidationError:
      response = {'Error': 'Invalid email address.'}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   try:
      s = List.objects.get(name='RP-announce')
      s.subscribe_email(email)
      response = {'Message': 'You have been subscribed.'}
      return HttpResponse(json.dumps(response), mimetype="application/json")
   except Exception as e:
      response = {'Error': "%s"%e}
      return HttpResponse(json.dumps(response), mimetype="application/json")

