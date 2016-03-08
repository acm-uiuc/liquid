from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from utils.group_decorator import group_admin_required
from django.core.urlresolvers import reverse
from intranet.caffeine_manager.trays.models import Tray
from intranet.caffeine_manager.trays.forms import TrayForm
from intranet.caffeine_manager.views import fromLocations
import subprocess

def view(request):
    request.session['from']=fromLocations.TRAYS
    trays=Tray.objects.all().order_by('id')
    is_caffeine_admin=request.user.is_group_admin('Caffeine')
    return render_to_response(
       'intranet/caffeine_manager/trays/trays.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'sub_page':'trays',
         'trays':trays,
         'is_caffeine_admin':is_caffeine_admin
       },
       context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def add_tray(request):
    tray_form=None;
    if request.method == 'POST':
        tray_form=TrayForm(request.POST)
        if tray_form.is_valid():
            tray_form.save()
            return redirect(reverse('cm_trays_view'))
    else:
        tray_form=TrayForm()

    return render_to_response(
       'intranet/caffeine_manager/trays/edit_tray.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'form':tray_form
       }, context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def edit_tray(request, trayId):
    tray=get_object_or_404(Tray, pk=trayId)
    if request.method == 'POST':
        tray_form=TrayForm(request.POST, instance=tray)
        if tray_form.is_valid():
            tray_form.save()
            return redirect(reverse('cm_trays_view'))
    else:
        tray_form=TrayForm(instance=tray)

    return render_to_response(
       'intranet/caffeine_manager/trays/edit_tray.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'form':tray_form,
         'id':trayId
       }, context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def delete_tray(request, trayId):
    get_object_or_404(Tray, pk=trayId).delete()
    return redirect(reverse('cm_trays_view'))

# Helper function to vend a soda
# Requires a valid SSH key; ensure trayId is an int to prevent command injection
def do_vend(trayId):
    return subprocess.call(['ssh', 'soda@siebl-1106-05.acm.illinois.edu', '-o', 'StrictHostKeyChecking no', '-i', '/config/.ssh/id_rsa', '~/bin/force_vend ' + str(int(trayId))])

# Vend a soda without recording the vend (i.e. don't charge anyone)
@group_admin_required(['Caffeine'])
def force_vend(request, trayId):
    ret=do_vend(trayId)
    if ret == 0:
        messages.add_message(request, messages.SUCCESS, 'Force vend successful!')
    else:
        messages.add_message(request, messages.ERROR, 'Force vend failed (error code ' + str(ret) + ').')
    return redirect(reverse('cm_trays_view'))

# Vend a soda, and record the vend (i.e. charge people)
def buy_vend(request, trayId):

    errorMessage = None

    # Validate
    tray = get_object_or_404(Tray, pk=trayId)
    vendUser=request.user.get_vending()
    if tray.qty < 1:
        errorMessage = 'That tray is empty.'
    elif tray.price > vendUser.balance:
        errorMessage = 'You can\'t afford that item.'
    # TODO add vend-time restriction here

    # Process valid purchase
    if errorMessage is None:

        # Update DB values
        tray.qty -= 1
        vendUser.balance -= tray.price
        tray.save()
        vendUser.save()

        # Log purchase
        # TODO

        # Do vend
        ret=0 #do_vend(trayId)
        if ret != 0:
            errorMessage = 'Script failure: error code ' + str(ret) + '.'

    # Notify user of success/failure
    if errorMessage is None:
        messages.add_message(request, messages.SUCCESS, 'Vend successful!')
    else:
        messages.add_message(request, messages.ERROR, 'Vend failed: ' + errorMessage)
    return redirect(reverse('cm_trays_view'))
