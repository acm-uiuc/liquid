from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.member_database.views.main'),
    url(r'^search$','intranet.member_database.views.search'),
    url(r'^new/$', 'intranet.member_database.views.new'),
    #url(r'^edit/(?P<id>\d+)$', 'intranet.member_manager.views.edit'),
    
)

