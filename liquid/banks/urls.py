from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # /banks
    url(r'^$', 'banks.views.main'),
    # -- Posts Routes --
    # /banks/posts/:_id
    url(r'^posts/(?P<id>\d+)$', 'banks.views.viewPost'),
    # /banks/posts/new
    url(r'^posts/new/$', 'banks.views.new'),
    #  /banks/posts/edit/:_id
    url(r'^posts/edit(?P<id>\d+)$', 'banks.views.edit'),
    # /banks/posts/delete/:_id
    url(r'^posts/delete/(?P<id>\d+)$', 'banks.views.delete'),

    # -- Comments Routes --
    # /banks/comments/new/
    url(r"^comments/new/(\d+)/$", "add_comment"),
    # /banks/comments/delete_comment
    url(r"^/comments/delete_comment/(\d+)/$", "delete_comment"),
    # /banks/comments/delete_comment/:_id
    url(r"^/comments/delete_comment/(\d+)/(\d+)/$", "delete_comment")
)

