import random


class Cache:
    def __init__(self, cache_size):
        self.cache = dict()
        self.cache_size = cache_size

    def checkCache(self, so_instance, lucky_charm):
        if lucky_charm in self.cache:
            print "SERVING: " + lucky_charm + " FROM CACHE!"
            urlcache = self.cache[lucky_charm]
            so_instance.source = urlcache['source']
            so_instance.sourceObject = urlcache['sourceobj']
        else:
            self.cleanup_cache()
            so_instance.set_url(lucky_charm)
            cachentry = dict()
            cachentry['source'] = so_instance.source
            cachentry['sourceobj'] = so_instance.sourceObject
            self.cache[lucky_charm] = cachentry

    def cleanup_cache(self):
        if len(self.cache) == self.cache_size:
            choice = random.choice(self.cache.keys())
            print "CACHE SIZE EXCEEDED --> POPPING: " + choice
            self.cache.pop(choice)
