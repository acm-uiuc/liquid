from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from utils.group_decorator import group_admin_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from intranet.models import VendingVoter
from intranet.caffeine_manager.soda.models import Soda
from intranet.caffeine_manager.soda.forms import SodaForm
from intranet.caffeine_manager.views import fromLocations

def allSodas(request):
    sodas=Soda.objects.all().order_by('-dispensed', 'name')
    voter=VendingVoter.objects.get(pk=request.user.id)
    for s in sodas:
        s.votedFor=(voter.votes.filter(pk=s.id).count() == 1)
        s.voteCount=VendingVoter.objects.filter(votes=s).count()

    request.session['from'] = fromLocations.ALL_SODAS

    is_caffeine_admin=request.user.is_group_admin('Caffeine')

    # Get paginator and page
    page=1
    paginator=Paginator(sodas, 10)
    page_arg=request.GET.get('page')
    if page_arg and page_arg.isdigit():
        page=int(page_arg)
        page=max(1, min(paginator.num_pages, page))
    sodasPage=paginator.page(page)

    return render_to_response(
     'intranet/caffeine_manager/soda/allsodas.html',
     {
       'section':'intranet',
       'page':'caffeine',
       'sub_page':'sodas',
       'sodasPage':sodasPage,
       'request':request,
       'is_caffeine_admin':is_caffeine_admin
     }, context_instance=RequestContext(request))


@group_admin_required(['Caffeine'])
def add(request):
    soda_form=None;
    from_arg=request.session.get('from', fromLocations.ALL_SODAS)
    if request.method == 'POST':
        soda_form=SodaForm(request.POST)
        if soda_form.is_valid():
            soda_form.save()
            return redirect(reverse('cm_soda_all_sodas'))
    else:
        soda_form=SodaForm()

    return render_to_response(
       'intranet/caffeine_manager/soda/edit_soda.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'form':soda_form,
         'from_arg':from_arg
       },
       context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def edit(request, sodaId):
    soda=get_object_or_404(Soda, pk=sodaId)
    soda_form=None;
    from_arg=request.session.get('from', fromLocations.ALL_SODAS)

    previous_url = reverse('cm_soda_allsodas')
    if from_arg == fromLocations.TRAYS:
        previous_url = reverse('cm_trays_view')

    if request.method == 'POST':
        soda_form=SodaForm(request.POST, instance=soda)
        if soda_form.is_valid():
            soda_form.save()
            return redirect(previous_url)
    else:
        soda_form=SodaForm(instance=soda)

    return render_to_response(
       'intranet/caffeine_manager/soda/edit_soda.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'form':soda_form,
         'id':sodaId,
         'previous_url':previous_url,
         'from_arg':from_arg
       }, context_instance=RequestContext(request))

@group_admin_required(['Caffeine'])
def delete(request, sodaId):
    get_object_or_404(Soda, pk=sodaId).delete()

    if request.session.get('from', fromLocations.ALL_SODAS) == fromLocations.TRAYS:
        return redirect(reverse('cm_trays_view'))
    return redirect(reverse('cm_soda_allsodas'))

def toggleVote(request, sodaId):
    voter=VendingVoter.objects.get(pk=request.user.id)
    has_voted=(voter.votes.filter(id=sodaId).count() > 0)
    if has_voted:
        voter.votes.remove(sodaId)
        messages.add_message(request, messages.INFO, 'Your vote has been removed!')
    else:
        voter.votes.add(sodaId)
        messages.add_message(request, messages.SUCCESS, 'Your vote has been recorded!')

    return redirect(reverse('cm_soda_allsodas'))

# @group_admin_required(['Caffeine'])
def clearVotes(request, sodaId):
    users = VendingVoter.objects.filter(votes=sodaId)
    for u in users:
        u.votes.remove(sodaId)
    messages.add_message(request, messages.INFO, 'Votes cleared.')
    return redirect(reverse('cm_soda_allsodas'))
