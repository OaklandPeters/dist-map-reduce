from __future__ import absolute_import
import abc
import collections
from ..timerange import TimeRange
from ..extern.clsproperty import VProperty


__all__ = ['QueryABC', 'Query']

class QueryABC(object):
    __metaclass__ = abc.ABCMeta
    ips = abc.abstractproperty()
    timerange = abc.abstractproperty()

class Query(QueryABC):
    def __init__(self, ips, timerange):
        self.ips = ips
        self.timerange = timerange

    def __repr__(self):
        return "{name}({ips}, {timerange})".format(
            name = type(self).__name__,
            ips = self.ips,
            timerange = self.timerange
        )
    
    @VProperty
    class ips(object):
        def _get(self):
            return self._ips
        def _set(self, value):
            self._ips = value
        def _val(self, value):
            return validate_ips(value)
            
    @VProperty
    class timerange(object):
        def _get(self):
            return self._timerange
        def _set(self, value):
            self._timerange = value
        def _val(self, value):
            return validate_timerange(value)

def validate_ips(ips):
    if isinstance(ips, basestring):
        return [ips]
    elif isinstance(ips, collections.Sequence):
        for elm in ips:
            if not isinstance(elm, basestring):
                raise TypeError("All 'ips' must be strings, not {0}".format(
                    type(elm).__name__
                ))
        return ips
    else:
        raise TypeError(str.format(
            "'ips' must be basestring or Sequence of basestrings, not {0}",
            type(ips).__name__
        ))

def validate_timerange(tr):
    if isinstance(tr, TimeRange):
        return tr
    elif isinstance(tr, (tuple, list)):
        if len(tr) == 2:
            return TimeRange(tr[0], tr[1])
        else:
            raise ValueError("'timerange' must be length 2")
    else:
        raise ValueError(str.format(
            "'timerange': expected TimeRange or list/tuple. Got {0}",
            type(tr).__name__
        ))


