from __future__ import absolute_import
import abc
from endgame.timerange import TimeRange

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
        elif isinstance(timerange, (tuple, list)):
            if len(timerange) == 2:
                self.timerange = TimeRange(timerange[0], timerange[1])
            else:
                raise ValueError("'timerange' must be length 2")
            #self.timerange = TimeRange(timerange)
        else:
            raise ValueError(str.format(
                "'timerange': expected TimeRange or list/tuple. Got {0}",
                type(timerange).__name__
            ))