from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.member_manager.views.main'),
    url(r'^new/$', 'intranet.member_manager.views.new'),
    url(r'^edit/(?P<id>\d+)$', 'intranet.member_manager.views.edit'),
    
)

