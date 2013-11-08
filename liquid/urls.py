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
    url(r'^banks/', include('banks.urls')),
    url(r'^conf/$', 'views.conference'),
    url(r'^corporate/', include('corporate.urls')),
    url(r'^contact/$', 'views.contact'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^intranet/', include('intranet.urls')),
    url(r'^conference/', include('conference.urls')),

    url(r'^resume/$', redirect_to, {'url': '/corporate/resume/'}),
    url(r'^print/$', redirect_to, {'url': 
        'https://www-s.acm.uiuc.edu/confluence/display/admin/Printing'}),

    #temporary redirect for FB hackathon IRC
    url(r'^hackathon/$', redirect_to, {'url': 
        'http://calvinshirley.net/hackathon-irc'}),

    #rp redirects
    url(r'^mm/$',redirect_to, {'url': '/conference/2013/mechmania.html'}),
    url(r'^attend/$',redirect_to, {'url': '/conference/2013/register.html'}),
    url(r'^register/$',redirect_to, {'url': '/conference/2013/register.html'}),
    url(r'^helpout/$',redirect_to, {'url': '/conference/2013/volunteers.html'}),
    url(r'^schedule/$',redirect_to, {'url': '/conference/2013/schedule.html'}),
    url(r'^jobs/$',redirect_to, {'url': '/conference/2013/career_fairs.html'}),
    url(r'^jobfair/$',redirect_to, {'url': '/conference/2013/career_fairs.html'}),
    url(r'^startup/$',redirect_to, {'url': '/conference/2013/career_fairs.html'}),
    url(r'^startupfair/$',redirect_to, {'url': '/conference/2013/career_fairs.html'}),
    url(r'^mm-irc/$',redirect_to, {'url': 'http://webchat.freenode.net/?channels=%23%23mm19&uio=OT10cnVlde'}),

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
