from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import messages
from intranet.chroma.models import Animation, Play
from sets import Set
import json
import urllib
import urllib2

# Create your views here.
def main(request):
   animations = Animation.objects.all()
   try:
      current = Play.objects.latest('timestamp').animation
   except:
      current = None
   return render_to_response('intranet/chroma/main.html',{"section":"intranet","page":'chroma','animations':animations,'current':current},context_instance=RequestContext(request))

def play(request,id):
   animation = Animation.objects.get(id=id)
   
   data = {}
   data['animation'] = animation.identifier
   url_values = urllib.urlencode(data)
   url = 'http://localhost:8181/play'
   full_url = url + '?' + url_values
   response = urllib2.urlopen(full_url).read()
   
   Play(animation=animation,member=request.user).save()

   messages.add_message(request, messages.SUCCESS, response)
   return HttpResponseRedirect('/intranet/chroma/') # Redirect after POST

def off(request):
   url = 'http://localhost:8181/off'
   response = urllib2.urlopen(url).read()
   
   Play(animation=None,member=request.user).save()
   
   messages.add_message(request, messages.SUCCESS, response)
   return HttpResponseRedirect('/intranet/chroma/') # Redirect after POST

def pull(request):
   animations = Animation.objects.all()
   identifiers = []
   for a in animations:
      identifiers.append(a.identifier)
   identifiers = Set(identifiers)
   url = 'http://localhost:8181/pull'
   response = json.loads(urllib2.urlopen(url).read())
   identifiers_response = []
   for a in response['animations']:
      identifiers_response.append(a)
   identifiers_response = Set(identifiers_response)
   
   not_in_db = identifiers_response.difference(identifiers)
   been_deleted = identifiers.difference(identifiers_response)
   already_there = identifiers_response.intersection(identifiers)
   
   for identifier in not_in_db:
      current = response['animations'][identifier]
      a = Animation(name=current['name'],description=current['description'],creator=current['creator'],identifier=identifier)
      a.save()
   for identifier in been_deleted:
      a = Animation.objects.get(identifier=identifier)
      a.delete()
   for identifier in already_there:
      current = response['animations'][identifier]
      a = Animation.objects.get(identifier=identifier)
      a.name = current['name']
      a.description = current['description']
      a.creator = current['creator']
      a.save()
   messages.add_message(request, messages.SUCCESS, response['output'])
   return HttpResponseRedirect('/intranet/chroma/') # Redirect after POST