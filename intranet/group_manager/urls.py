from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.group_manager.views.main'),
    url(r'^new/$', 'intranet.group_manager.views.new'),
    url(r'^edit/(?P<id>\d+)$', 'intranet.group_manager.views.edit'),
    
)


