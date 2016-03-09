from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from intranet.caffeine_manager.views import leaderboard

urlpatterns=patterns('',
    url(r'^$', redirect_to, {'url': '/intranet/caffeine/trays'}),
    url(r'^stats/$', leaderboard, name='cm_stats'),

    url(r'^user/', include('intranet.caffeine_manager.user.urls')),
    url(r'^soda/', include('intranet.caffeine_manager.soda.urls')),
    url(r'^trays/', include('intranet.caffeine_manager.trays.urls'))
)
