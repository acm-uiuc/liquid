from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db.models import Q
from django.forms.util import ErrorList
from django.contrib import messages
from utils.group_decorator import group_admin_required, is_admin
from intranet.models import Member, PreMember
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from intranet.member_database.forms import NewMemberForm, EditMemberForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ldap


# Create your views here.
def main(request):
   pre_members = PreMember.objects.all()
   return render_to_response('intranet/member_database/main.html',{
      "section":"intranet",
      "page":'members',
      "pre_members": pre_members
   },context_instance=RequestContext(request))
  
def search(request):
   q = request.GET.get('q')
   if q:
      members = Member.objects.filter(Q(username__icontains=q) | \
                                    Q(first_name__icontains=q) | \
                                    Q(last_name__icontains=q)) \
                            .order_by('last_name', 'first_name')
   else:
      members = Member.objects.order_by('last_name', 'first_name')

   paginator = Paginator(members, 25) # Show 25 contacts per page
   total_members = paginator.count

   page = request.GET.get('page')
   try:
      members = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      members = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      members = paginator.page(paginator.num_pages)
  
   return render_to_response('intranet/member_database/search.html',{
    "section":"intranet",
    "page":'members',
    'members':members,
    "total_members": total_members,
    'q':q,
    'request': request,
   },context_instance=RequestContext(request))

@is_admin()
def new(request,id):
   try:
      pre_member = PreMember.objects.get(id=id)
   except PreMember.DoesNotExist:
      raise Http404
   try:
      u = Member(username=pre_member.netid,uin=pre_member.uin)
      u.save()
      u.set_unusable_password()
      member_group = Group.objects.get(name='Member')
      u.groups.add(member_group)
      u.save()
      messages.add_message(request, messages.SUCCESS, 'Member created')
      pre_member.delete()
      welcome_msg = """Hello %s %s,

You sent a payment of $40.00 USD to the Association for Computing Machinery at the University of Illinois at Urbana-Champaign on %s.

----------------------------------------
ACM Lifetime Membership   $40.00 USD

Subtotal: $40.00 USD
Total: $40.00 USD

Payment: $40.00
----------------------------------------

Your ACM Network account and other ACM services will be provisioned within 48 hours. You will receive an additional e-mail when this is complete.

Questions? Contact userhelp@acm.illinois.edu

Please retain this email for your records.

Thanks,
ACM@UIUC


Approved by: %s"""%(u.first_name,u.last_name,u.date_joined.strftime("%a %b %d, %Y %H:%M:%S"),request.user.username)
      send_mail('Welcome to ACM@UIUC', welcome_msg, 'ACM <acm.illinois.edu>',[u.email,'payment-mailer@acm.illinois.edu'], fail_silently=False)
      return HttpResponseRedirect('/intranet/members/search?q=%s' % u.username) # Redirect after POST
   except ValueError:
      messages.add_message(request, messages.ERROR, "Not a valid netid")

   return HttpResponseRedirect('/intranet/members/') 

@group_admin_required(['Top4'])
def edit(request,id):
   g = Member.objects.get(id=id)
   forms = EditMemberForm(instance=g)
   if request.method == 'POST': # If the form has been submitted...
      form = EditMemberForm(request.POST,instance=g) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
         form.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
      return HttpResponseRedirect('/intranet/members') # Redirect after POST
   else:
      form = EditMemberForm(instance=g)

   return render_to_response('intranet/member_database/form.html',{
      "form":form,
      "section":"intranet",
      "page":'members',
      "page_title":"Edit member",
      },context_instance=RequestContext(request))
