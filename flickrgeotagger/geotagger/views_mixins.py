import urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from flickr import FlickrAPI


class FlickrRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        tokens = request.user.social_auth.get(provider='flickr').tokens
        tokens = dict(urlparse.parse_qsl(tokens.get('access_token')))

        self.flickr_api = FlickrAPI(
            api_key=settings.FLICKR_APP_ID,
            api_secret=settings.FLICKR_API_SECRET,
            oauth_token=tokens.get('oauth_token'),
            oauth_token_secret=tokens.get('oauth_token_secret'))

        return (super(FlickrRequiredMixin, self)
                .dispatch(request, *args, **kwargs))


class ActiveMenuMixin(object):
    active_menu = ''

    def get_context_data(self, **kwargs):
        context = super(ActiveMenuMixin, self).get_context_data(**kwargs)
        context['active'] = self.active_menu
        return context
