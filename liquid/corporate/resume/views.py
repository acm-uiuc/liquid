from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail
from corporate.resume.forms import ResumePersonForm, ResumeForm
from intranet.models import Member
from intranet.models import Group
from intranet.models import ResumePerson, Resume
from django.forms.util import ErrorList
import settings



# Create your views here.
def main(request):
  return render_to_response('corporate/resume/main.html',{"section":"corporate"},context_instance=RequestContext(request))

def student_thanks(request,id):
  try:
    r = Resume.objects.get(id=id)
    r.generate_thumbnails()
  except:
    pass
  return render_to_response('corporate/resume/student_thanks.html',{"section":"corporate"},context_instance=RequestContext(request))


def student(request):
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
        return HttpResponseRedirect("/corporate/resume/student/thanks/%d"%(resume.id)) # Redirect after POST
      except ValueError:
        errors = resume_person_form._errors.setdefault("netid", ErrorList())
        errors.append(u"Not a valid netid")
  else:
    resume_person_form = ResumePersonForm()
    resume_form = ResumeForm()

  return render_to_response('corporate/resume/student.html',{
      'resume_form': resume_form,
      'resume_person_form': resume_person_form,
      'section': "corporate",
    },context_instance=RequestContext(request))
      

