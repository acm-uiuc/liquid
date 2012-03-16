from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'acm.views.main'),
    url(r'about/^$', 'acm.views.about'),
)

urlpatterns += staticfiles_urlpatterns()
