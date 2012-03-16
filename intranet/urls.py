from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.views.main'),
    url(r'^faq/$', 'intranet.views.faq'),
    url(r'^group/', include('intranet.group_manager.urls')),
)


