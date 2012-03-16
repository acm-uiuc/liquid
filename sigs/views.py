from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from intranet.sig_manager.models import SIG, SIGMember, Project

# Create your views here.
def main(request):
  sigs = SIG.objects.all()
  return render_to_response('sigs/main.html',{'sigs':sigs})
