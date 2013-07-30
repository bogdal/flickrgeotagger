from django.conf import settings
import flickrapi


def get_api_instance(request):
    kwargs = {
        'api_key': unicode(settings.FLICKR_API_KEY),
        'secret': unicode(settings.FLICKR_API_SECRET),
    }
    if not getattr(settings, 'FLICKR_OAUTH_TOKEN_CACHE', False):
        kwargs.update({
            'token': request.session.get('oauth_token'),
            'store_token': False
        })
    return flickrapi.FlickrAPI(**kwargs)
