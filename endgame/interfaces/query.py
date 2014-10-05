from __future__ import absolute_import
import abc
from ..time import TimeRange

__all__ = ['QueryABC', 'Query']

class QueryABC(object):
    __metaclass__ = abc.ABCMeta
    ips = abc.abstractproperty()
    timerange = abc.abstractproperty()

class Query(QueryABC):
    def __init__(self, ips, timerange):
        self.ips = ips
        if isinstance(timerange, TimeRange):
            self.timerange = timerange
        else:
            self.timerange = TimeRange(timerange)