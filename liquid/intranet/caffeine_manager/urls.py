from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.caffeine_manager.soda.views.allsodas'),
    url(r'^stats/$', 'intranet.caffeine_manager.views.leaderboard'),

    url(r'^user/', include('intranet.caffeine_manager.user.urls')),
    url(r'^soda/', include('intranet.caffeine_manager.soda.urls')),
    url(r'^trays/', include('intranet.caffeine_manager.trays.urls'))
)
