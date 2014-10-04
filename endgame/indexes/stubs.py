from __future__ import absolute_import
import abc
import operator
import functools

from ..interfaces import Query, Record
from ..dispatch import finder

__all__ = [
    'IndexABC',
    'IndexDispatcher',
    'RecordChunk'
]




class IndexABC(object):
    """
    @todo: Give MutableSequence behavior, based on data. Inherit from BasicMutableSequence
    
    """
    __metaclass__ = abc.ABCMeta
    live = abc.abstractproperty()
    state = abc.abstractproperty()
    waken = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    data = abc.abstractproperty() # list of entries: IndexDispatcher or RecordChunk
    
        

    def find(self, query):
        """The recursion step. Combines map + reduce

        For now, assume accepts only 1 argument: query
        Todo: allow to accept either:
            find(ip_list, timerange)
                --> query = Query(ip_list, timerange)
                    return self.find(query)
            find(query)
        """
        # Map
        # found = map(finder(query), self.data)
        found = self.map(query)
        
        # Reduce
        # This step should be changed for RecordChunk indexes 
        # ... filter
        reduced = self.reduce(found, query) 
        
        return reduced
        
        
        
        
    def __iter__(self):
        return iter(self.data)
            

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, config_file):
        # Config file, or possibly direct keywords
        pass
    def map(self, query):
        return [
            elm.find(query)
            for elm in self.data
        ]
    def reduce(self, records, query):
        """This step should be changed for RecordChunk indexes
        """
        return sorted(records, key=lambda record: record.timestamp)    

class RecordChunk(IndexABC):
    """Corresponds to a single log file."""
    def map(self, query):
        # Get records
        self.awaken()
        for record in self:
            yield record
        
    def reduce(self, records, query):
        # Filter by timerange
        timerange = TimeRange(query.timerange)
        found = [
            record
            for record in self
            if record.timestamp in timerange
            and record.ip in query.ips
        ]

# Setup web server
# Web server ~ Index
# 

# Correspondence:
# config_file <--> Index
#     entries = [...
#        FilePath: to config file, or to record file
#        URL: to another Web-index

#
# Live: in memory, potentially with associated web-server
# Dormant: on hard-drive (as config file and/or csv file)
#
# Can be told to 'wake' (become live)
# If queried, wakes before responding


#Perhaps future improvement:
# have the indexes track the time range of the things they contain
# so they can answer whether or not the time range is appropriate

