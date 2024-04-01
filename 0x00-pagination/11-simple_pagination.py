#!/usr/bin/env python3
"""
function that takes in two int arguments and returns
a tuple with start and end index
"""


import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    returns tuple with start and end index
    """
    if page <= 0 or page_size <= 0:
        return None

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index


class Server:
    """
    Server class to paginate a database of popular
    baby names
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __int__(self):
        """
        intialize dataset to none
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Cached dataset
        """

        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        finds indexes to paginate dataset and
        returns page of the dataset
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()

        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
