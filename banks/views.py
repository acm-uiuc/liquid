from django.shortcuts import render_to_response
from django.http import HttpResponse



# Create your views here.
def main(request):
  return render_to_response('banks/main.html',{"section":"banks","page":'main'})