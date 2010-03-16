from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.library.views',

    # Local editing
    url(r'^local-editing/$', 'local_editing', name='local_editing'),
    url(r'^local-editing/bulk-download.tar$', 'bulk_download', name='bulk_download'),
    url(r'^local-editing/bulk-upload/$', 'bulk_upload', name='bulk_upload'),
)
