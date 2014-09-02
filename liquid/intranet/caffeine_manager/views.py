from django.shortcuts import render_to_response
from django.template import RequestContext
from intranet.models import Vending

def leaderboard(request):
    count = 5
    baseQuery = Vending.objects.filter(user__status = 'active')

    topCalories = baseQuery.order_by('-calories')[0:count]
    topCaffeine = baseQuery.order_by('-caffeine')[0:count]
    topSpent = baseQuery.order_by('-spent')[0:count]
    topSodas = baseQuery.order_by('-sodas')[0:count]

    return render_to_response(
       'intranet/caffeine_manager/leaderboard.html',
       {
         'section':'intranet',
         'page':'caffeine',
         'topCalories':topCalories,
         'topCaffeine':topCaffeine,
         'topSpent':topSpent,
         'topSodas':topSodas
       }, context_instance=RequestContext(request))
