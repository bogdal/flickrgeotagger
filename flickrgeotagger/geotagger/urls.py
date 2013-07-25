from django.conf.urls import patterns, url

from flickrgeotagger.geotagger.views import UploadFileView, HomeView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^upload/$', UploadFileView.as_view(), name='upload_file'),
)
