from django.conf import settings
from django.http import HttpResponseRedirect

import flickrapi


def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''

    def protected_view(request, *args, **kwargs):
        token = request.session.get('token', None)

        flickr_api = flickrapi.FlickrAPI(
            settings.FLICKR_API_KEY,
            settings.FLICKR_API_SECRET,
            token=token,
            store_token=False)

        if token:
            # We have a token, but it might not be valid
            try:
                flickr_api.auth_checkToken()
            except flickrapi.FlickrError:
                token = None
                del request.session['token']

        if not token:
            # No valid token, so redirect to Flickr
            url = flickr_api.web_login_url(perms='write')
            return HttpResponseRedirect(url)

        return view(request, flickr_api, *args, **kwargs)
    return protected_view
