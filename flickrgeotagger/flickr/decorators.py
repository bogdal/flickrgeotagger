from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import flickrapi


def require_flickr_auth(view):

    def protected_view(request, *args, **kwargs):
        flickr_perms = 'write'

        flickr_api = flickrapi.FlickrAPI(
            unicode(settings.FLICKR_API_KEY),
            unicode(settings.FLICKR_API_SECRET))

        if not flickr_api.token_valid(perms=flickr_perms):
            callback = "%s%s" % (settings.CANONICAL_BASE_URL,
                                 reverse('flickr_callback'))
            flickr_api.get_request_token(oauth_callback=callback)

            authorize_url = flickr_api.auth_url(perms=flickr_perms)
            request.session['request_token'] = (flickr_api.flickr_oauth
                                                .resource_owner_key)
            request.session['request_token_secret'] = (flickr_api.flickr_oauth
                                                       .resource_owner_secret)
            request.session['requested_permissions'] = (flickr_api.flickr_oauth
                                                        .requested_permissions)

            return HttpResponseRedirect(authorize_url)

        return view(request, flickr_api, *args, **kwargs)
    return protected_view
