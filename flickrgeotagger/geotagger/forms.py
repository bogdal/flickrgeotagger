from StringIO import StringIO
import urllib2
from urlparse import urlparse

from django import forms
from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from pytz import common_timezones

from . import GpxBackend, BackendException
from .widgets import DropboxChooserWidget


class GpxMixinForm(forms.Form):

    gpx = None

    def get_gpx_backend(self, gpx_file):
        try:
            gpx = GpxBackend(gpx_file)
        except BackendException:
            message = _("Error parsing file")
            self._errors['__all__'] = self.error_class([message])
        else:
            return gpx


class UploadGpxFileForm(GpxMixinForm):

    gpx_file = forms.FileField()

    def clean(self):
        data = self.cleaned_data

        if data.get('gpx_file'):
            self.gpx = self.get_gpx_backend(data.get('gpx_file'))

        return data


class DropboxChooserForm(GpxMixinForm):

    chooser = forms.CharField(label='', widget=DropboxChooserWidget(
        attrs={'data-extensions': '.gpx'}))

    def clean(self):
        data = self.cleaned_data
        url = data.get('chooser')

        if url:
            filename = urlparse(url).path.split('/')[-1]
            gpx_file = File(
                file=StringIO(urllib2.urlopen(url).read()), name=filename)
            self.gpx = self.get_gpx_backend(gpx_file)
        return data


class TimezoneForm(forms.Form):

    timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones])
