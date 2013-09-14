from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.quote.views.main'),
    url(r'^(?P<quote_id>\d+)$', 'intranet.quote.views.main'),
    url(r'^add/$', 'intranet.quote.views.add'),
    url(r'^edit/(?P<quote_id>\d+)$', 'intranet.quote.views.edit'),
)


 
