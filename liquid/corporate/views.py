from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail
from corporate.forms import JobForm
from intranet.models import Member
from intranet.models import Group
from django.forms.util import ErrorList
import settings



# Create your views here.
def main(request):
  return render_to_response('corporate/main.html',{"section":"corporate"},context_instance=RequestContext(request))
  
def job(request):
  c = {}
  c.update(csrf(request))
  if request.method == 'POST': # If the form has been submitted...
      form = JobForm(request.POST) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          job = form.save()
          email = "A new job post for " +  job.job_title + " at " + job.company + " was just posted.  To approve this posting, use the admin interface at http://acm.uiuc.edu/intranet/jobs/"
          send_mail('New Job Post', email, 'ACM Corporate Committee <corporate@acm.uiuc.edu>',['corporate-l@acm.uiuc.edu'], fail_silently=False)
          return HttpResponseRedirect('/corporate/job/thanks/') # Redirect after POST
  else:
      form = JobForm() # An unbound form

  return render_to_response('corporate/job.html',{
      'form': form,
      "section":"corporate",
  },context_instance=RequestContext(request))

def thanks(request):
  return render_to_response('corporate/thanks.html',{"section":"corporate"},context_instance=RequestContext(request))

def resume_student_thanks(request):
  return render_to_response('corporate/resume_student_thanks.html',{"section":"corporate"},context_instance=RequestContext(request))


def resume_student(request):
  if request.method == 'POST':
    resume_form = ResumeForm(request.POST,request.FILES)
    resume_person_form = ResumePersonForm(request.POST)

    if resume_person_form.is_valid() and resume_form.is_valid():
      try:
        rp = ResumePerson.objects.get(netid=resume_person_form.cleaned_data['netid'])
        resume_person_form = ResumePersonForm(request.POST,instance=rp)
      except:
        pass
      try:
        resume_person = resume_person_form.save()
          
        resume = resume_form.save(commit=False)
        resume.person = resume_person
        resume.save()
        return HttpResponseRedirect('/corporate/resume/student/thanks/') # Redirect after POST
      except ValueError:
        errors = resume_person_form._errors.setdefault("netid", ErrorList())
        errors.append(u"Not a valid netid")
  else:
    resume_person_form = ResumePersonForm()
    resume_form = ResumeForm()

  return render_to_response('corporate/resume_student.html',{
      'resume_form': resume_form,
      'resume_person_form': resume_person_form,
      'section': "corporate",
    },context_instance=RequestContext(request))
      

