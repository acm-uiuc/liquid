from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def main(request):
	return render_to_response('conf/main.html',{"section":"conf", "page":"main"},context_instance=RequestContext(request))