from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.sig_manager.views.main'),
    url(r'^new/$', 'intranet.sig_manager.views.new'),
    url(r'^edit/(?P<id>\d+)$', 'intranet.sig_manager.views.edit'),
    
)


