GEOTAGGER_SESSION_KEY = 'geotagger'


class GeoTaggerMiddleware(object):

    def process_request(self, request):
        try:
            geotagger = request.session[GEOTAGGER_SESSION_KEY]
        except KeyError:
            pass
        else:
            setattr(request, 'geotagger', geotagger)

    def process_response(self, request, response):
        if hasattr(request, 'geotagger'):
            request.session[GEOTAGGER_SESSION_KEY] = request.geotagger
        return response
