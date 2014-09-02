from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.caffeine_manager.soda.views.allsodas'),
    url(r'^add$', 'intranet.caffeine_manager.soda.views.add'),
    url(r'^edit/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.edit'),
    url(r'^delete/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.delete'),
    url(r'^vote/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.vote'),
    url(r'^clearvotes/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.clear_votes')
)
