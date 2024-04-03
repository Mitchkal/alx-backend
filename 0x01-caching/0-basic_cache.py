#!/usr/bin/python3
"""
Module basic cache
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    inherits from BaseCaching
    """
    def __init__(self):
        """
        intitialization
        """
        super().__init__()

    def put(self, key, item):
        """
        assigns key and value to dict
        """
        if key is not None and item is not None:
            self.cache_data.update({key: item})

    def get(self, key):
        """
        returns dict value linked to key
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
