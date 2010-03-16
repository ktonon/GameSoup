from django import *


class BulkUploadForm(forms.Form):
    tarball = forms.FileField(label='Modules tarball')
