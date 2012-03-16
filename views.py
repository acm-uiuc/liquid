from django.shortcuts import render_to_response
from django.http import HttpResponse

def main(request):
	return render_to_response('main.html')
	
def contact(request):
  return render_to_response('contact.html')
	

