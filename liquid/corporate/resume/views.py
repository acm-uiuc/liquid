from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from corporate.resume.forms import ResumePersonForm, ResumeForm, EmailChangeForm, PreResumePersonForm
from intranet.models import Member
from intranet.models import Group
from intranet.models import ResumePerson, Resume, ResumeDownloadSet, ResumeDownload, PreResumePerson
from django.forms.util import ErrorList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.group_decorator import group_admin_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import settings
import operator
import pyPdf

def student_thanks(request,id):
  try:
    r = Resume.objects.get(id=id)
    r.generate_thumbnails()
  except:
    pass
  return render_to_response('corporate/resume/student_thanks.html',{"section":"corporate"},context_instance=RequestContext(request))


def main(request):
  if request.user.groups.filter(name='Recruiter').count() > 0:
    return HttpResponseRedirect("/corporate/resume/recruiter/")

  if request.method == 'POST' and request.POST.get('student')=="yes":
    resume_form = ResumeForm(request.POST,request.FILES)
    resume_person_form = ResumePersonForm(request.POST)

    if resume_person_form.is_valid() and resume_form.is_valid():
      try:
        rp = ResumePerson.objects.get(netid=resume_person_form.cleaned_data['netid'].lower())
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

  if request.method == "POST" and request.POST.get('recruiter')=="yes":
    login_form = AuthenticationForm(data=request.POST)
    if login_form.is_valid():
      login(request, login_form.get_user())
      return HttpResponseRedirect("/corporate/resume/recruiter/") # Redirect after POST
  else:
    login_form = AuthenticationForm()

  return render_to_response('corporate/resume/main.html',{
      'resume_form': resume_form,
      'resume_person_form': resume_person_form,
      'login_form': login_form,
      'section': "corporate",
    },context_instance=RequestContext(request))


def student_rp(request):
  if request.method == 'POST':
    pre_resume_person_form = PreResumePersonForm(request.POST)

    if pre_resume_person_form.is_valid():
      try:
        rp = PreResumePerson.objects.get(netid=pre_resume_person_form.cleaned_data['netid'].lower())
        messages.add_message(request, messages.ERROR, 'We already have your resume, no need to give it to us today!')  
        pre_resume_person_form = PreResumePersonForm()
      except:
        try:
          pre_resume_person_form.save()
          messages.add_message(request, messages.SUCCESS, 'Thanks, your resume will be added.')  
          pre_resume_person_form = PreResumePersonForm()
        except ValueError:
          errors = pre_resume_person_form._errors.setdefault("netid", ErrorList())
          errors.append(u"Not a valid netid")
  else:
    pre_resume_person_form = PreResumePersonForm()

  return render_to_response('corporate/resume/student_rp.html',{
      'pre_resume_person_form': pre_resume_person_form,
      'section': "corporate",
    },context_instance=RequestContext(request))

@group_admin_required(['Corporate','!Recruiter'])  
def recruiter(request):
  sets = ResumeDownloadSet.objects.filter(owner=request.user)

  return render_to_response('corporate/resume/recruiter.html',{"section":"corporate","page":"download","sets":sets},context_instance=RequestContext(request))

@group_admin_required(['Corporate','!Recruiter'])
def recruiter_help(request):
  return render_to_response('corporate/resume/recruiter_help.html',{"section":"corporate","page":"help"},context_instance=RequestContext(request))

@group_admin_required(['Corporate','!Recruiter'])
def recruiter_browse(request):
  q = request.GET.get('q')
  if q==None:
    q = ""
  level = request.GET.getlist('level')
  level.sort()
  seeking = request.GET.getlist('seeking')
  seeking.sort()
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

  sets = ResumeDownloadSet.objects.filter(level=level_str,seeking=seeking_str,acm=acm,graduation_start=graduation_start,graduation_end=graduation_end,owner=request.user)
  if sets.count() > 0:
    set = sets[0]
  else:
    set = ResumeDownloadSet(level=level_str,seeking=seeking_str,acm=acm,graduation_start=graduation_start,graduation_end=graduation_end)

  if request.GET.get('download') == "true":
    set.owner = request.user
    set.save()
    download = set.generate_download()
    return HttpResponseRedirect('/corporate/resume/recruiter/download/%d.pdf'%(download.id))

  if q != "":
    queries = q.split()
    qset1 =  reduce(operator.__or__, [Q(netid__icontains=q) | Q(first_name__icontains=query) | Q(last_name__icontains=query) for query in queries])
    people = set.get_people(qset1)
  else:
    people = set.get_people()

  num_per_page = request.GET.get('num_per_page')
  if num_per_page==None:
    num_per_page = 50
  else:
    num_per_page = int(num_per_page)
  # Show requested number of resumes per page (50 by default)
  paginator = Paginator(people, num_per_page)
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

  

  return render_to_response('corporate/resume/recruiter_browse.html',{
    "section":"corporate",
    "page":"browse",
    "people":people,
    "q":q,
    "set":set,
    "total_people":total_people,
    "graduation_choices":graduation_choices,
    "num_per_page": num_per_page,
    "request":request
  },context_instance=RequestContext(request))

@group_admin_required(['Corporate','!Recruiter']) 
def recruiter_generate(request,id,diff=False):
  try:
    set = ResumeDownloadSet.objects.get(id=id)
    download = set.generate_download()
    if diff:
      return HttpResponseRedirect('/corporate/resume/recruiter/download/diff/%d.pdf'%(download.id))
    else:
      return HttpResponseRedirect('/corporate/resume/recruiter/download/%d.pdf'%(download.id))
  except ResumeDownloadSet.DoesNotExist:
    raise Http404

def recruiter_generate_diff(request,id):
  return recruiter_generate(request,id,True)

@group_admin_required(['Corporate','!Recruiter']) 
def recruiter_pdf(request,netid):
  person = ResumePerson.objects.get(netid=netid)
  r = person.latest_resume()
  pdf_data = open(r.resume.path, "rb").read()
  return HttpResponse(pdf_data, mimetype="application/pdf")

@group_admin_required(['Corporate','!Recruiter']) 
def recruiter_download_pdf(request,id):
  try:
    download = ResumeDownload.objects.get(id=id)
    download.generate()
    pdf_data = open(download.file_path(), "rb").read()
    return HttpResponse(pdf_data, mimetype="application/pdf")
  except ResumeDownload.DoesNotExist:
    raise Http404

@group_admin_required(['Corporate','!Recruiter']) 
def recruiter_download_pdf_diff(request,id):
  try:
    download = ResumeDownload.objects.get(id=id)
    download.generate_diff()
    pdf_data = open(download.diff_file_path(), "rb").read()
    return HttpResponse(pdf_data, mimetype="application/pdf")
  except ResumeDownload.DoesNotExist:
    raise Http404

@group_admin_required(['!Recruiter'])
def recruiter_account(request):
  if request.method == "POST" and request.POST.get('password_change')=="yes":
    password_form = PasswordChangeForm(request.user, data=request.POST)
    if password_form.is_valid():
      password_form.save()
      messages.add_message(request, messages.SUCCESS, 'Password changed')
  else:
    password_form = PasswordChangeForm(request.user)

  if request.method == "POST" and request.POST.get('email_change')=="yes":
    email_form = EmailChangeForm(request.POST,instance=request.user)
    if email_form.is_valid():
      email_form.save()
      messages.add_message(request, messages.SUCCESS, 'Email changed')
  else:
    email_form = EmailChangeForm(instance=request.user)
  
  return render_to_response('corporate/resume/recruiter_account.html',{
    "section":"corporate",
    "page":"account",
    "account": request.user,
    "password_form": password_form,
    "email_form": email_form,
  },context_instance=RequestContext(request))


