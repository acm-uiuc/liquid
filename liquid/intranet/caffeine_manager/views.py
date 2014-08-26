from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from intranet.models import Job, Resume, Member, Vending
from intranet.caffeine_manager.models import Soda, Tray
from django.contrib.auth.decorators import user_passes_test
from utils.group_decorator import group_admin_required
from django.core.paginator import Paginator
from intranet.caffeine_manager.forms import SodaForm, TrayForm, VendingForm
from django.db.models import Q

# Create your views here.
def main(request):
   sodas = Soda.objects.all().order_by('-total_sold', 'name')
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

   return render_to_response('intranet/caffeine_manager/allsodas.html',{'section':'intranet','page':'caffeine','sodasPage':sodasPage,'request':request, 'is_caffeine_admin':is_caffeine_admin}, context_instance=RequestContext(request))

def vote(request, vote):
   return render_to_response('intranet/caffeine_manager/vote.html',{'section':'intranet','page':'caffeine'}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def add_soda(request):
   soda_form = None;
   if request.method == 'POST':
      soda_form = SodaForm(request.POST)
      if soda_form.is_valid():
        soda_form.save()
        return redirect('/intranet/caffeine/')
   else:
      soda_form = SodaForm()
      
   from_arg = request.session.get('from') or ''
   return render_to_response('intranet/caffeine_manager/edit_soda.html', {'section':'intranet','page':'caffeine','form':soda_form,'new_soda':True,'from_arg':from_arg}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def edit_soda(request, sodaId):

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
   
   return render_to_response('intranet/caffeine_manager/edit_soda.html',{'section':'intranet','page':'caffeine','form':soda_form,'new_soda':False,'id':sodaId,'from_arg':from_arg}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def delete_soda(request, sodaId):

   soda = get_object_or_404(Soda, pk=sodaId)
   soda.delete()

   if request.session.get('from') == 'trays':
      return redirect('/intranet/caffeine/trays')
   else:
      return redirect('/intranet/caffeine/')

def user(request, netid=None):

   searchArg = ''
   vend_user = None
   is_caffeine_admin = request.user.is_group_admin('Caffeine')

   if request.method == 'GET' and request.GET.get('q'):
      searchArg = request.GET.get('q')

   if searchArg and (not request.GET.get('searched')):
      users = Vending.objects.filter(Q(user__status = 'active') & (Q(user__first_name = searchArg) | Q(user__last_name = searchArg) | Q(user__username = searchArg))).order_by('-spent', 'balance')

      append = '?q=' + searchArg + '&searched=1'
      if users:
         vend_user = users[0].user
         netid = vend_user.username
         return redirect('/intranet/caffeine/user/' + netid + append)
      else:
         return redirect('/intranet/caffeine/user/' + append)

   if netid:
      vend_user = get_object_or_404(Member, username=netid)
   elif not searchArg:
      vend_user = request.user

   vending = None
   if vend_user:
      vending = vend_user.get_vending()

   return render_to_response('intranet/caffeine_manager/user.html',{'section':'intranet','page':'caffeine','is_caffeine_admin':is_caffeine_admin,'vend_user':vend_user,'vending':vending,'searchArg':searchArg}, context_instance=RequestContext(request))

def leaderboard(request):

   count = 5
   baseQuery = Vending.objects.filter(user__status = 'active')

   topCalories = baseQuery.order_by('-calories')[0:count]
   topCaffeine = baseQuery.order_by('-caffeine')[0:count]
   topSpent = baseQuery.order_by('-spent')[0:count]
   topSodas = baseQuery.order_by('-sodas')[0:count]

   return render_to_response('intranet/caffeine_manager/leaderboard.html',{'section':'intranet','page':'caffeine','topCalories':topCalories,'topCaffeine':topCaffeine,'topSpent':topSpent,'topSodas':topSodas}, context_instance=RequestContext(request))

def trays(request):

   request.session['from'] = 'trays'

   trays = Tray.objects.all().order_by('tray_number')
   is_caffeine_admin = request.user.is_group_admin('Caffeine')

   return render_to_response('intranet/caffeine_manager/trays.html', {'section':'intranet','page':'caffeine','trays':trays,'is_caffeine_admin':is_caffeine_admin}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def add_tray(request):
   tray_form = None;
   if request.method == 'POST':
      tray_form = TrayForm(request.POST)
      if tray_form.is_valid():
        tray_form.save()
        return redirect('/intranet/caffeine/trays/')
   else:
      tray_form = TrayForm()
      
   return render_to_response('intranet/caffeine_manager/edit_tray.html',{'section':'intranet','page':'caffeine','form':tray_form,'new_tray':True}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def edit_tray(request, trayId):

   tray = get_object_or_404(Tray, pk=trayId)

   if request.method == 'POST':
      tray_form = TrayForm(request.POST, instance=tray)
      if tray_form.is_valid():
          tray_form.save()
          return redirect('/intranet/caffeine/trays/')
   else:
      tray_form = TrayForm(instance=tray)

   return render_to_response('intranet/caffeine_manager/edit_tray.html',{'section':'intranet','page':'caffeine','form':tray_form,'new_tray':False,'id':trayId}, context_instance=RequestContext(request))

#@group_admin_required(['Caffeine'])
def delete_tray(request, trayId):

   tray = get_object_or_404(Tray, pk=trayId)
   tray.delete()

   return redirect('/intranet/caffeine/trays/')

#@group_admin_required(['Caffeine'])
def edit_user(request, netid):

    vend_user = get_object_or_404(Member, username=netid)
    vending = vend_user.get_vending()
    user_form = None;
    
    if request.method == 'POST':
        user_form = VendingForm(request.POST, instance=vending)
        if user_form.is_valid():
            user_form.save()
            return redirect('/intranet/caffeine/user/' + vend_user.username);
    else:
        user_form = VendingForm(instance=vending)
    
    return render_to_response('intranet/caffeine_manager/edit_user.html',{'section':'intranet','page':'caffeine','form':user_form}, context_instance=RequestContext(request))

def soda_vote(request):
   pass
