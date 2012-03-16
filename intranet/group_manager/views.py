from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from intranet.group_manager.models import Group, GroupMember, Project

# Create your views here.
def main(request):
  groups = Group.objects.all()
  return render_to_response('intranet/group_manager/main.html',{"page":'group','groups':groups})
  
def new(requset):
  return render_to_response('intranet/group_manager/form.html',{"page":'group',"page_title":"Create new Group"})
  
def edit(request,id):
  return render_to_response('intranet/group_manager/form.html',{"page":'group',"page_title":"Edit Group"})
  