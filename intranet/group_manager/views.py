from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from intranet.group_manager.models import Group, GroupMember, Project
from intranet.group_manager.forms import GroupForm, GroupMemberFormSet
from intranet.member_manager.models import Member
import string

# Create your views here.
def main(request):
  groups = Group.objects.all()
  return render_to_response('intranet/group_manager/main.html',{"section":"intranet","page":'group','groups':groups})
  
def new(request):
  if request.method == 'POST': # If the form has been submitted...
      form = GroupForm(request.POST) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          form.save()
          return HttpResponseRedirect('/intranet/group') # Redirect after POST
  else:
      form = GroupForm() # An unbound form

  return render_to_response('intranet/group_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":'group',
      "page_title":"Create new Group"
      },context_instance=RequestContext(request))
  
def edit(request,id):
  g = Group.objects.get(id=id)
  forms = GroupMemberFormSet(instance=g)
  if request.method == 'POST': # If the form has been submitted...
      form = GroupForm(request.POST,instance=g) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          form.save()
          return HttpResponseRedirect('/intranet/group') # Redirect after POST
  else:
    form = GroupForm(instance=g)

  
  return render_to_response('intranet/group_manager/form.html',{
    "form":form,
    "section":"intranet",
    "page":'group',
    "page_title":"Edit Group",
    },context_instance=RequestContext(request))

def manage(request,id):
  saved = False
  g = Group.objects.get(id=id)
  if request.method == 'POST': # If the form has been submitted...
    forms = GroupMemberFormSet(request.POST,instance=g)
    if forms.is_valid(): # All validation rules pass
      forms.save()
      saved = True
  else:
    forms = GroupMemberFormSet(instance=g)

  return render_to_response('intranet/group_manager/manage.html',{
    "section":"intranet",
    "page":'group',
    "group":g,
    "forms":forms,
    "saved":saved
    },context_instance=RequestContext(request))

def add(request,id):
  g = Group.objects.get(id=id)
  added = []
  badid = []
  duplicate = []

  if request.method == 'POST':
    netids = [i.strip() for i in string.split(request.POST['netids'],",")]
    for i in netids:
      if len(i) > 0:
        try:
          m = Member.objects.get(netid=i)
          gm = GroupMember(member=m,group=g)
          gm.save()
          added.append(m)
        except Member.DoesNotExist:
          badid.append(i)
        except IntegrityError:
          duplicate.append(m)


  return render_to_response('intranet/group_manager/add.html',{
    "section":"intranet",
    "page":'group',
    "group":g,
    "added": added,
    "badid": badid,
    "duplicate": duplicate
    },context_instance=RequestContext(request))

