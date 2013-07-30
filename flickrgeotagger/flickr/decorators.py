from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from . import get_api_instance


def require_flickr_auth(view):

    def protected_view(request, *args, **kwargs):
        flickr_perms = getattr(settings, 'FLICKR_PERMS', 'read')

        flickr_api = get_api_instance(request)

        if not flickr_api.token_valid(perms=flickr_perms):
            callback = request.build_absolute_uri(reverse('flickr_callback'))
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
