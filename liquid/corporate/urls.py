from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'corporate.views.main'),
    url(r'^job/$', 'corporate.views.job'),
    url(r'^job/thanks/$', 'corporate.views.thanks'),
    url(r'^resume/', include('corporate.resume.urls')),
    url(r'^sponsor/', 'corporate.views.sponsor', name="sponsorship_info"),
)


 