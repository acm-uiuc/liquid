from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'conf.views.main', name="conference_main"),
    url(r'^jobfair$', 'conf.views.jobfair', name="conference_jobfair"),
)