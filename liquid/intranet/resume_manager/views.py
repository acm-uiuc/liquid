from django.shortcuts import render_to_response
from intranet.models import Resume
from django.template import RequestContext
from django.contrib import messages
from intranet.resume_manager.forms import ResumeFormSet
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
from django.http import HttpResponse


@group_admin_required(['Corporate'])
def main(request):
   if request.method == 'POST':
      formset = ResumeFormSet(request.POST)
      if formset.is_valid(): # All validation rules pass
         formset.save()
         messages.add_message(request, messages.SUCCESS, 'Changes saved')
   resumes = Resume.objects.filter(approved__exact=False)
   formset = ResumeFormSet(queryset=resumes)
   return render_to_response('intranet/resume_manager/main.html',{"section":"intranet","page":'resume',"resume_count":len(resumes),"resumes":formset},context_instance=RequestContext(request))

@group_admin_required(['Corporate'])
def thumb(request,id):
   try:
      r = Resume.objects.get(id=id)
      r.generate_thumbnails()
      image_data = open(r.thumbnail_location(), "rb").read()
      return HttpResponse(image_data, mimetype="image/png")
   except:
      raise Http404

@group_admin_required(['Corporate'])
def thumb_top(request,id):
   r = Resume.objects.get(id=id)
   r.generate_thumbnails()
   image_data = open(r.thumbnail_top_location(), "rb").read()
   return HttpResponse(image_data, mimetype="image/png")
