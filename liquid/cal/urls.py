from django.conf.urls.defaults import patterns, include, url
from cal.event_feed import EventFeed

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cal.views.main'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', 'cal.views.main'),
    url(r'^details/(?P<id>\d+)/$', 'cal.make_calendar_file.details',name='event_details'),

    url(r'^feed.ics$',EventFeed()),
)


