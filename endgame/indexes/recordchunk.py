from __future__ import absolute_import
import csv
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
        
    def map(self, query):
        # Get records
        self.wake_up()
        for record in self.data:
            yield record
        
    def reduce(self, records, query):
        # Filter by timerange
        return [
            record
            for record in self.data
            if record in query
            #if record.timestamp in query.timerange
            #and record.ip in query.ips
        ]
    
    @property
    def awake(self):
        if self.data is None:
            return True
        else:
            return False
    @property
    def state(self):
        return self.awake