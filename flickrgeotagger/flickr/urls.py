from django.conf.urls import patterns, url

from flickrgeotagger.flickr.views import CallbackView


urlpatterns = patterns(
    '',
    url(r'^callback/$', CallbackView.as_view(), name='flickr_callback')
)
