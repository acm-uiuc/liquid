from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from intranet.models import Job
from intranet.models import Resume

from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
# Create your views here.
def main(request):
   groups = request.user.group_set.all()
   unsent_jobs = Job.objects.filter(sent__exact=False).filter(status__exact="approve")
   pend_jobs = Job.objects.filter(sent__exact=False).filter(status__exact="defer")
   resumes = Resume.objects.filter(approved__exact=False)

   return render_to_response('intranet/main.html',{"section":"intranet","page":'main',"groups":groups, "unsent_jobs_count":len(unsent_jobs), "pend_jobs_count":len(pend_jobs),"resume_count":len(resumes)} ,context_instance=RequestContext(request))
