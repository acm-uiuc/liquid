from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

urlpatterns=patterns('',
    url(r'^$', redirect_to, {'url': '/intranet/caffeine/soda'}),
    url(r'^stats/$', 'intranet.caffeine_manager.views.leaderboard'),

    url(r'^user/', include('intranet.caffeine_manager.user.urls')),
    url(r'^soda/', include('intranet.caffeine_manager.soda.urls')),
    url(r'^trays/', include('intranet.caffeine_manager.trays.urls'))
)
