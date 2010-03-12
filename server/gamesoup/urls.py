from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^gamesoup/', include('gamesoup.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)


if settings.IS_LOCAL:
    urlpatterns += patterns('django.views.static',
        (r'^site-media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^django-admin-media/(?P<path>.*)$', 'serve', {'document_root': settings.ADMIN_MEDIA_ROOT}),
    )