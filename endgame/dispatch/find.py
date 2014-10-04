from __future__ import absolute_import
import functools

__all__ = ['find', 'finder']

def find(query, index):
    """Dispatching operator.
    __contains is to operator.contains
    as
    find is to Index.find
    """
    return index.find(query)

def finder(query):
    return functools.partial(find, query)
