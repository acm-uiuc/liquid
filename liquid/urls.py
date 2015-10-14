from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
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
    url(r'^conf/', include('conf.urls')),
    url(r'^corporate/', include('corporate.urls')),
    url(r'^contact/$', 'views.contact'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^intranet/', include('intranet.urls')),
    #url(r'^conference/', include('conference.urls')),

    url(r'^vpnrequired/$', 'views.vpnRequired'),
    url(r'^resume/$', redirect_to, {'url': '/corporate/resume/'}),
    url(r'^print/$', redirect_to, {'url':
        'https://www-s.acm.uiuc.edu/confluence/display/admin/Printing'}),
    url(r'^3dprint/$', redirect_to, {'url':
        'https://illinois.edu/fb/sec/1826253'}),
 
    #sigmusic redirects
    url(r'^chroma/$',redirect_to, {'url': '/sigmusic/chroma'}),
    url(r'^cosmos/$',redirect_to, {'url': '/sigmusic/cosmos'}),

    url(r'^cron/', include('cron.urls')),

    url(r'^RP/$',redirect_to, {'url': '/rp'}),
)

handler404 = 'django.views.defaults.page_not_found'

handler500 = 'django.views.defaults.server_error'


if settings.SERVE_STATIC:
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  urlpatterns += staticfiles_urlpatterns()
