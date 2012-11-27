from django.conf.urls.defaults import patterns, include, url
from cal.event_feed import EventFeed

urlpatterns = patterns('cal.views',
    # Examples:
    url(r'^$', 'cal.views.main'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', 'cal.views.main'),
    url(r'^details/(?P<id>\d+)/$', 'cal.views.details',name='event_details'),

    url(r'^feed.ics$',EventFeed()),
)


