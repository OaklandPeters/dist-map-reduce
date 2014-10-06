from __future__ import absolute_import
import csv
import os
#from ..extern.unroll import unroll #multiline comprehensions
from ..interfaces import IndexABC, Record


class RecordChunk(IndexABC):
    """Corresponds to a single log file.
    Considered to be live when data != None
    
    @todo: data --> VProperty, assumed to be None or list
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
    
    def sleep(self):
        self.data = None
    def wake_up(self):
        self.data = list(self.read())

    def read(self):
        with open(self.filepath, 'rb') as infile:
            csvreader = csv.reader(infile)
            for row in csvreader:
                yield Record(row[0], row[1])

#     def find(self, query):
#         found = self.map(query)
#         reduced = self.reduce(found, query) 
#         return reduced
    
    def map(self, query):
        return list(self.imap(query))
    def imap(self, query):
        # Get records
        self.wake_up()
        for record in self.data:
            yield record
    def reduce(self, records, query):
        return list(self.ireduce(records, query))
    def ireduce(self, records, query):
        # Filter by the query
        for record in self.data:
            if record in query:
                yield record
    
    @property
    def awake(self):
        if self.data is None:
            return False
        else:
            return True
    @property
    def state(self):
        return self.awake
    def __str__(self):
        return "{name}({data})".format(
            name = type(self).__name__,
            data = str(self.data)
        )
    def __repr__(self):
        return "{name}({data})".format(
            name = type(self).__name__,
            data = repr(self.data)
        )
    
    #--------------------------------------------------------------------------
    #    Dispatching
    #--------------------------------------------------------------------------
    chunk_extensions = ['.csv']
    @classmethod
    def valid(cls, value):
        return cls.valid_recordpath(value)
    @classmethod
    def valid_recordpath(cls, filepath):
        """Identifies valid record source files."""
        if os.path.exists(filepath) and os.path.isfile(filepath):
            fname, fext = os.path.splitext(filepath)
            if fext in cls.chunk_extensions:
                return True
        return False