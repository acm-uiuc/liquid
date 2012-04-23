from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail
from abouta.forms import JobForm
from intranet.models import Member
from intranet.models import Group



# Create your views here.
def main(request):
  return render_to_response('about/main.html',{"section":"about","page":'main'},context_instance=RequestContext(request))
  
def join(request):
  return render_to_response('about/join.html',{"section":"about","page":'join'},context_instance=RequestContext(request))
  
def committees(request):
  committees = Group.objects.filter(type='C').filter(status='Active').order_by('name')
  return render_to_response('about/committees.html',{"section":"about","page":'committees',"committees":committees},context_instance=RequestContext(request))

def committees_details(request,id):
  c = Group.objects.get(id=id)
  return render_to_response('about/committees_details.html',{"section":"about","page":'committees',"c":c},context_instance=RequestContext(request))
  
def members(request):
  n = 3
  
  members = Member.objects.filter(status='active').order_by('last_name', 'first_name')
  p = len(members) / n
  members  = [members[p*i:p*(i+1)] for i in range(n - 1)] + [members[p*(i+1):]]
  
  return render_to_response('about/members.html',{"section":"about","page":'members','members':members},context_instance=RequestContext(request))
