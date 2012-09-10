from django.shortcuts import render_to_response
from intranet.models import Resume
from django.template import RequestContext
from django.contrib import messages
from intranet.models import Recruiter
from django.core.mail import send_mail
from intranet.resume_manager.forms import ResumeFormSet, RecruiterForm
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect


@group_admin_required(['Corporate'])
def main(request):
   if request.method == 'POST':
      formset = ResumeFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
   resumes = Resume.objects.filter(approved__exact=False)
   formset = ResumeFormSet(queryset=resumes)
   return render_to_response('intranet/resume_manager/main.html',{"section":"intranet","page":"resume","sub_page":"resumes","resume_count":len(resumes),"resumes":formset},context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def thumb(request,id):
   try:
      r = Resume.objects.get(id=id)
      r.generate_thumbnails()
      image_data = open(r.thumbnail_location(), "rb").read()
      return HttpResponse(image_data, mimetype="image/png")
   except:
      raise Http404

@group_admin_required(['Corporate'])
def thumb_top(request,id):
   r = Resume.objects.get(id=id)
   r.generate_thumbnails()
   image_data = open(r.thumbnail_top_location(), "rb").read()
   return HttpResponse(image_data, mimetype="image/png")

@group_admin_required(['Corporate'])
def pdf(request,id):
   r = Resume.objects.get(id=id)
   r.generate_thumbnails()
   pdf_data = open(r.resume.path, "rb").read()
   return HttpResponse(pdf_data, mimetype="application/pdf")

@group_admin_required(['Corporate'])
def accounts(request,):
   recrutiers = Recruiter.objects.all()
   paginator = Paginator(recrutiers, 25) # Show 25 contacts per page
   
   total_recruiters = paginator.count

   page = request.GET.get('page')
   try:
      recrutiers = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      recrutiers = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      recrutiers = paginator.page(paginator.num_pages)

   return render_to_response('intranet/resume_manager/accounts.html',{
      "section":"intranet",
      "page":"resume",
      "sub_page":"accounts",
      "total_recruiters":total_recruiters,
      "recrutiers":recrutiers
   },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def accounts_new(request):
   if request.method == 'POST': # If the form has been submitted...
      e = Recruiter()
      form = RecruiterForm(request.POST,instance=e) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
         recruiter = form.save()
         password = Recruiter.objects.make_random_password()
         print password
         recruiter.set_password(password)
         recruiter.save()
         email = "Hi %s,\n\nA new account for you to access the ACM@UIUC resume book has been created.\n\nUsername: %s\nPassword: %s\n\nTo login visit http://acm.uiuc.edu/resume.\n\nThanks,\nACM@UIUC Corporate Committee"%(recruiter.first_name,recruiter.username,password)
         send_mail('ACM@UIUC Resume Book', email, 'ACM Corporate Committee <corporate@acm.uiuc.edu>',[recruiter.email,'corporate@acm.uiuc.edu'], fail_silently=False)
         messages.add_message(request, messages.SUCCESS, 'Recruiter created (%s, %s)'%(recruiter.username, password))
         return HttpResponseRedirect('/intranet/resume/accounts') # Redirect after POST    
   else:
      form = RecruiterForm() # An unbound form

   return render_to_response('intranet/event_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":"resume",
      "sub_page":"accounts",
      "page_title":"Create new Recruiter"
    },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def accounts_edit(request,id):
  e = Recruiter.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    form = EventForm(request.POST,instance=e) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Recruiter changed')
      return HttpResponseRedirect('/intranet/resume/accounts') # Redirect after POST
  else:
    form = RecruiterForm(instance=e)

  
  return render_to_response('intranet/resume_manager/account_form.html',{
      "form":form,
      "section":"intranet",
      "page":"resume",
      "sub_page":"accounts",
      "page_title":"Edit Recruiter",
   },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def accounts_delete(request,id):
  e = Recruiter.objects.get(id=id)
  e.delete()
  messages.add_message(request, messages.SUCCESS, 'Recruiter deleted')
  return HttpResponseRedirect('/intranet/resume/accounts')
