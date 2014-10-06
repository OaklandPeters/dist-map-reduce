from __future__ import absolute_import
import os
import json
import itertools
from ..interfaces import IndexABC
from .recordchunk import RecordChunk
from .urldispatcher import URLDispatcher

__all__ = ['IndexDispatcher', 'directory_to_config']

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, filepath):
        self.confpath = self._validate_confpath(filepath)
        self.dirpath = confpath_to_dirpath(self.confpath)
        if not os.path.exists(self.confpath):
            self.write(self.dirpath)
        self.data = None # 'sleeping'
    
    
    
    #--------------------------------------------------------------------------
    #    File Interaction
    #--------------------------------------------------------------------------
    dispatcher_extensions = ['.json', '.config']
    def read(self):
        """Read configuration file, and return iterator over it's data."""
        with open(self.confpath, 'r') as config_file:
            config = json.load(config_file)
        return iter(config['data'])
    @classmethod
    def write(cls, dirpath):
        """Create configuration file, based on a directory."""
        return directory_to_config(dirpath)
    
    @classmethod
    def _validate_confpath(cls, filepath):
        """filepath: path of directory, or path of config file
        returns path of config file
        """
        if os.path.isdir(filepath): #if directory
            return dirpath_to_confpath(filepath)
        elif os.path.isfile(filepath): #is file
            #is it config file?
            fname, fext = os.path.splitext(filepath)
            if fext in cls.dispatcher_extensions:
                return filepath
            else:
                raise ValueError(str.format(
                    "Invalid 'filepath' extension '{0}'. Should be '{1}'",
                    fext, ", ".join(cls.dispatcher_extensions)
                ))
        else:
            raise ValueError(str.format(
                "'filepath' of type '{0}' is neither a config or directory: {1}",
                type(filepath).__name__, filepath
            ))
    @classmethod
    def valid_confpath(cls, filepath):
        try:
            cls._validate_confpath(filepath)
        except (ValueError):
            return False
        else:
            return True
    

    
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
    # Wake/Sleep Interface
    @property
    def awake(self):
        if self.data is None:
            return False
        else:
            return True
    @property
    def state(self):
        return self.awake
    def sleep(self):
        self.data = None
    def wake_up(self):
        self.data = list(self.wake_iter())

    def wake_iter(self):
        """
        Expand this, so that it creates the wrapper objects for each.
        Assumes each element from self.read() is a basestring.
        """
        for elm in self.read():
            if is_RecordChunk(elm):
                yield RecordChunk(elm)
            elif is_Dispatcher(elm):
                yield IndexDispatcher(elm)
            elif is_URL(elm):
                yield URLDispatcher(elm)
            else:
                raise TypeError("Unrecognized element type.")


    #--------------------------------------------------------------------------
    #    Magic Methods
    #--------------------------------------------------------------------------
    # ? Provide __iter__ - and connect to wake_up?
#     def __iter__(self):
#         if not self.awake:
#             self.wake_up()
#         return iter(self.data)
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


def dirpath_to_confpath(dirpath):
    if dirpath[-1] == os.sep:
        confpath = dirpath[:-1] + ".json"
    else:
        confpath = dirpath + ".json"
    return confpath

def confpath_to_dirpath(confpath):
    cname, cext = os.path.splitext(confpath)
    return cname

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
    confpath = dirpath_to_confpath(dirpath)
    #Get all csv files
    record_files = [os.path.join(dirpath, filepath)
        for filepath in os.listdir(dirpath)
        if filepath.endswith('.csv')
    ]
    # Write JSON config file
    with open(confpath, 'w') as config_file:
        json.dump({'data': record_files}, config_file)
    return confpath
    
    


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
    return IndexDispatcher.valid_filepath(value)
#     if os.path.exists(value) and os.path.isfile(value):
#         _, ext = os.path.splitext(value)
#         if ext in dispatcher_extensions:
#             return True
#     return False
def is_URL(value):
    if value.startswith("http://"):
        return True
    return False


#------------------------------------------------------------------------------
#    Local Utility Functions
#------------------------------------------------------------------------------
def flatten(seq_of_seq):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(seq_of_seq)
