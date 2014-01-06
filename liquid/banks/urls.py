from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

     url(r'posts/new$', 'banks.views.new'),
     url(r'posts/(?P<slug>[-\w]+)/$', 'banks.views.viewPost'),
     url(r'posts/edit/(?P<slug>[-\w]+)/$', 'banks.views.edit'),
     url(r'posts/delete/(?P<slug>[-\w]+)/$', 'banks.views.delete'),
     url(r'$', 'banks.views.main'),
)


