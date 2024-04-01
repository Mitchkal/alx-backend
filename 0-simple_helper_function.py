#!/usr/bin/env python3
"""
function that takes in two int arguments and returns
a tuple with start and end index
"""


def index_range(page: int, page_size: int) -> tuple:
    """
    returns tuple with start and end index
    """
    if page <= 0 or page_size <= 0:
        return None

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index
