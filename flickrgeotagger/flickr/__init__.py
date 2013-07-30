from django.conf import settings
import flickrapi


def get_api_instance(request):
    oauth_token = request.session.get('oauth_token')

    return flickrapi.FlickrAPI(
        unicode(settings.FLICKR_API_KEY),
        unicode(settings.FLICKR_API_SECRET),
        token=oauth_token,
        store_token=False)
