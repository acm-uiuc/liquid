from django.shortcuts import render_to_response
from intranet.models import Job
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from intranet.job_manager.forms import JobFormSet
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
from django.core.mail import send_mail
from scripts.send_job_email import send_email

@group_admin_required(['Corporate'])
def main(request):
   if request.method == 'POST':
      formset = JobFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
   unsent_jobs = Job.objects.filter(sent__exact=False).filter(status__exact='approve')
   def_jobs = Job.objects.filter(sent__exact=False).filter(status__exact='defer')
   formset = JobFormSet(queryset=def_jobs)
   return render_to_response('intranet/job_manager/main.html',{"section":"intranet","page":'jobs',"job_count":len(unsent_jobs), "def_job_count":len(def_jobs), "jobs":formset},context_instance=RequestContext(request))

@group_admin_required(['Top4'])
def send_job_email(request):
  send_email()
  return HttpResponseRedirect('/intranet/jobs')
