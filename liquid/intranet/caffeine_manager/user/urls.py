from django.conf.urls.defaults import patterns, url

urlpatterns=patterns('',
    url(r'^$', 'intranet.caffeine_manager.user.views.view', name='cm_user_view'),
    url(r'^(?P<netid>\w+)/$', 'intranet.caffeine_manager.user.views.view', name='cm_user_view'),
    url(r'^(?P<netid>\w+)/edit/$', 'intranet.caffeine_manager.user.views.edit', name='cm_user_edit'),
    url(r'^(?P<netid>\w+)/transfer/$', 'intranet.caffeine_manager.user.views.transfer', name='cm_user_transfer'),
)
