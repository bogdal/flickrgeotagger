from django.conf import settings
from django.contrib.gis.geoip import GeoIP

from pytz import country_timezones


def get_user_timezone(request):
    ip_addr = request.META['REMOTE_ADDR']
    user_timezone = settings.TIME_ZONE

    geoip = GeoIP()
    country_code = geoip.country(ip_addr).get('country_code')
    if country_code:
        timezones = country_timezones(country_code)
        user_timezone = timezones[0] if timezones else user_timezone

    return user_timezone
