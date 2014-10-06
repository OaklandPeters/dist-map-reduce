from __future__ import absolute_import
import datetime
from ..extern.clsproperty import VProperty

__all__ = ['TimeRange', 'range_contains', 'datetime_to_timestamp', 'timestamp_to_datetime']

class TimeRange(object):
    """
    Should have capacity to ask if one timerange is in another.
    Or if a timestamp is in a timerange range.
    """
    def __init__(self, start, end):
        # Validation occurs inside properties
        self.start = start
        self.end = end
        
        if not self.start <= self.end:
            raise ValueError("Start must be <= end")
        

    def __contains__(self, other):
        """Other should be a TimeRange, or float (timestamp)."""
        return range_contains(self.start, self.end, other)
#         if isinstance(other, timerange.timerange):
#             other = other.microsecond
#             return range_contains(self.start, self.end, other)
#         elif isinstance(other, float):
#             return range_contains(self.start, self.end, other)
#         elif isinstance(other, TimeRange):
#             return (self.start <= other.start) and (other.end <= self.end)
#         else:
#             raise TypeError("Cannot ask if TimeRange contains {0}".format(
#                 type(other).__name__))
        
    @VProperty
    class start(object):
        def _get(self):
            return self._start
        def _set(self, value):
            self._start = value
        def _val(self, value):
            return validate_timestamp(value, 'start')
    
    @VProperty
    class end(object):
        def _get(self):
            return self._end
        def _set(self, value):
            self._end = value
        def _val(self, value):
            return validate_timestamp(value, 'end')
    
    def __str__(self):
        return "{name}({start}, {end})".format(
            name = type(self).__name__,
            start = timestamp_to_datetime(self.start),
            end = timestamp_to_datetime(self.end)
        )
    def __repr__(self):
        return "({0}, {1}".format(repr(self.start), repr(self.end))

def validate_timestamp(value, name='object'):
    if isinstance(value, type(None)):
        return datetime_to_timestamp(datetime.datetime.now())
    elif isinstance(value, datetime.datetime):
        return datetime_to_timestamp(value)
    elif isinstance(value, float ):
        return value
    else:
        raise TypeError(str.format(
            "'{0}' should be timerange or float (timestamp), not {1}",
            name,
            type(value).__name__
        ))


#==============================================================================
#    Conversions
#==============================================================================
def get_total_seconds(delta):
    """Polyfill for 'delta.total_seconds' from Python 2.7"""
    if hasattr(delta, 'total_seconds'):
        return delta.total_seconds
    else:
        return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 1e6) / 1e6

def datetime_to_timestamp(dt):
    #return (dt - timerange.timerange(1970, 1, 1)).total_seconds()
    #return (dt - datetime.datetime(1970, 1, 1, 0, 0)).total_seconds()
    return get_total_seconds(dt - datetime.datetime(1970, 1, 1, 0, 0))
    
dt2ts = datetime_to_timestamp
    #return timerange.mktime(dt.timetuple())
    #
    #return dt.microsecond
    #return timerange.timerange(dt).microsecond

def timestamp_to_datetime(ts):
    return datetime.datetime.utcfromtimestamp(ts)
    #return timerange.timerange.fromtimestamp(ts)
    #return timerange.timerange.utcfromtimestamp(ts)
    #return timerange.timerange(ts)
ts2dt = timestamp_to_datetime

#==============================================================================
#    Time Range Inclusion
#==============================================================================
def range_contains(start, end, subject):
    """Predicate. Asks if subject is in range [start, end].
    subject can be float  (timestamp), timerange, or TimeRange
    """ 
    subject_start, subject_end = subject_bounds(subject)
    return (start <= subject_start) and (subject_end <= end)

def subject_bounds(subject):
    if isinstance(subject, datetime.datetime):
        return subject.microsecond, subject.microsecond
    elif isinstance(subject, float):
        return subject, subject
    elif isinstance(subject, TimeRange):
        return subject.start, subject.end
    else:
        raise TypeError("Cannot find timerange bounds for {0}.".format(
            type(subject).__name__
        ))
