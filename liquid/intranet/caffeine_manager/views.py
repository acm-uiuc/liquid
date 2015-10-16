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
        count = max(0, int(request.GET.get('count', 5)))
    except:
        pass
    
    subQuery = "SELECT uid from users WHERE status = 'active'"
    baseQuery = "SELECT * FROM vending WHERE uid IN (%s)" % subQuery

    top_calories=Vending.objects.raw(baseQuery + " ORDER BY -calories LIMIT %d" % count)
    top_caffeine=Vending.objects.raw(baseQuery + " ORDER BY -caffeine LIMIT %d" % count)
    top_spent=Vending.objects.raw(baseQuery + " ORDER BY -spent LIMIT %d" % count)
    top_sodas=Vending.objects.raw(baseQuery + " ORDER BY -sodas LIMIT %d" % count)

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
