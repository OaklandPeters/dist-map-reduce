from __future__ import absolute_import
import abc
from ..extern.clsproperty import VProperty

__all__ = ['RecordABC', 'Record']

class RecordABC(object):
    __metaclass__ = abc.ABCMeta
    ip = abc.abstractproperty()
    timestamp = abc.abstractproperty()


class Record(RecordABC, tuple):
    def __new__(cls, ip, timestamp):
        if not isinstance(timestamp, int):
            timestamp = int(timestamp)
        return tuple.__new__(cls, [ip, timestamp])

    def __str__(self):
        return "{name}({ip}, {ts})".format(
            name = type(self).__name__,
            ip = self.ip,
            ts = self.timestamp
        )

    @VProperty
    class ip(object):
        """IPv4 address"""
        def _get(self):
            return self[0]
        def _set(self, value):
            self[0] = value
        def _val(self, value):
            if not isinstance(value, basestring):
                raise TypeError("'ip' should be a basestring.")
            return value
    
    @VProperty
    class timestamp(object):
        """Timestamp. An integer. Microseconds since..."""
        def _get(self):
            return self[1]
        def _set(self, value):
            self[1] = value
        def _val(self, value):
            if not isinstance(value, int):
                raise TypeError("'timestamp' should be an integer.")
            return value

rec = Record('aa',123)
print(rec)
print()
