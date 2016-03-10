from django.conf.urls.defaults import patterns, url

urlpatterns=patterns('',
    url(r'^$', 'intranet.caffeine_manager.trays.views.view', name='cm_trays_view'),
    url(r'^add/$', 'intranet.caffeine_manager.trays.views.add_tray', name='cm_trays_add'),
    url(r'^edit/(?P<trayId>\d+)/$', 'intranet.caffeine_manager.trays.views.edit_tray', name='cm_trays_edit'),
    url(r'^delete/(?P<trayId>\d+)/$', 'intranet.caffeine_manager.trays.views.delete_tray', name='cm_trays_delete'),
    url(r'^forcevend/(?P<trayId>\d+)/$', 'intranet.caffeine_manager.trays.views.force_vend', name='cm_trays_forcevend'),
    url(r'^buyvend/(?P<trayId>\d+)/$', 'intranet.caffeine_manager.trays.views.buy_vend', name='cm_trays_buy_vend'),
)
