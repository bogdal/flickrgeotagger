from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.conf import settings

from .decorators import require_flickr_auth
from . import get_api_instance


class FlickrAuthRequiredMixin(object):

    @method_decorator(require_flickr_auth)
    def dispatch(self, request, flickr_api, *args, **kwargs):
        self.flickr_api = flickr_api
        return (super(FlickrAuthRequiredMixin, self)
                .dispatch(request, *args, **kwargs))


class CallbackView(RedirectView):

    def get(self, request, *args, **kwargs):

        flickr_api = get_api_instance(request)

        session = request.session
        oauth = flickr_api.flickr_oauth
        oauth.resource_owner_key = session.get('request_token')
        oauth.resource_owner_secret = session.get('request_token_secret')
        oauth.requested_permissions = session.get('requested_permissions')

        verifier = request.GET.get('oauth_verifier')
        flickr_api.get_access_token(verifier)

        session['oauth_token'] = flickr_api.flickr_oauth.token

        return super(CallbackView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return getattr(settings, 'FLICKR_CALLBACK_REDIRECT_URL', '/')
