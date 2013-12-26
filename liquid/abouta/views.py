from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.mail import send_mail
from abouta.forms import PreMemberForm
from intranet.models import Member
from intranet.models import Group



# Create your views here.
def main(request):
  return render_to_response('about/main.html',{"section":"about","page":'main'},context_instance=RequestContext(request))
  
def join(request):
  c = {}
  c.update(csrf(request))
  sigs = Group.objects.filter(type='S').order_by('name')

  sig_count_half = sigs.count()/2
  
  if request.method == 'POST': # If the form has been submitted...
      form = PreMemberForm(request.POST) # A form bound to the POST data
      choosen_sigs = [int(s) for s in request.POST.getlist('sigs')]
      if form.is_valid(): # All validation rules pass
          pre_member = form.save()
          for s in choosen_sigs:
            g = Group.objects.get(id=s)
            try:
              g.subscribe("%s@illinois.edu"%pre_member.netid)
            except:
              pass
          return HttpResponseRedirect('/about/join/thanks/') # Redirect after POST
  else:
      form = PreMemberForm() # An unbound form
      choosen_sigs = []

  return render_to_response('about/join.html',{
      'form': form,
      "section":"about",
      'page': 'join',
      'sigs': sigs,
      "sig_count_half": sig_count_half,
      "choosen_sigs": choosen_sigs,
  },context_instance=RequestContext(request))

def join_thanks(request):
  return render_to_response('about/join_thanks.html',{
      "section":"about",
      'page': 'join'
  },context_instance=RequestContext(request))

  
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
