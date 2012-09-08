from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.mail import send_mail
from corporate.resume.forms import ResumePersonForm, ResumeForm
from intranet.models import Member
from intranet.models import Group
from intranet.models import ResumePerson, Resume, ResumeDownloadSet, ResumeDownload
from django.forms.util import ErrorList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import settings
import pyPdf



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


def recruiter(request):
  return render_to_response('corporate/resume/recruiter.html',{"section":"corporate","page":"download"},context_instance=RequestContext(request))

def recruiter_browse(request):
  q = request.GET.get('q')
  if q==None:
    q = ""
  level = request.GET.getlist('level')
  seeking = request.GET.getlist('seeking')
  acm = request.GET.get('acm') == "yes"
  graduation_start = request.GET.get('graduation_start')
  graduation_end = request.GET.get('graduation_end')

  if graduation_start == "":
    graduation_start = None

  if graduation_end == "":
    graduation_end = None

  level_str = None
  if len(level) > 0:
    level_str = "".join(level)

  seeking_str = None
  if len(seeking) > 0:
    seeking_str = "".join(seeking)

  set = ResumeDownloadSet(level=level_str,seeking=seeking_str,acm=acm,graduation_start=graduation_start,graduation_end=graduation_end)

  people = set.get_people(Q(netid__icontains=q) | \
                                    Q(first_name__icontains=q) | \
                                    Q(last_name__icontains=q))

  paginator = Paginator(people, 25) # Show 25 contacts per page
  total_people = paginator.count

  page = request.GET.get('page')
  try:
      people = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      people = paginator.page(1)
  except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      people = paginator.page(paginator.num_pages)

  graduation_choices = ResumePerson.RESUME_PERSON_GRADUATION

  

  return render_to_response('corporate/resume/recruiter_browse.html',{"section":"corporate","page":"browse","people":people,"q":q,"set":set,"total_people":total_people,"graduation_choices":graduation_choices,"request":request},context_instance=RequestContext(request))

def recruiter_pdf(request,netid):
  person = ResumePerson.objects.filter(netid=netid)[0]
  r = person.latest_resume()
  pdf_data = open(r.resume.path, "rb").read()
  return HttpResponse(pdf_data, mimetype="application/pdf")

def recruiter_download(request):
  pass

def recruiter_download_pdf(request,id):
  pdf_out = pyPdf.PdfFileWriter()

  for p in people:
    pdf_in = pyPdf.PdfFileReader(file(p.latest_resume().path,"rb"))

    for page in range(pdf_in.getNumPages()):
      pdf_out.addPage(pdf_in.getPage(page))

