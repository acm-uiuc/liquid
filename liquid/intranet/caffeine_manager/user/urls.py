from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.caffeine_manager.user.views.view'),
    url(r'^(?P<netid>\w+)$', 'intranet.caffeine_manager.user.views.view'),
    url(r'^(?P<netid>\w+)/edit$', 'intranet.caffeine_manager.user.views.edit'),
    url(r'^(?P<netid>\w+)/transfer$', 'intranet.caffeine_manager.user.views.transfer'),
)
