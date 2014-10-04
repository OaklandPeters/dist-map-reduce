import datetime
from ..extern.clsproperty import VProperty

class TimeRange(object):
    """
    Should have capacity to ask if one timerange is in another.
    Or if a timestamp is in a time range.
    """
    def __init__(self, start, end):
        # Validation occurs inside properties
        self.start = start
        self.end = end
        
        if start > end:
            raise ValueError("Start must be <= end")
        

    def __contains__(self, other):
        """
        Other should be a TimeRange, or int (~TimeStamp)
        """
        return range_contains(self.start, self.end, other)
    def __repr__(self):
        return repr((self.start, self.end))
        
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
    
    
    
def validate_timestamp(value, name='object'):
    if isinstance(value, datetime.datetime):
        return datetime_to_timestamp(value)
    elif isinstance(value, int):
        return value
    else:
        raise TypeError(str.format(
            "'{0}' should be datetime or int, not {1}",
            name,
            type(value).__name__
        ))

def datetime_to_timestamp(dt):
    return datetime.datetime(dt).microsecond

def range_contains(start, end, subject):
    return start <= subject <= end
