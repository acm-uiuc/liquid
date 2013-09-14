from django.core.mail import send_mail, EmailMessage
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from conference.models import Company
from conference.forms import CompanyForm
from intranet.jobfair_manager.forms import InviteForm
import settings
from utils.group_decorator import group_admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import date

@group_admin_required(['Corporate'])
def companies(request):
   fair = request.GET.get('type')
   if fair == 'startup':
      companies = Company.objects.filter(type=Company.STARTUP)
   elif fair == 'jobfair':
      companies = Company.objects.filter(type=Company.JOBFAIR)
   else:
      companies = Company.objects.all()

   page = request.GET.get('page')
   paginator = Paginator(companies, 25) # Show 25 invites per page
   total_companies = paginator.count

   try:
      companies = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      companies = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      companies = paginator.page(paginator.num_pages)

   return render_to_response('intranet/jobfair_manager/companies.html',{
      "section":"intranet",
      "page":"jobfair",
      "sub_page":"companies",
      "page_title":"Job Fair Manager",
      "total_companies":total_companies,
      "companies":companies,
      "request": request,
   },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def companies_new(request):
   message = ""
   if request.method == 'POST': # If the form has been submitted...
      e = Company()
      form = CompanyForm(request.POST,instance=e) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          try:
              company = form.save(commit=False)
              company.username = slugify("rp13 "+company.company_name)
              company.save()
              messages.add_message(request, messages.SUCCESS, 'Company created (%s)'%(company.username))
              return HttpResponseRedirect('/intranet/jobfair_manager/companies') # Redirect after POST
          except IntegrityError as error:
              messages.add_message(request, messages.ERROR, "There is already a username like that! Please enter a different company name.")
   else:
      form = CompanyForm() # An unbound form

   return render_to_response('intranet/jobfair_manager/company_form.html',{
      'form': form,
      "section":"intranet",
      "page":"jobfair",
      "sub_page":"companies",
      "page_title":"Create new Company",
      "message": message
    },context_instance=RequestContext(request))


@group_admin_required(['Corporate'])
def companies_edit(request,id):
    e = Company.objects.get(id=id)
    if request.method == 'POST': # If the form has been submitted...
        form = CompanyForm(request.POST,instance=e) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Company changed')
            return HttpResponseRedirect('/intranet/jobfair_manager/companies') # Redirect after POST
    else:
        form = CompanyForm(instance=e)


    return render_to_response('intranet/jobfair_manager/company_form.html',{
        "form":form,
        "section":"intranet",
        "page":"jobfair",
        "sub_page":"companies",
        "page_title":"Edit Company",
        },context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def companies_delete(request,id):
    e = Company.objects.get(id=id)
    e.delete()
    messages.add_message(request, messages.SUCCESS, 'Company deleted')
    return HttpResponseRedirect('/intranet/jobfair_manager/companies')

@group_admin_required(['Corporate'])
def companies_invite(request, id):
    e = Company.objects.get(id=id)
    if request.method =="GET":
        password = Company.objects.make_random_password()
        e.set_password(password)
        e.invited_on = date.today()
        e.invited_by = request.user
        e.save()
        c = {"company": e, "password": password}
        if e.type == Company.JOBFAIR:
            body = render_to_string("conference/emails/jobfair_invite.txt", c, context_instance=RequestContext(request))
            subject = "Invitation to Reflections | Projections 2013 Job Fair"
        else:
            body = render_to_string("conference/emails/startupfair_invite.txt", c, context_instance=RequestContext(request))
            subject = "Invitation to Reflections | Projections 2013 Startup Fair"
        form = InviteForm(data={"body":body,
                                "subject":subject,
                                "from_email":request.user.email,
                                "to_email": e.email})
    else:
        form = InviteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if not settings.DEBUG:
                cc = ["ACM Corporate <corporate@acm.illinois.edu>"]
            else:
                cc =[]
            email = EmailMessage(subject=data["subject"],
                      body=data["body"],
                      from_email="%s <%s>" % (request.user.get_full_name(), data["from_email"]),
                      to=[data["to_email"]],
                      cc= cc
                      )
            email.send()
            messages.add_message(request, messages.SUCCESS, 'Invite sent to %s' % (data["to_email"]))
            e.invited = True
            e.save()
            return HttpResponseRedirect('/intranet/jobfair_manager/companies')
    return render_to_response('intranet/jobfair_manager/company_invite.html',{
    "form":form,
    "company":e,
    "section":"intranet",
    "page":"jobfair",
    "sub_page":"companies",
    "page_title":"Invite Company",
    },context_instance=RequestContext(request))



