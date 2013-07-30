from django import forms
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from pytz import timezone
import gpxpy
import gpxpy.gpx
from timezone_field import TimeZoneFormField


class UploadFileForm(forms.Form):

    gpx_file = forms.FileField()
    timezone = TimeZoneFormField()

    def clean_gpx_file(self):
        data = self.cleaned_data.get('gpx_file')

        try:
            self.gpx = gpxpy.parse(data)
        except gpxpy.gpx.GPXXMLSyntaxException:
            raise forms.ValidationError(_("Error parsing file"))

        return data

    def get_photos(self, flickr_api):
        self.full_clean()

        user_timezone = timezone('Europe/Warsaw') # @TODO

        utc = timezone('UTC')
        date_format = "%Y-%m-%d %H:%M:%S"

        min_taken_date, max_taken_date = self.gpx.get_time_bounds()
        min_taken_date = utc.localize(min_taken_date).astimezone(user_timezone)
        max_taken_date = utc.localize(max_taken_date).astimezone(user_timezone)

        flickr_photos = flickr_api.get('flickr.photos.search',
                                       params={
                                           'user_id': 'me',
                                           'has_geo': 1,
                                           'min_taken_date': min_taken_date,
                                           'max_taken_date': max_taken_date,
                                           'extras':
                                                "geo,url_t,url_s,date_taken"})

        photos_with_location = []
        for photo in flickr_photos.get('photos').get('photo'):
            taken = datetime.strptime(photo.get('datetaken'), date_format)
            taken = user_timezone.localize(taken)

            taken_utc = taken.astimezone(utc).replace(tzinfo=None)
            gpx_locations = self.gpx.get_location_at(taken_utc)
            if gpx_locations:
                gpx_location = gpx_locations.pop()

                photos_with_location.append({
                    'id': photo.get('id'),
                    'title': photo.get('title'),
                    'taken': taken,
                    'url': photo.get('url_s'),
                    'latitude': gpx_location.latitude,
                    'longitude': gpx_location.longitude
                })

        return photos_with_location
