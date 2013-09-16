from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.quote.views.main'),
    url(r'^(?P<quote_id>\d+)$', 'intranet.quote.views.main'),
    url(r'^add/$', 'intranet.quote.views.add'),
    url(r'^edit/(?P<quoteId>\d+)$', 'intranet.quote.views.edit'),
)


 
