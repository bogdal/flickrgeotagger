from django import forms
from django.utils.translation import ugettext_lazy as _

from pytz import common_timezones

from . import GpxBackend, BackendException


class UploadGpxFileForm(forms.Form):

    gpx_file = forms.FileField()

    def clean(self):
        data = self.cleaned_data

        try:
            self.gpx = GpxBackend(data.get('gpx_file'))
        except BackendException:
            raise forms.ValidationError(_("Error parsing file"))

        return data


class TimezoneForm(forms.Form):

    timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones])
