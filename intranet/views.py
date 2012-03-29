from django.shortcuts import render_to_response
from django.http import HttpResponse

# Create your views here.
def main(request):
  return render_to_response('intranet/main.html',{"section":"intranet","page":'main'})
  
def faq(request):
  return render_to_response('intranet/faq.html',{"section":"intranet","page":'faq'})
  
def treasure_chest(request):
  return render_to_response('intranet/treasure_chest.html',{"section":"intranet","page":'treasure_chest'})