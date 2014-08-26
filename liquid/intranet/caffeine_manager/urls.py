from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.caffeine_manager.views.main'),
    url(r'^stats/$', 'intranet.caffeine_manager.views.leaderboard'),
    url(r'^user/$', 'intranet.caffeine_manager.views.user'),
    url(r'^user/(?P<netid>\w+)$', 'intranet.caffeine_manager.views.user'),
    url(r'^user/(?P<netid>\w+)/edit$', 'intranet.caffeine_manager.views.edit_user'),

    url(r'^add$', 'intranet.caffeine_manager.views.add_soda'),
    url(r'^edit/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.views.edit_soda'),
    url(r'^delete/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.views.delete_soda'),

    url(r'^trays/$', 'intranet.caffeine_manager.views.trays'),


    url(r'^trays/add$', 'intranet.caffeine_manager.views.add_tray'),
    url(r'^trays/edit/(?P<trayId>\d+)$', 'intranet.caffeine_manager.views.edit_tray'),
    url(r'^trays/delete/(?P<trayId>\d+)$', 'intranet.caffeine_manager.views.delete_tray'),
)
