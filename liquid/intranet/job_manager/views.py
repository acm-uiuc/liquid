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
import sys,os
import time
from datetime import date
from textwrap import wrap

@group_admin_required(['Corporate'])
def main(request):
   if request.method == 'POST':
      formset = JobFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
   jobs = Job.objects.filter(sent__exact=False).filter(status__exact='defer')
   formset = JobFormSet(queryset=jobs)
   return render_to_response('intranet/job_manager/main.html',{"section":"intranet","page":'jobs',"job_count":len(jobs),"jobs":formset},context_instance=RequestContext(request))

#no admin for now...
def send_email(request):
  jobs = Job.objects.filter(sent__exact=False).filter(status__exact='approve')

  if jobs:

    today = date.today()

    email = "ACM@UIUC Weekly Job Postings\r\nWeek of " + today.strftime("%m/%d/%y") + "\r\n\r\n"
    email += "With postings from:\r\n"
    #post header
    for j in jobs:
      email += "* " + j.company + "\r\n"

      email += "\r\n========================================================================\r\n\r\n";
    #job listing
    for j in jobs:
      email += "Title: " + j.job_title + "\r\n"
      email += "Company: " + j.company + "\r\n";
      email += "Contact: " + j.contact_name +  ' <' + j.contact_email + '> ' + j.contact_phone + "\r\n"
      email += "Hiring for: " + j.types() + "\r\n"
      description = j.description.split('\n')
      description_out = ""
      for d in description:
        if d != "":
          description_out += "\r\n".join(wrap(d,72)) + "\r\n"
          email += "Description:\r\n" + description_out + "\r\n";
          email += "\r\n========================================================================\r\n\r\n";


    try:
      send_mail('ACM@UIUC Weekly Job Postings', email, 'ACM Corporate Committee <corporate@acm.uiuc.edu>',['bjryan2@illinois.edu', 'ryan.brendanjohn@gmail.com'], fail_silently=False)
      print "Email sent"
      for j in jobs:
        j.sent = True
        j.save()
    except Exception as inst:
      print "Error sending email"
      print inst

  else:
    print "No jobs to send"
  print("--Email Sent!!!--")
  return HttpResponseRedirect('/intranet/jobs')
