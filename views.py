from django.shortcuts import render_to_response
from django.http import HttpResponse
import urllib
import simplejson

def main(request):
  # Build GitHub activity
  feed = urllib.urlopen("https://api.github.com/orgs/acm-uiuc/events")
  events = simplejson.loads(feed.read())[0:5]
  return render_to_response('main.html', {'events':events})
	
def contact(request):
  return render_to_response('contact.html')
	

