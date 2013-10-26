
CACHE_ATTRIBUTES_LIST = '_cache_attributes'


def cache(name):
    def _wrapper(func):
        def _decorated(self, *args, **kwargs):
            if hasattr(self, name):
                return getattr(self, name)
            result = func(self, *args, **kwargs)
            setattr(self, name, result)
            cache_attributes = getattr(self, CACHE_ATTRIBUTES_LIST, [])
            if not name in cache_attributes:
                cache_attributes.append(name)
            setattr(self, CACHE_ATTRIBUTES_LIST, cache_attributes)
            return result
        return _decorated
    return _wrapper
