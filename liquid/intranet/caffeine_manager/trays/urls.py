from django.conf.urls.defaults import patterns, url

urlpatterns=patterns('',
    url(r'^$', 'intranet.caffeine_manager.trays.views.trays'),
    url(r'^add$', 'intranet.caffeine_manager.trays.views.add_tray'),
    url(r'^edit/(?P<trayId>\d+)$', 'intranet.caffeine_manager.trays.views.edit_tray'),
    url(r'^delete/(?P<trayId>\d+)$', 'intranet.caffeine_manager.trays.views.delete_tray'),
    url(r'^forcevend/(?P<trayId>\d+)$', 'intranet.caffeine_manager.trays.views.force_vend'),
)
