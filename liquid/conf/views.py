from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.views import login
from django.http import HttpResponse, Http404
from django import forms
from django.forms import ValidationError
from conf.models import Company
from utils.django_mailman.models import List
from utils.group_decorator import group_admin_required, check_group_admin
import simplejson as json

def main(request):
	return render_to_response('conf/main.html',{"section":"conf", "page":"main"},context_instance=RequestContext(request))

def jobfair(request):
    if request.user.is_authenticated() and check_group_admin(['Conference', '!Company'], request):
        return jobfair_invite(request)
    else:
        return login(request,'conf/job-fair-login.html',extra_context={'is_authed': request.user.is_authenticated()})

@group_admin_required(['Conference', '!Company'])
def jobfair_invite(request):
    company = get_object_or_404(Company, username=request.user.username)
    return render_to_response('conf/job-fair-invite.html',
                              {"company" : company,
                               "STARTUP": Company.STARTUP,
                               "JOBFAIR": Company.JOBFAIR},
                              context_instance=RequestContext(request))
