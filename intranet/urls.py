from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'intranet.views.main'),
    url(r'^faq/$', 'intranet.views.faq'),
    url(r'^group/', include('intranet.group_manager.urls')),
    url(r'^banks/', include('intranet.banks_manager.urls')),
    url(r'^members/', include('intranet.member_manager.urls')),
    url(r'^treasure_chest/', 'intranet.views.treasure_chest'),
)


