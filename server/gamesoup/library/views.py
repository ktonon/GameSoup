from django.contrib.admin.views.decorators import staff_member_required
from django.http import *
from django.shortcuts import *
from gamesoup.library.forms import *
from gamesoup.library.local_editing import pack_types, unpack_types
from gamesoup.library.models import *


@staff_member_required
def bulk_download(request):
    response = HttpResponse(mimetype='application/x-tar')
    pack_types(request.user.username, response)
    return response


@staff_member_required
def bulk_upload(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            error = False
            tarball = form.cleaned_data['tarball']
            try:
                messages = unpack_types(request.user.username, tarball)
            except ValueError, e:
                messages = [str(e)]
                error = True
            context = {
                'title': 'Bulk Upload Done',
                'bu_messages': messages,
                'error': error,
            }
            return render_to_response('admin/library/local-editing/bulk-upload-done.html', context)
    else:
        form = BulkUploadForm()
    context = {
        'title': 'Bulk Upload',
        'form': form,
    }
    return render_to_response('admin/library/local-editing/bulk-upload.html', context)
