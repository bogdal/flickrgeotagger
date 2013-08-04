from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _

from .forms import UploadGpxFileForm
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
        geotagger = form.get_geotagger(self.flickr_api)
        self.request.session[GEOTAGGER_SESSION_KEY] = geotagger
        messages.success(self.request,
                         _("%(count)d photos were found on flickr" %
                           {'count': len(geotagger.get_localized_photos())}))
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('preview_photos')


class PreviewView(FlickrRequiredMixin, TemplateView):
    template_name = 'geotagger/preview.html'

    def dispatch(self, request, *args, **kwargs):
        self.geotagger = request.session.get(GEOTAGGER_SESSION_KEY)
        if not self.geotagger:
            return HttpResponseRedirect(reverse('upload_file'))
        return (super(PreviewView, self)
                .dispatch(request, *args, **kwargs))

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)
        context['geotagger'] = self.geotagger
        return context
