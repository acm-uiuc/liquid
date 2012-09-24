from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django import forms
from django.forms import ValidationError
import simplejson as json
from utils.ip_decorator import ips_required, password_get
import settings

# Create your views here.
@ips_required(settings.CRON_IPS)
@password_get(settings.CRON_PASSWORD)
def job_email(request):
   pass
   