from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.main'),
    url(r'^about/$', 'abouta.views.about'),
    url(r'^about/join/$', 'abouta.views.join'),
    url(r'^about/committees/$', 'abouta.views.committees'),
    url(r'^about/corporate/$', 'abouta.views.corporate'),
    url(r'^about/corporate/job/$', 'abouta.views.job'),
    url(r'^about/members/$', 'abouta.views.members'),
)

urlpatterns += staticfiles_urlpatterns()
