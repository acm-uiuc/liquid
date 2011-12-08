from projects.models import SIG, Project
from django.shortcuts import render_to_response

def sig_list(request):
	sigs = SIG.objects.all()
	context = {'sigs':sigs}
	return render_to_response("sigs.html", context)
