from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _

from flickr import FlickrAPI

from .forms import UploadGpxFileForm

import urlparse


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


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class UploadFileView(FlickrRequiredMixin, FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadGpxFileForm

    def form_valid(self, form):
        photos = form.get_photos(self.flickr_api)
        self.request.session['photos'] = photos
        messages.success(self.request,
                         _("%(count)d photos were found on flickr" %
                           {'count': len(photos)}))
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return "/"