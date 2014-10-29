from django.shortcuts import render_to_response
from django.template import RequestContext
from intranet.models import Vending
from enum import Enum

# Enum of from locations
class fromLocations(Enum):
    ALL_SODAS = 'allsodas'
    TRAYS = 'trays'

def leaderboard(request):

    count = 5
    try:
        count = int(request.GET.get('count', 5))
    except:
        pass
    
    baseQuery=Vending.objects.all()

    top_calories=baseQuery.order_by('-calories')[0:count]
    top_caffeine=baseQuery.order_by('-caffeine')[0:count]
    top_spent=baseQuery.order_by('-spent')[0:count]
    top_sodas=baseQuery.order_by('-sodas')[0:count]

    is_caffeine_admin=request.user.is_group_admin('Caffeine')

    return render_to_response(
       'intranet/caffeine_manager/leaderboard.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'sub_page':'leaderboard',
         'is_caffeine_admin':is_caffeine_admin,
         'top_calories':top_calories,
         'top_caffeine':top_caffeine,
         'top_spent':top_spent,
         'top_sodas':top_sodas
       }, context_instance=RequestContext(request))
