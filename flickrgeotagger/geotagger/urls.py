from django.conf.urls import patterns, url

from flickrgeotagger.geotagger.views import (UploadFileView, HomeView,
                                             PreviewView)


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_page'),
    url(r'^upload/$', UploadFileView.as_view(), name='upload_file'),
    url(r'^preview/$', PreviewView.as_view(), name='preview_photos'),
)
