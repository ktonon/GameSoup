from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.library.views',
    # Documentation
    url(r'^interface/documentation/$', 'multiple_interface_documentation', name='multiple_interface_documentation'),
    url(r'^interface/(?P<interface_id>\d+)/documentation/$', 'interface_documentation', name='interface_documentation'),
    
    # Local editing
    url(r'^local-editing/$', 'local_editing', name='local_editing'),
    url(r'^local-editing/bulk-download.tar$', 'bulk_download', name='bulk_download'),
    url(r'^local-editing/bulk-upload/$', 'bulk_upload', name='bulk_upload'),
)
