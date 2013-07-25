from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.utils.translation import ugettext_lazy as _
from flickrgeotagger.flickr.views import FlickrAuthRequiredMixin
from flickrgeotagger.geotagger.forms import UploadFileForm


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class UploadFileView(FlickrAuthRequiredMixin, FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadFileForm

    def form_valid(self, form):
        photos = form.get_photos(self.flickr_api)
        self.request.session['photos'] = photos
        messages.success(self.request,
                         _("%(count)d photos were found on flickr" %
                           {'count': len(photos)}))
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return "/"