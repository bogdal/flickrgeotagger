from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from pytz import timezone, common_timezones
from flickrgeotagger.geotagger import GeoTagger, GpxBackend, BackendException


class UploadGpxFileForm(forms.Form):

    gpx_file = forms.FileField()
    timezone = forms.ChoiceField(choices=[(x, x) for x in common_timezones], initial=settings.TIME_ZONE)

    def clean(self):
        data = self.cleaned_data

        try:
            self.gpx = GpxBackend(data.get('gpx_file'), timezone(data.get('timezone')))
        except BackendException:
            raise forms.ValidationError(_("Error parsing file"))

        return data

    def get_geotagger(self, flickr_api):
        self.full_clean()
        return GeoTagger(api=flickr_api, coordinates=self.gpx)
