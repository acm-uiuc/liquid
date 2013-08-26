from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^companies$', 'intranet.jobfair_manager.views.companies'),
    url(r'^companies/new$', 'intranet.jobfair_manager.views.companies_new'),
    url(r'^companies/edit/(?P<id>\d+)$', 'intranet.jobfair_manager.views.companies_edit'),
    url(r'^companies/delete/(?P<id>\d+)$', 'intranet.jobfair_manager.views.companies_delete'),
    url(r'^companies/invite/(?P<id>\d+)$', 'intranet.jobfair_manager.views.companies_invite'),
)
