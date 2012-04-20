from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'intranet.chroma.views.main'),
    url(r'^pull$','intranet.chroma.views.pull'),
    url(r'^play/(?P<id>\d+)$', 'intranet.chroma.views.play',name='play_animation'),
    url(r'^off$', 'intranet.chroma.views.off',name='animations_off'),
)


