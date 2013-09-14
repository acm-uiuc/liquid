from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

#    # -- Posts Routes --
#    # /banks/posts/:_id
#    url(r'^posts/(?P<id>\d+)$', 'banks.views.viewPost'),
#    # /banks/posts/new
#    url(r'^posts/new/$', 'banks.views.new'),
#    #  /banks/posts/edit/:_id
#    url(r'^posts/edit(?P<id>\d+)$', 'banks.views.edit'),
#    # /banks/posts/delete/:_id
#    url(r'^posts/delete/(?P<id>\d+)$', 'banks.views.delete'),


    # /banks/posts/new
     url(r'/posts/new$', 'banks.views.new'),
     # /banks/posts/:_id
     url(r'/posts/(?P<slug>[-\w]+)/$', 'banks.views.viewPost'),
     #  /banks/posts/edit/:_id
     url(r'/posts/edit/(?P<slug>[-\w]+)/$', 'banks.views.edit'),
     # /banks/posts/delete/:_id
     url(r'/posts/delete/(?P<slug>[-\w]+)/$', 'banks.views.delete'),
     # /banks
     url(r'/$', 'banks.views.main'),
)

