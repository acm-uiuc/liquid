from django.conf.urls.defaults import patterns, url
from intranet.caffeine_manager.soda.views import *

urlpatterns=patterns('',
    url(r'^$', 'intranet.caffeine_manager.soda.views.allSodas', name='cm_soda_allsodas'),
    url(r'^add/$', 'intranet.caffeine_manager.soda.views.add', name='cm_soda_add'),
    url(r'^edit/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.edit', name='cm_soda_edit'),
    url(r'^delete/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.delete', name='cm_soda_delete'),
    url(r'^vote/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.toggleVote', name='cm_soda_vote'),
    url(r'^clearvotes/(?P<sodaId>\d+)$', 'intranet.caffeine_manager.soda.views.clearVotes', name='cm_soda_clearvotes')
)
