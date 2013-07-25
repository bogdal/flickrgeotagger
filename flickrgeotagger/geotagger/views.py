from django.views.generic import FormView, TemplateView
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
        self.request.session['photos'] = form.get_photos(self.flickr_api)
        return super(UploadFileView, self).form_valid(form)

    def get_success_url(self):
        return "/"