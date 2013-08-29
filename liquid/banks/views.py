from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.contrib import messages
from banks.models import BanksPost
from banks.forms import PostForm
from utils.group_decorator import group_admin_required
import datatime

# /banks
def main(request):
  return render_to_response('banks/main.html',{"section":"banks","page":'main'},context_instance=RequestContext(request))

# /banks/posts/:_id
def viewPost(request, id):


# /banks/posts/new
@group_admin_required(['top4'])
def new(request):
  if request.metod == 'POST': #form has been properly submitted
  p = BanksPost(creator=request.user)
  form = PostForm(request.Post, instance=p)
  if form.is_valid():
    form.save()
    messages.add_message(request, messages.SUCCESS, 'Post Successfully Created')
    return HttpResponseRedirect('/banks')
  else:
    form = PostForm() #an unbound post

  retyrn render_to_response('banks/posts/form.html', {
    "form": form,
    "section": 'banks',
    "page": "post",
    "page_title", "Create new Post"
    }, context_instance=RequestContext(request))

# /banks/posts/edit/:_id
@group_admin_required(['top4'])
def edit(request, id):
  p = BanksPosts.objects.get(id=id)
  if request.method == "POST":
    form = PostForm(request.Post, instance=p)
    if form.is_valid():
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Post Changed')
      return HttpResponseRedirect('/banks')
  else:
      form = PostForm(instance=p)

  return render_to_response('banks/posts/form.html',{
    'form':form,
    "section":"banks",
    "page":"post",
    "page_title":"Edit Post"
  }, context_instance=RequestContext(request))

# /banks/posts/delete/:_id
@group_admin_required(['top4'])
def delete(request, id):
  post = BanksPosts.objects.get(id=id)
  post.delete()
  messages.add_message(request, messages.SUCCESS, 'Post Deleted')
  return HttpResponseRedirect('/banks')
