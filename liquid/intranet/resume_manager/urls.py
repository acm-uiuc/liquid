from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.resume_manager.views.main'),
    url(r'^thumb/(?P<id>\d+).png$', 'intranet.resume_manager.views.thumb'),
    url(r'^thumb/top/(?P<id>\d+).png$', 'intranet.resume_manager.views.thumb_top'),
)


