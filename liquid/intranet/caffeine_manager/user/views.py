from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from intranet.models import Member, Vending
from utils.group_decorator import group_admin_required
from django.core.urlresolvers import reverse
from intranet.caffeine_manager.user.forms import VendingForm
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

def view(request, netid=None):
    search_arg=request.GET.get('q') or ''
    vend_user=None
    is_caffeine_admin=request.user.is_group_admin('Caffeine')

    if search_arg:
        users=Member.objects.filter(
          Q(first_name=search_arg) |
          Q(last_name=search_arg) |
          Q(username=search_arg)
        )

        if users:
            vend_users = [u.get_vending() for u in users]
            vend_user = max(vend_users, key=lambda v: (v.spent, -v.balance)).user

    elif netid:
        vend_user=get_object_or_404(Member, username=netid)
    elif not search_arg:
        vend_user=request.user

    vending=vend_user.get_vending() if vend_user else None
    can_transfer = vend_user and vend_user != request.user

    return render_to_response(
     'intranet/caffeine_manager/user/user.html',
     {
       'section':'intranet',
       'page':'caffeine',
       'sub_page':'users',
       'is_caffeine_admin':is_caffeine_admin,
       'vend_user':vend_user,
       'vending':vending,
       'search_arg':search_arg,
       'can_transfer':can_transfer
     }, context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def edit(request, netid):
    vend_user=get_object_or_404(Member, username=netid)
    vending=vend_user.get_vending()
    user_form=None;

    if request.method == 'POST':
        user_form=VendingForm(request.POST, instance=vending)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('cm_user_view', args=[vend_user.username]))
    else:
        user_form=VendingForm(instance=vending)

    return render_to_response(
      'intranet/caffeine_manager/user/edit_user.html',
      {
        'section':'intranet',
        'page':'caffeine',
        'form':user_form,
        'is_transfer':False
      }, context_instance=RequestContext(request))

def transfer(request, netid):
    vend_user=get_object_or_404(Member, username=netid)
    vending=vend_user.get_vending()
    user_form=None;

    # Prevent transferring to yourself, since that causes nasty concurrence errors
    if netid == request.user.username:
        messages.add_message(request, messages.ERROR, 'You can\'t transfer money to yourself.')
        return redirect(reverse('cm_user_view'))

    if request.method == 'POST':
        user_form=VendingForm(request.POST, instance=vending)

        if user_form.is_valid():
            debtor=request.user.get_vending()
            amount=Decimal(user_form['balance'].value())

            if Decimal(amount) <= 0:
                user_form.errors['balance']=['Transfer amount must be a number greater than $0.00.']
            elif debtor.balance < amount:
                user_form.errors['balance']=['Transfer amount must not be more than your current balance.']
            else:
                debtor.balance -= amount

                vending=vend_user.get_vending() # Get a clean copy
                vending.balance += amount

                debtor.save()
                vending.save()

                return redirect(reverse('cm_user_view', args=[vend_user.username]))
    else:
        user_form=VendingForm(instance=vending)

    user_form.fields['balance'].label='Transfer amount'
    return render_to_response(
      'intranet/caffeine_manager/user/edit_user.html',
      {
        'section':'intranet',
        'page':'caffeine',
        'form':user_form,
        'is_transfer':True
      }, context_instance=RequestContext(request))
 
