from __future__ import absolute_import
import os
from ..interfaces import IndexABC
from .recordchunk import RecordChunk
from .urldispatcher import URLDispatcher

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, filepath):
        # Config file, or possibly direct keywords
        self.filepath = filepath
        self.data = None # 'sleeping'
    def map(self, query):
        return [
            elm.find(query)
            for elm in self.data
        ]
    def reduce(self, records, query):
        """This step should be changed for RecordChunk indexes
        """
        return sorted(records, key=lambda record: record.timestamp)

    # Map/Reduce Interface
    #map = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    #reduce = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    
    # Wake/Sleep Interface
    @property
    def awake(self):
        if self.data is None:
            return True
        else:
            return False
    @property
    def state(self):
        return self.awake
    def sleep(self):
        self.data = None
    def wake_up(self):
        self.data = list(self.wake_iter())
    #---------------- Unfinished
    def wake_iter(self):
        """
        Expand this, so that it creates the wrapper objects for each.
        """
        for elm in self.read():
            
            # Assumes elm should be basestring
            
            if is_RecordChunk(elm):
                yield RecordChunk(elm)
            elif is_Dispatcher(elm):
                yield IndexDispatcher(elm)
            elif is_URL(elm):
                yield URLDispatcher(elm)
            else:
                raise TypeError("Unrecognized element type.")
            
        self.data = list(self.read())
    def read(self):
        pass

    def write(self):
        # ? Do I even need this ?
        pass


class DispatcherConfig(object):
    def __init__(self, dirpath):
        pass
    @classmethod
    def from_folder(cls, dirpath):
        pass


#------------------------------------------------------------------------------
#    Classifiers
#------------------------------------------------------------------------------
chunk_extensions = ['.csv']
def is_RecordChunk(value):
    if os.path.exists(value) and os.path.isfile(value):
        _, ext = os.path.splitext(value)
        if ext in chunk_extensions:
            return True
    return False
dispatcher_extensions = ['.json', '.config']
def is_Dispatcher(value):
    if os.path.exists(value) and os.path.isfile(value):
        _, ext = os.path.splitext(value)
        if ext in dispatcher_extensions:
            return True
    return False
def is_URL(value):
    if value.startswith("http://"):
        return True
    return False

