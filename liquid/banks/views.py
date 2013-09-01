from django.shortcuts import render_to_response, HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.contrib import messages
from banks.models import Post
from banks.forms import PostForm
from utils.group_decorator import group_admin_required
import calendar, datetime

# /banks
def main(request):
  posts_set = Post.objects.all()

  paginator = Paginator(posts_set, 5)
  page = request.GET.get('page')

  #try to get the first page
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  return render_to_response(
    'banks/main.html',
    {
      "section":"banks",
      "page":'main',
      "posts": posts,
      "user": request.user
    }
    ,context_instance=RequestContext(request)
  )

# /banks/posts/:slug
def viewPost(request, slug):
  print "VIEW POST"
  post = get_object_or_404(Post, slug=slug)
  return render_to_response(
    'banks/post.html',
    {
      "section":"banks",
      "page": "post",
      "post": post,
      "user": request.user
    }
    ,context_instance=RequestContext(request)
  )

# /banks/posts/new
@group_admin_required(['top4'])
def new(request):
  if request.method == 'POST': # form has been properly submitted
    p = Post(creator=request.user)
    form = PostForm(request.POST, instance=p)
    if form.is_valid():
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Post Created')
    else:
      messages.add_message(request, messages.SUCCESS, "Error in Post")

    return HttpResponseRedirect('/banks')
  else:
    #rendering old form
    form = PostForm()

    return render_to_response('banks/form.html', {
      "form": form,
      "page_title": "Create new Post"
      }, context_instance=RequestContext(request))


# /banks/posts/edit/:slug
@group_admin_required(['top4'])
def edit(request, slug):
  p = Posts.objects.get(slug=slug)
  if request.method == "POST":
    form = PostForm(request.Post, instance=p)
    if form.is_valid():
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Post Changed')
      return HttpResponseRedirect('/banks', context_instance=RequestContext(request))
  else:
    form = PostForm(instance=p)

  render_to_response('banks/posts/form.html',{
    'form':form,
    "page_title":"Edit Post"
  }, context_instance=RequestContext(request))

# /banks/posts/delete/:slug
@group_admin_required(['top4'])
def delete(request, slug):
  post = Posts.objects.get(id=slug)
  post.delete()
  messages.add_message(request, messages.SUCCESS, 'Post Deleted')
  return HttpResponseRedirect('/banks', context_instance=RequestContext(request))
