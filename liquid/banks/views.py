from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.contrib import messages
from banks.models import BanksPost, Comment
from banks.forms import PostForm, CommentForm
from utils.group_decorator import group_admin_required
import datetime

# /banks
def main(request):
  posts = BanksPost.objects.all().order_by("-created")
  paginator = Paginator(posts,10)

  #try to get the first page
  try: page = int(request.GET.get("page", '1'))
  except ValueError: page = 1

  try:
    posts = paginator.page(page)
  except (InvalidPage, EmptyPage):
    posts = paginator.page(paginator.num_pages)

  return render_to_response('banks/main.html',{"section":"banks","page":'main', "posts": posts, "user": request.user},context_instance=RequestContext(request))

# /banks/posts/:_id
def viewPost(request, id):
  post = BanksPost.objects.get(id=id)
  comments = Comments.object.filter(post=post)
  res = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
  res.update(crsf(request))
  return render_to_response("banks/post.html", res)

# /banks/posts/new
@group_admin_required(['top4'])
def new(request):
  if request.method is 'POST': #form has been properly submitted
    p = BanksPost(creator=request.user)
    form = PostForm(instance=p)
    form.save()
    messages.add_message(request, messages.SUCCESS, 'Post Successfully Created')
  return HttpResponseRedirect('/banks')


# /banks/posts/edit/:_id
@group_admin_required(['top4'])
def edit(request, id):
  p = BanksPosts.objects.get(id=id)
  if request.method == "POST":
    form = PostForm(request.Post, instance=p)
    if form.is_valid():
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Post Changed')
      print "new post hit"
      return HttpResponseRedirect('/banks')

  else:
      form = PostForm(instance=p)
  print "form is not valid"
  return HttpResponseRedirect('/banks')

  #render_to_response('banks/posts/form.html',{
  #  'form':form,
  #  "section":"banks",
  #  "page":"post",
  #  "page_title":"Edit Post"
  #}, context_instance=RequestContext(request))

# /banks/posts/delete/:_id
@group_admin_required(['top4'])
def delete(request, id):
  post = BanksPosts.objects.get(id=id)
  post.delete()
  messages.add_message(request, messages.SUCCESS, 'Post Deleted')
  return HttpResponseRedirect('/banks')


# -- COMMENTS ROUTES

# /banks/comments/delete_comment/:_id
@group_admin_required(['top4'])
def delete_comment(request, post_id, id=None):
  if not id: idList = request.Post.getlist('delete')
  else: idList = [id]

  #handle deletion of multiple comments at once
  for id in idList:
    Comment.objects.get(id=id).delete()

  return HttpResponseRedirect(reverse('banks.views.viewPost',args=[id]))


# /banks/comments/new/:_id"
def add_comment(request, id):
  p = request.POST
  if p.has_key("body") and p["body"]:
    author = "Anonymous"
    if p["Author"]: author = p["Author"]

    comment = Comment(post=post.objects.get(id=id))
    form = CommentForm(p, instance=comment)
    form.fields["author"].required = False
    comment.author = author
    comment.save()

  return HttpResponseRedirect(reverse("banks.views.viewPost", args=[id]))
