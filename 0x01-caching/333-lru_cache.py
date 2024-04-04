#!/usr/bin/env python3
"""
last recently used caching
"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):

    """
    Least recently usedcaching
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """
        caches item using LIRU
        """
        if key is None or item is None:
            return
        # add item to cache
        self.cache_data.update({key: item})
        # check if cache item is greater than max

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # if so, pop lru item
            lru = self.keys.pop(0)
            # delete lru item from cache
            del self.cache_data[lru]
            print(f"DISCARD: {lru}")
        if key not in self.keys:
            self.keys.append(key)
        else:
            if self.keys[-1] != key:
                self.keys.remove(key)
                self.keys.append(key)

    def get(self, key):
        """
        retrieves item from cache
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
