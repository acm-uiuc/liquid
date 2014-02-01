from django.shortcuts import render_to_response
from intranet.models import Resume, ResumePerson
from django.template import RequestContext
from django.contrib import messages
from intranet.models import Recruiter
from django.core.mail import send_mail
from intranet.resume_manager.forms import ResumeFormSet, RecruiterForm
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import datetime, timedelta
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives # Used for sending HTML emails

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
def accounts(request):
   recruiters = Recruiter.objects.all()
   paginator = Paginator(recruiters, 25) # Show 25 contacts per page
   
   total_recruiters = paginator.count

   page = request.GET.get('page')
   try:
      recruiters = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      recruiters = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      recruiters = paginator.page(paginator.num_pages)

   return render_to_response('intranet/resume_manager/accounts.html',{
      "section":"intranet",
      "page":"resume",
      "sub_page":"accounts",
      "total_recruiters":total_recruiters,
      "recruiters":recruiters,
      "request": request,
   },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def accounts_new(request):
   message = ""
   if request.method == 'POST': # If the form has been submitted...
      e = Recruiter()
      form = RecruiterForm(request.POST,instance=e) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
         recruiter = form.save()
         password = Recruiter.objects.make_random_password()
         print password
         recruiter.set_password(password)
         recruiter.save()
         message = request.POST.get('message')
         email = "%s\n\n----------------------------\n\nHi %s,\n\nA new account for you to access the ACM@UIUC resume book has been created.\n\nUsername: %s\nPassword: %s\n\nTo login visit http://acm.illinois.edu/resume.\n\nThanks,\nACM@UIUC Corporate Committee"%(message,recruiter.first_name,recruiter.username,password)
         send_mail('ACM@UIUC Resume Book', email, 'ACM Corporate Committee <corporate@acm.illinois.edu>',[recruiter.email,'corporate@acm.illinois.edu'], fail_silently=False)
         messages.add_message(request, messages.SUCCESS, 'Recruiter created (%s, %s)'%(recruiter.username, password))
         return HttpResponseRedirect('/intranet/resume/accounts') # Redirect after POST    
   else:
      form = RecruiterForm() # An unbound form

   return render_to_response('intranet/resume_manager/account_form.html',{
      'form': form,
      "section":"intranet",
      "page":"resume",
      "sub_page":"accounts",
      "page_title":"Create new Recruiter",
      "message": message
    },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def accounts_edit(request,id):
  e = Recruiter.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    form = RecruiterForm(request.POST,instance=e) # A form bound to the POST data
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
  
@group_admin_required(['Corporate'])
def send_resume_reminders(request):

   # Send e-mails
   successful = 0
   failed = 0
   if request.method == "POST":
            
      # Get threshold date
      months = int(request.POST["reminder_duration"])
      threshold_date = datetime.now() - timedelta(days=30*months)
      
      # Get people to send e-mails to
      people = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date)
            
      # Send e-mails
      current_site = request.META['HTTP_HOST']
      for person in people:        
         email_url = (
                     "http://" +
                     current_site + 
                     "/corporate/resume/student/referred"
                     "?netid=" + person.netid +
                     "&fname=" + person.first_name +
                     "&lname=" + person.last_name +
                     "&level=" + person.level +
                     "&seeking=" + person.seeking +
                     "&graduation=" + str(person.graduation) +
                     "&resume_uuid=" + person.resume_uuid
                     )
         unsubscribe_url = (
                     "http://" +
                     current_site +
                     "/corporate/resume/student/unsubscribe" +
                     "?resume_uuid=" + person.resume_uuid
                     )
                      
         email_string = (
                     "<p>Hello " + person.first_name + ",</p>" +
                     "<p>You haven't updated your resume on the ACM@UIUC website in awhile." +
                     " If you'd like to preview and/or update the copy of your resume that we" +
                     " have on file, click " +
                     
                     "<a href='" + email_url + "'>here</a>.</p>" +
                     
                     "<p>If you would like to unsubscribe from these notifications, click " +
                     "<a href='" + unsubscribe_url + "'>here</a>.</p>" +
                        
                     "<p>Thanks,<br \The ACM@UIUC Corporate Committee.</p>"
                     )        
                       
           try:
             msg = EmailMultiAlternatives("ACM@UIUC Resume Book", "Please view this e-mail with HTML enabled.", "corporate@acm.illinois.edu", [person.netid+"@illinois.edu"])
             msg.attach_alternative(email_string, "text/html")
             msg.send()
             successful += 1
             
             # Update sent date
             person.resume_reminded_at = datetime.now()
             person.save()
             
           except:
             failed += 1
             pass
      
      messages.add_message(request, messages.INFO, str(successful + failed) + ' e-mail sends were attempted.')
      if successful != 0:
         messages.add_message(request, messages.SUCCESS, str(successful) + ' e-mail(s) were successfully sent!')
      if failed != 0:
         messages.add_message(request, messages.ERROR, str(failed) + ' e-mail(s) failed to send.')
      
   # Get sizes of e-mail groups
   threshold_date_0 = datetime.now()
   threshold_date_1 = datetime.now() - timedelta(days=30)
   threshold_date_3 = datetime.now() - timedelta(days=90)
   threshold_date_6 = datetime.now() - timedelta(days=180)
   threshold_date_12 = datetime.now() - timedelta(days=360)
   
   people_count_0 = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date_0).count()
   people_count_1 = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date_1).count()
   people_count_3 = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date_3).count()
   people_count_6 = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date_6).count()
   people_count_12 = ResumePerson.objects.filter(resume_reminded_at__lt=threshold_date_12).count()

   people_array = ["nobody", " person", " people"]

   return render_to_response('intranet/resume_manager/resume_reminder.html',{
      "section":"intranet",
      "page":"resume",
      "sub_page":"send_reminders",
      
      "people_0": (str(people_count_0) if people_count_0 != 0 else "") + people_array[min(people_count_0,2)],
      "people_1": (str(people_count_1) if people_count_1 != 0 else "") + people_array[min(people_count_1,2)],
      "people_3": (str(people_count_3) if people_count_3 != 0 else "") + people_array[min(people_count_3,2)],
      "people_6": (str(people_count_6) if people_count_6 != 0 else "") + people_array[min(people_count_6,2)],
      "people_12": (str(people_count_12) if people_count_12 != 0 else "") + people_array[min(people_count_12,2)]
      
   },context_instance=RequestContext(request))
