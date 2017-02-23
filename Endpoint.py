class Endpoint(object):

    def __init__(self, id, dcl, caches):
        self.id = id
        self.base_latency = dcl
        self.cache_list = dict(caches)
        self.n_cache = len(caches)
