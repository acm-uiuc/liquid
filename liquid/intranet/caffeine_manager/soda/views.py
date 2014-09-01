from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from utils.group_decorator import group_admin_required
from django.contrib import messages
from intranet.caffeine_manager.soda.models import Soda
from intranet.caffeine_manager.soda.forms import SodaForm

def allsodas(request):
   sodas = Soda.objects.all().order_by('-total_sold', 'name')
   for s in sodas:
      s.votedFor = (s.votes.filter(username = request.user.username).count() == 1)

   request.session['from'] = None
 
   is_caffeine_admin = request.user.is_group_admin('Caffeine')
  
   # Get paginator and page
   page = 1
   paginator = Paginator(sodas, 10)
   page_arg = request.GET.get('page')
   if page_arg and page_arg.isdigit():
      page = int(page_arg)
      page = max(1, min(paginator.num_pages, page))
   sodasPage = paginator.page(page)

   return render_to_response(
    'intranet/caffeine_manager/soda/allsodas.html',
    {
      'section':'intranet',
      'page':'caffeine',
      'sodasPage':sodasPage,
      'request':request,
      'is_caffeine_admin':is_caffeine_admin
    }, context_instance=RequestContext(request))


#@group_admin_required(['Caffeine'])
def add(request):
   soda_form = None;
   from_arg = request.session.get('from') or ''
   if request.method == 'POST':
      soda_form = SodaForm(request.POST)
      if soda_form.is_valid():
        soda_form.save()
        return redirect('/intranet/caffeine/')
   else:
      soda_form = SodaForm()
      
   return render_to_response(
      'intranet/caffeine_manager/soda/edit_soda.html',
      {
        'section':'intranet',
        'page':'caffeine',
        'form':soda_form,
        'from_arg':from_arg
      }, 
      context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def edit(request, sodaId):
   soda = get_object_or_404(Soda, pk=sodaId)
   soda_form = None;
   from_arg = request.session.get('from') or ''
   
   if request.method == 'POST':
      soda_form = SodaForm(request.POST, instance=soda)
      if soda_form.is_valid():
        soda_form.save()
        if from_arg == 'trays':
            return redirect('/intranet/caffeine/trays')
        else:
            return redirect('/intranet/caffeine/')
   else:
      soda_form = SodaForm(instance=soda)
   
   return render_to_response(
      'intranet/caffeine_manager/soda/edit_soda.html',
      {
        'section':'intranet',
        'page':'caffeine',
        'form':soda_form,
        'id':sodaId,
        'from_arg':from_arg
      }, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def delete(request, sodaId):
   get_object_or_404(Soda, pk=sodaId).delete()

   if request.session.get('from') == 'trays':
      return redirect('/intranet/caffeine/trays')
   return redirect('/intranet/caffeine/')

def vote(request, sodaId):
   soda = get_object_or_404(Soda, pk=sodaId)
   has_voted = soda.votes.filter(username = request.user.username).count()
   if has_voted == 1:
      soda.votes.remove(request.user)
      messages.add_message(request, messages.ERROR, "Your vote has been removed!")
   else:
      soda.votes.add(request.user)
      messages.add_message(request, messages.SUCCESS, "Your vote has been recorded!")

   return redirect('/intranet/caffeine')

#@group_admin_required(['Caffeine'])  
def clear_votes(request, sodaId):
   soda = get_object_or_404(Soda, pk=sodaId)
   soda.votes.clear()
   messages.add_message(request, messages.INFO, "Votes cleared.")
   return redirect('/intranet/caffeine')