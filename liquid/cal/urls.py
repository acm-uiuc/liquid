from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cal.views.main'),
    url(r'(?P<page>\d+)/$', 'cal.views.main'),
    url(r'details/(?P<id>\d+)/$', 'cal.views.details',name='event_details'),
)


