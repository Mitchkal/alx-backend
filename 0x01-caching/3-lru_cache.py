#!/usr/bin/env python3
"""
least recently used caching
"""

from threading import RLock
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
        self.__rlock = RLock()
        self.register = []

    def put(self, key, item):
        """
        caches item using LRU
        """
        if key is None or item is None:
            return

        mru = self. _limit(key)
        with self.__rlock:
            self.cache_data.update({key: item})
        if mru is not None:
            print(f"DISCARD: {mru}")

    def get(self, key):
        """
        retrieves item from cache
        """
        with self.__rlock:
            if key in self.register:
                self._limit(key)

            return self.cache_data.get(key)

    def _limit(self, key):
        """
        deletes from cache when max
        """
        out = None

        with self.__rlock:
            if key not in self.register:
                if len(self.cache_data) == BaseCaching.MAX_ITEMS:
                    out = self.register.pop(0)
                    self.cache_data.pop(out)
            else:
                self.register.remove(key)
            self.register.insert(len(self.register), key)
        return out
