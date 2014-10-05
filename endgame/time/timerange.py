import datetime
from ..extern.clsproperty import VProperty

__all__ = ['TimeRange', 'range_contains', 'datetime_to_timestamp', 'timestamp_to_datetime']

# Unify int and long
integer_types = (int, long)

class TimeRange(object):
    """
    Should have capacity to ask if one timerange is in another.
    Or if a timestamp is in a time range.
    """
    def __init__(self, start, end):
        # Validation occurs inside properties
        self.start = start
        self.end = end
        
        if not self.start <= self.end:
            raise ValueError("Start must be <= end")
        

    def __contains__(self, other):
        """Other should be a TimeRange, or int (timestamp)."""
        return range_contains(self.start, self.end, other)
#         if isinstance(other, datetime.datetime):
#             other = other.microsecond
#             return range_contains(self.start, self.end, other)
#         elif isinstance(other, int):
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
    elif isinstance(value, integer_types ):
        return value
    else:
        raise TypeError(str.format(
            "'{0}' should be datetime or integer_type (int or long), not {1}",
            name,
            type(value).__name__
        ))


#==============================================================================
#    Conversions
#==============================================================================
def datetime_to_timestamp(dt):
    zero = datetime.datetime.fromtimestamp(0)
    return long((dt - zero).total_seconds() * 1000.0)
dt2ts = datetime_to_timestamp
    #return dt.microsecond
    #return datetime.datetime(dt).microsecond

def timestamp_to_datetime(ts):
    return datetime.datetime(microseconds=ts)
    #return datetime.datetime.utcfromtimestamp(ts)
    #return datetime.datetime(ts)
ts2dt = timestamp_to_datetime

#==============================================================================
#    Time Range Inclusion
#==============================================================================
def range_contains(start, end, subject):
    """Predicate. Asks if subject is in range [start, end].
    subject can be integer_types  (timestamp), datetime, or TimeRange
    """ 
    subject_start, subject_end = subject_bounds(subject)
    return (start <= subject_start) and (subject_end <= end)

def subject_bounds(subject):
    if isinstance(subject, datetime.datetime):
        return subject.microsecond, subject.microsecond
    elif isinstance(subject, integer_types ):
        return subject, subject
    elif isinstance(subject, TimeRange):
        return subject.start, subject.end
    else:
        raise TypeError("Cannot find time bounds for {0}.".format(
            type(subject).__name__
        ))
