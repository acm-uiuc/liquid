from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.main'),
    url(r'^about/', include('abouta.urls')),
    url(r'^calendar/', include('cal.urls')),
    url(r'^sigs/', include('sigs.urls')),
    url(r'^banks/', include('banks.urls')),
    url(r'^contact/', 'views.contact'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout'),
    url(r'^intranet/', include('intranet.urls')),
)

handler404 = 'django.views.defaults.page_not_found'

handler500 = 'django.views.defaults.server_error'


if settings.SERVE_STATIC:
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  urlpatterns += staticfiles_urlpatterns()
