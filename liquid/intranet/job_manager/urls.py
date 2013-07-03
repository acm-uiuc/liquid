from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.job_manager.views.main'),
    url(r'^sendEmail', 'intranet.job_manager.views.send_job_email'),
)
