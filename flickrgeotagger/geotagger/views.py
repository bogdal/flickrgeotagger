from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _
from flickrgeotagger.geotagger import GeoTagger
from pytz import timezone

from .geoip_timezone import get_user_timezone
from .forms import UploadGpxFileForm, TimezoneForm
from .views_mixins import FlickrRequiredMixin


GEOTAGGER_SESSION_KEY = 'geotagger'


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class UploadFileView(FlickrRequiredMixin, FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadGpxFileForm

    def form_valid(self, form):
        user_timezone = get_user_timezone(self.request)
        session = {
            'gpx': form.gpx,
            'geotagger': GeoTagger(api=self.flickr_api,
                                   coordinates=form.gpx,
                                   user_timezone=user_timezone)
        }
        self.request.session[GEOTAGGER_SESSION_KEY] = session
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('preview_photos')


class PreviewView(FlickrRequiredMixin, FormView):
    template_name = 'geotagger/preview.html'
    form_class = TimezoneForm

    def dispatch(self, request, *args, **kwargs):
        self.geotagger = (self.request.session.get(GEOTAGGER_SESSION_KEY, {}))
        return (super(PreviewView, self)
                .dispatch(request, *args, **kwargs))

    def get_initial(self):
        return {'timezone': get_user_timezone(self.request)}

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)

        context['gpx_file'] = self.geotagger.get('gpx').gpx_file
        context['geotagger'] = self.geotagger.get('geotagger')

        return context

    def form_valid(self, form):
        geotagger = self.geotagger.get('geotagger')
        geotagger.set_timezone(timezone(form.cleaned_data['timezone']))

        return self.render_to_response(
            self.get_context_data(form=form, geotagger=geotagger))