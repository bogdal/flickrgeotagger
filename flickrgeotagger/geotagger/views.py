from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _
from flickrgeotagger.geotagger import GeoTagger

from .forms import UploadGpxFileForm
from .views_mixins import FlickrRequiredMixin


GEOTAGGER_SESSION_KEY = 'geotagger'


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class UploadFileView(FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadGpxFileForm

    def form_valid(self, form):
        session = {'gpx': form.gpx}
        self.request.session[GEOTAGGER_SESSION_KEY] = session
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('preview_photos')


class PreviewView(FlickrRequiredMixin, TemplateView):
    template_name = 'geotagger/preview.html'

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)
        self.gpx = (self.request.session
                    .get(GEOTAGGER_SESSION_KEY, {}).get('gpx'))

        context['gpx_file'] = self.gpx.gpx_file
        context['geotagger'] = GeoTagger(api=self.flickr_api,
                                         coordinates=self.gpx)
        return context
