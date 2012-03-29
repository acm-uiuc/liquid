from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from intranet.group_manager.models import Group, GroupMember, Project

# Create your views here.
def main(request):
  sigs = Group.objects.all()
  return render_to_response('sigs/main.html',{"section":"sigs",'sigs':sigs})
