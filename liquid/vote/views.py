from django.shortcuts import render_to_response
from django.template import RequestContext
from vote.models import Vote
# Create your views here.

def vote(request,netid,key):
   try:
      vote = Vote.objects.filter(user__username=netid).filter(key=key)[:1][0]
   except IndexError:
      vote = None
   if not vote:
      #not a valid vote netid/key combo
      return render_to_response('vote/error.html',context_instance=RequestContext(request))
   
   if request.method == 'POST':
      #if they are submitting their vote
      try:
         print request.POST['vote']
         vote.vote = request.POST['vote'] == "true"
         vote.save()
         vote_text = "Accept" if vote.vote else "Reject"
         return render_to_response('vote/thanks.html',{"name":vote.user.full_name(),"vote":vote_text },context_instance=RequestContext(request))
      except:
         pass
   if not vote.vote == None:
      #if they already voted
      return render_to_response('vote/error.html',context_instance=RequestContext(request))
   return render_to_response('vote/vote.html',{"name":vote.user.full_name()},context_instance=RequestContext(request))
   