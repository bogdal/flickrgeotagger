from django.views.generic import FormView, TemplateView
from flickrgeotagger.flickr.views import FlickrAuthRequiredMixin
from flickrgeotagger.geotagger.forms import UploadFileForm


class HomeView(TemplateView):
    template_name = 'geotagger/home.html'


class UploadFileView(FlickrAuthRequiredMixin, FormView):
    template_name = 'geotagger/upload_file.html'
    form_class = UploadFileForm
