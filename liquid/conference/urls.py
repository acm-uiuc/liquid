from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'conference.views.main'),
    url(r'^2013/jobfair$', 'conference.views.jobfair'),
    url(r'^2013/jobfair/invite$', 'conference.views.jobfair_invite'),
    url(r'^2013/$', 'conference.views.main'),
    url(r'^subscribe/$', 'conference.views.subscribe')
)


