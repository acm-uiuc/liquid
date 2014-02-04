from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.resume_manager.views.main'),
    url(r'^thumb/(?P<id>\d+).png$', 'intranet.resume_manager.views.thumb'),
    url(r'^thumb/top/(?P<id>\d+).png$', 'intranet.resume_manager.views.thumb_top'),
    url(r'^pdf/(?P<id>\d+).pdf$', 'intranet.resume_manager.views.pdf'),

    url(r'^reminder$', 'intranet.resume_manager.views.send_resume_reminders'),

    url(r'^accounts$', 'intranet.resume_manager.views.accounts'),
    url(r'^accounts/new/$', 'intranet.resume_manager.views.accounts_new'),
    url(r'^accounts/edit/(?P<id>\d+)$', 'intranet.resume_manager.views.accounts_edit'),
    url(r'^accounts/delete/(?P<id>\d+)$', 'intranet.resume_manager.views.accounts_delete'),
)
