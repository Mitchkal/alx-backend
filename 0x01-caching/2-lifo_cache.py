#!/usr/bin/env python3
"""
last in first out caching
"""

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):

    """
    Last in First out caching
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        caches item using LIFO
        """
        if key is not None and item is not None:
            self.cache_data.update({key: item})

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                if self.keys:
                    del_key = self.keys.pop()
                    del self.cache_data[del_key]
                    print(f"DISCARD: {del_key}")

            self.keys.append(key)

    def get(self, key):
        """
        retrieves item from cache
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
