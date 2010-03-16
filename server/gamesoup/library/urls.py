from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.library.views',
    (r'^local-editing/bulk-download/$', 'bulk_download'),
    (r'^local-editing/bulk-download.tar$', 'bulk_download'),
    (r'^local-editing/bulk-upload/$', 'bulk_upload'),
)
