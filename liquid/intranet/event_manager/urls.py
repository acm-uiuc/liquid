from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.event_manager.views.main'),
    url(r'^new/$', 'intranet.event_manager.views.new'),
    url(r'^edit/(?P<id>\d+)$', 'intranet.event_manager.views.edit'),
    url(r'^delete/(?P<id>\d+)$', 'intranet.event_manager.views.delete'),
    url(r'^sendEmail/$', 'intranet.event_manager.views.send_email'),
)


