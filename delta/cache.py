import random


class Cache:
    class __Cache:
        def __init__(self, cache_size):
            self.cache_size = cache_size
            self.cache = dict()

    instance = None

    def __init__(self, cache_size):
        if not Cache.instance:
            Cache.instance = Cache.__Cache(cache_size)
        else:
            print "Cannot create more instances of this..."

    def checkCache(self, so_instance, lucky_charm):
        if lucky_charm in self.instance.cache:
            print "SERVING: " + lucky_charm + " FROM CACHE!"
            urlcache = self.instance.cache[lucky_charm]
            # so_instance.source = urlcache['source']
            so_instance.sourceObject = urlcache['sourceobj']
        else:
            self.cleanup_cache()
            so_instance.set_url(lucky_charm)
            cachentry = dict()
            # cachentry['source'] = so_instance.source
            cachentry['sourceobj'] = so_instance.sourceObject
            self.instance.cache[lucky_charm] = cachentry

    def cleanup_cache(self):
        if len(self.instance.cache) == self.instance.cache_size:
            choice = random.choice(self.instance.cache.keys())
            print "CACHE SIZE EXCEEDED --> POPPING: " + choice
            self.instance.cache.pop(choice)
