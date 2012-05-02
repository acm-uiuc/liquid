from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^(?P<netid>[a-zA-Z0-9]+)/(?P<key>[a-zA-Z0-9]+)$', 'vote.views.vote'),
)


