from __future__ import absolute_import

from .recordchunk import RecordChunk
from .urldispatcher import URLDispatcher


import os
print(os.getcwd())
print()

from .indexdispatcher import IndexDispatcher
from ..extern.abf import ABFMeta



class ClassifyIndex(object):
    """typeswitch(basestring: instring) --> IndexABC
    Operator-style (Abstract Base Function) class.
    
    Based on instring, construct and return an appropriate index type - one
    descendant of IndexABC (RecordChunk or IndexDispatcher or URLDispatcher).
    
    instring: basestring, usually read from IndexDispatcher's config file
    
    Ex.
    # self = IndexDispatcher()
    for elm in self.data:
        yield ClassifyIndex.string(elm)(elm)
        #     RecordChunk(elm)
    """
    __metaclass__ = ABFMeta
    index_types = [RecordChunk, IndexDispatcher, URLDispatcher]
    @classmethod
    def __call__(cls, instring):
        return cls.string(instring)
    @classmethod
    def string(cls, instring):
        """Classify based on string input. Equivalent to:
        if RecordChunk.valid(elm):
            return RecordChunk
        if IndexDispatcher.valid(elm):
            return IndexDispatcher #...
        """
        for index in cls.index_types:
            if index.valid(instring):
                return index