from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, TemplateView, View
from django.utils.translation import ugettext_lazy as _
from flickrgeotagger.geotagger import GeoTagger
from pytz import timezone

from .geoip_timezone import get_user_timezone
from .forms import UploadGpxFileForm, TimezoneForm
from .views_mixins import FlickrRequiredMixin, ActiveMenuMixin, AjaxViewMixin


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class UploadFileView(ActiveMenuMixin, FlickrRequiredMixin, FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadGpxFileForm
    active_menu = 'upload_file'

    def form_valid(self, form):
        user_timezone = get_user_timezone(self.request)
        geotagger = GeoTagger(api=self.flickr_api,
                              coordinates=form.gpx,
                              user_timezone=user_timezone)
        setattr(self.request, 'geotagger', geotagger)
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('preview_photos')


class PreviewView(ActiveMenuMixin, FlickrRequiredMixin, FormView):
    template_name = 'geotagger/preview.html'
    form_class = TimezoneForm
    active_menu = 'preview_photos'

    def dispatch(self, request, *args, **kwargs):
        if not request.geotagger:
            return HttpResponseRedirect(reverse('upload_file'))
        return (super(PreviewView, self)
                .dispatch(request, *args, **kwargs))

    def get_initial(self):
        return {'timezone': get_user_timezone(self.request)}

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)

        context['geotagger'] = self.request.geotagger

        return context

    def form_valid(self, form):
        user_timezone = timezone(form.cleaned_data['timezone'])
        self.request.geotagger.set_timezone(user_timezone)
        return self.render_to_response(
            self.get_context_data(form=form, geotagger=self.request.geotagger))


class SaveCoordinatesView(FlickrRequiredMixin, View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        request.geotagger.save_location()
        request.geotagger.clean_cache()
        return HttpResponse('')
