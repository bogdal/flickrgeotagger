from django.views.generic import RedirectView
from django.conf import settings

import flickrapi


class CallbackView(RedirectView):

    def get(self, request, *args, **kwargs):
        flickr_api = flickrapi.FlickrAPI(
            settings.FLICKR_API_KEY,
            settings.FLICKR_API_SECRET,
            store_token=False)

        request.session['token'] = (flickr_api
                                    .get_token(request.GET.get('frob')))

        return super(CallbackView, self).get(request, *args, **kwargs)
