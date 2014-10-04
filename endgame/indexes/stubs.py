from __future__ import absolute_import
import abc



__all__ = [
]

class IndexABC(object):
    __metaclass__ = abc.ABCMeta
    live = abc.abstractproperty()
    waken = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    def find(self, ip_list, timedelta):
        

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""

class RecordChunk(IndexABC):
    """Corresponds to a single log file."""



"""
Can be .live (in memory) or .dormant (on hard-drive)
Can be told to 'wake' (become live), or, if read from, wakes before responding
"""
# Setup web server
# Web server ~ Index
# 

# Correspondence:
# config_file <--> Index
#     entries = [...
#        FilePath: to config file, or to record file
#        URL: to another Web-index

#

#Perhaps future improvement:
# have the indexes track the time range of the things they contain
# so they can answer whether or not the time range is appropriate

