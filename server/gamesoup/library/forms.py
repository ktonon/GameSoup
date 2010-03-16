from django import *


class BulkUploadForm(forms.Form):
    tarball = forms.FileField(help_text='A tarred archive containing JavaScript files which correspond to the Type.code fields you want to update. This should be in the same format as the file received from the Bulk Download page.')
