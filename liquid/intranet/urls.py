from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.views.main'),
    url(r'^group/', include('intranet.group_manager.urls')),
    url(r'^members/', include('intranet.member_database.urls')),
    url(r'^event/', include('intranet.event_manager.urls')),
    url(r'^jobs/', include('intranet.job_manager.urls')),
    url(r'^chroma/', include('intranet.chroma.urls')),
    url(r'^resume/', include('intranet.resume_manager.urls')),
    url(r'^jobfair_manager/', include('intranet.jobfair_manager.urls')),
)


