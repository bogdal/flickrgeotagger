from django import forms


class UploadFileForm(forms.Form):

    gpx_file = forms.FileField()
