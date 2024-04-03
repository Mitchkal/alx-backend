#!/usr/bin/env python3
"""
FIFO caching
"""


BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFO caching inheriting from Base
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()

    def put(self, key, item):
        """
        stores items in cache using FIFO
        """
        if key is not None and item is not None:

            self.cache_data.update({key: item})

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                del_key = next(iter(self.cache_data))
                del self.cache_data[del_key]
                print(f"DISCARD: {del_key}")
            # self.cache_data.update({key: item})

    def get(self, key):
        """
        retrieves cache item given key
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
