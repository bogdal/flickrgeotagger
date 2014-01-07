from django import forms
from django.utils.translation import ugettext_lazy as _
from dropboxchooser_field.fields import DropboxChooserField
from pytz import common_timezones

from . import GpxBackend, BackendException


class UploadGpxFileForm(forms.Form):

    gpx_file = forms.FileField()

    def clean(self):
        data = self.cleaned_data

        if data.get('gpx_file'):
            self.gpx = self.get_gpx_backend(data.get('gpx_file'))

        return data

    def get_gpx_backend(self, gpx_file):
        try:
            gpx = GpxBackend(gpx_file)
        except BackendException:
            message = _("Error parsing file")
            self._errors['__all__'] = self.error_class([message])
        else:
            return gpx


class DropboxChooserForm(UploadGpxFileForm):

    dropbox_chooser = forms.CharField(widget=forms.HiddenInput, required=False)
    gpx_file = DropboxChooserField(extensions=['gpx'], label='')


class TimezoneForm(forms.Form):

    timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones])
