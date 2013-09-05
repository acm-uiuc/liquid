from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.quotedb.views.main'),
    url(r'^add/$', 'intranet.quotedb.views.add'),
)


 
