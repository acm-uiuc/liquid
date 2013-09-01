from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'quotedb.views.main'),
    url(r'^\?page=\d{0}+)$', 'quotedb.views.main'),
    url(r'^add/$', 'quotedb.views.add'),
)


 
