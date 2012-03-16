from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from abouta.models import JobForm



# Create your views here.
def about(request):
  return render_to_response('about/about.html',{"page":'about'})
  
def join(request):
  return render_to_response('about/join.html',{"page":'join'})
  
def committees(request):
  return render_to_response('about/committees.html',{"page":'committees'})
  
def corporate(request):
  return render_to_response('about/corporate.html',{"page":'corporate'})
  
def job(request):
  c = {}
  c.update(csrf(request))
  if request.method == 'POST': # If the form has been submitted...
      form = JobForm(request.POST) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          form.save()
          
          return HttpResponseRedirect('/about/corporate/job/thanks/') # Redirect after POST
  else:
      form = JobForm() # An unbound form

  return render_to_response('about/job.html',{
      'form': form,
      "page":'corporate'
  },context_instance=RequestContext(request))

def thanks(request):
  return render_to_response('about/thanks.html',{'page':'corporate'})
  
def members(request):
  return render_to_response('about/members.html',{"page":'members'})