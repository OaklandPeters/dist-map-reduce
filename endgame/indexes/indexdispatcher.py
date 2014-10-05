from __future__ import absolute_import
import os
import json
from ..interfaces import IndexABC
from .recordchunk import RecordChunk
from .urldispatcher import URLDispatcher

__all__ = ['IndexDispatcher', 'directory_to_config']

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, filepath):
        # Config file, or directory
        if os.path.isdir(filepath):
            filepath = directory_to_config(filepath)
        self.filepath = filepath
        self.data = None # 'sleeping'
    def map(self, query):
        self.wake_up()
        return [
            elm.find(query)
            for elm in self.data
        ]
    def reduce(self, records, query):
        """Does this need to do an filtering?"""
        return sorted(records, key=lambda record: record.timestamp)

    
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
        with open(self.filepath, 'r') as config_file:
            config = json.load(config_file)
        return iter(config['data'])

    def write(self):
        # ? Do I even need this ?
        pass



def directory_to_config(dirpath):
    """Create a configuration file for dirpath, and return it's filepath.
    Place the configuration file on level with the directory. IE:
    parent/
        {dirpath}/
        {dirpath}.json
        
    """
    if not os.path.isdir(dirpath):
        raise ValueError("{0} is not an existing directory.".format(dirpath))
    # Write config_path: remove trailing seperator
    if dirpath[-1] == os.sep:
        config_path = dirpath[:-1] + ".json"
    else:
        config_path = dirpath + ".json"
    #Get all csv files
    record_files = [os.path.join(dirpath, filepath)
        for filepath in os.listdir(dirpath)
        if filepath.endswith('.csv')
    ]
    # Write JSON config file
    with open(config_path, 'w') as config_file:
        json.dump({'data': record_files}, config_file)
    return config_path
    
    


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

