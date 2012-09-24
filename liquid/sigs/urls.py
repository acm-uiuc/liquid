from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sigs.views.main'),
    url(r'^(?P<id>\d+)$', 'sigs.views.details'),
    url(r'^(?P<id>\d+)/subscribe$', 'sigs.views.subscribe'),
)


