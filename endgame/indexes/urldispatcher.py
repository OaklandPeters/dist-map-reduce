"""

@todo: awake property
@todo: wake_up property
"""

from __future__ import absolute_import
import os
import json
from ..interfaces import IndexABC
from .indexdispatcher import IndexDispatcher
from .shared import is_nonstringsequence, directory_to_config

__all__ = ['URLDispatcher']

#class URLDispatcher(IndexDispatcher):
class URLDispatcher(IndexABC):
    """
    Interacts with a remote URL (which is expected to in turn be an IndexDispatcher).
    
    
    @todo: Overwrite read/write from IndexDispatcher
    
    """
    def __init__(self, urlpath):
        self.urlpath = self._validate_urlpath(urlpath)
        self.data = None # 'sleeping'
    
    #--------------------------------------------------------------------------
    #    Map/Reduce
    #--------------------------------------------------------------------------
    def map(self, query):
        self.wake_up()
        return [
            elm.find(query)
            for elm in self.data
        ]
    def reduce(self, records, query):
        """Flatten one-level of nesting, removing empty sequences, and then
        return records sorted by timestamp."""
        flattened = flatten(records)
        processed = sorted(flattened, key=lambda record: record.timestamp)
        return processed
    
    def make_url_string(self, ips, timerange):
        pass
        
    
    
    #--------------------------------------------------------------------------
    #    Wake/Sleep Interface
    #--------------------------------------------------------------------------
    @property
    def awake(self):
        # return True if self.urlpath responds to HTTP request
        pass
    def wake_up(self):
        """Cause destination to boot up the mini-server/initialize
        ... this may or may not be possible.
        In any case, it should be one of the last things coded
        """
        # Send HTTP request for list of data indexed by web-server
        
    def sleep(self):
        """Have the destination fold itself down to sleep."""
        for index in self.data:
            index.sleep()
        self.data = None
    
    #--------------------------------------------------------------------------
    #    Dispatching
    #--------------------------------------------------------------------------
    @classmethod
    def _validate_urlpath(cls, urlpath):
        """
        @todo: Expand this.
        """
        if not isinstance(urlpath, basestring):
            raise TypeError("'url' must be a basestring.")
        else: # string
            if urlpath.startswith("http://"):
                return urlpath
            else:
                raise ValueError("Invalid url.")
    @classmethod
    def valid_url(cls, url):
        try:
            cls._validate_url(url)
        except (ValueError, TypeError):
            return False
        else:
            return True
    @classmethod
    def valid(cls, value):
        return cls.valid_url(value)

    #--------------------------------------------------------------------------
    #    Magic Methods
    #--------------------------------------------------------------------------
    def __str__(self):
        return "{name}({data})".format(
            name = type(self).__name__,
            #data = str(self.data)
            #... limit length displayed
            data = [str(elm)[:20] for elm in self.data]
        )
    def __repr__(self):
        return "{name}({data})".format(
            name = type(self).__name__,
            #data = repr(self.data)
            #... limit length displayed
            data = [repr(elm)[:20] for elm in self.data]
        )

