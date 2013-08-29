from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # /banks
    url(r'^$', 'banks.views.main'),
    # /banks/posts/:_id
    url(r'^posts/(?P<id>\d+)$', 'banks.views.new')
    # /banks/posts/new
    url(r'^posts/new/$', 'banks.views.new')
    #  /banks/posts/edit/:_id
    url(r'^posts/edit(?P<id>\d+)$', 'banks.views.edit')
    # /banks/posts/delete/:_id
    url(r'^posts/delete/(?P<id>\d+)$', 'banks.views.delete')
)


