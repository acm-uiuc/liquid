from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.views import login
from django.http import HttpResponse, Http404
from django import forms
from django.forms import ValidationError
from conference.models import Company
from utils.django_mailman.models import List
from utils.group_decorator import group_admin_required
import simplejson as json

def jobfair(request):
    if request.user.is_authenticated():
        return jobfair_invite(request)
    else:
        return login(request,'conference/job-fair-login.html')

@group_admin_required(['Conference', '!Company'])
def jobfair_invite(request):
    company = get_object_or_404(Company, username=request.user.username)
    return render_to_response('conference/job-fair-invite.html',
                              {"company" : company,
                               "STARTUP": Company.STARTUP,
                               "JOBFAIR": Company.JOBFAIR},
                              context_instance=RequestContext(request))
