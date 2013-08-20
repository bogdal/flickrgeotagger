from datetime import datetime
import gpxpy
import gpxpy.gpx
from pytz import timezone


class Backend(object):

    def get_start_time(self):
        raise NotImplementedError()

    def get_end_time(self):
        raise NotImplementedError()

    def get_points(self):
        raise NotImplementedError()

    def get_location_at(self, time):
        raise NotImplementedError()


class BackendException(Exception):
    pass


class GpxBackend(Backend):

    utc = timezone('UTC')

    def __init__(self, data, timezone):
        try:
            self.gpx = gpxpy.parse(data)
        except gpxpy.gpx.GPXXMLSyntaxException:
            raise BackendException()
        self.timezone = timezone
        self.start_time, self.end_time = self.gpx.get_time_bounds()

    def get_start_time(self):
        return self.utc.localize(self.start_time).astimezone(self.timezone)

    def get_end_time(self):
        return self.utc.localize(self.end_time).astimezone(self.timezone)

    def get_points(self):
        points = []
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append({"latitude": point.latitude,
                                   "longitude": point.longitude})
        return points

    def get_location_at(self, time):
        time = (self.timezone.localize(time).astimezone(self.utc)
                .replace(tzinfo=None))
        gpx_locations = self.gpx.get_location_at(time)
        if gpx_locations:
            return gpx_locations.pop()


class GeoTagger(object):

    def __init__(self, api, coordinates):
        self.api = api
        self.coordinates = coordinates

    def __repr__(self):
        return (u"GeoTagger (api=%s, coordinates=%s)" %
                (self.api, self.coordinates))

    def get_time_from_string(self, time_as_string,
                             date_format="%Y-%m-%d %H:%M:%S"):
        return datetime.strptime(time_as_string, date_format)

    def get_localized_photos(self, **kwargs):
        if hasattr(self, '_get_localized_photos'):
            return self._get_localized_photos

        localized_photos = []

        photos = (self.api
                  .get('flickr.photos.search',
                       params={
                           'user_id': 'me',
                           'min_taken_date': self.coordinates.get_start_time(),
                           'max_taken_date': self.coordinates.get_end_time(),
                           'extras': "geo,url_t,url_s,date_taken"})
                  .get('photos'))

        for photo in photos.get('photo'):
            taken = self.get_time_from_string(photo.get('datetaken'))
            
            location = self.coordinates.get_location_at(taken)
            if location:

                localized_photos.append({
                    'id': photo.get('id'),
                    'title': photo.get('title'),
                    'taken': taken,
                    'url': photo.get('url_s'),
                    'latitude': location.latitude,
                    'longitude': location.longitude
                })

        setattr(self, '_get_localized_photos', localized_photos)
        return localized_photos
        
    def save_location(self, photos=None):
        if photos is None:
            photos = self.get_localized_photos()
        # @TODO
