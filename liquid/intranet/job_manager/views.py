from django.shortcuts import render_to_response
from intranet.models import Job
from django.template import RequestContext
from intranet.job_manager.forms import JobFormSet


# Create your views here.
def main(request):
   if request.method == 'POST':
      formset = JobFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
   jobs = Job.objects.filter(sent__exact=False).filter(status__exact='differ')
   formset = JobFormSet(queryset=jobs)
   return render_to_response('intranet/job_manager/main.html',{"section":"intranet","page":'jobs',"jobs":formset},context_instance=RequestContext(request))