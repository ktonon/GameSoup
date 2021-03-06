from django.conf.urls.defaults import *


urlpatterns = patterns('gamesoup.library.views',
    # Documentation
    url(r'^interface/documentation/$', 'multiple_interface_documentation', name='multiple_interface_documentation'),
    url(r'^interface/(?P<interface_id>\d+)/documentation/$', 'interface_documentation', name='interface_documentation'),
    url(r'^type/(?P<type_id>\d+)/parsed/$', 'parsed_type_code', name='parsed_type_code'),
    url(r'^type/(?P<type_id>\d+)/generate-code/$', 'generate_type_code', name='generate_type_code'),
    
    # Local editing
    url(r'^local-editing/$', 'local_editing', name='local_editing'),
    url(r'^local-editing/bulk-download.tar$', 'bulk_download', name='bulk_download'),
    url(r'^local-editing/bulk-upload/$', 'bulk_upload', name='bulk_upload'),
    
    # Templation
    url(r'^interface/(?:\d+|add)/possible-template-parameters/$', 'possible_method_template_parameters', name='possible_method_template_parameters'),
    url(r'^type/(?:\d+|add)/possible-template-parameters/$', 'possible_interface_template_parameters', name='possible_interface_template_parameters'),
)
