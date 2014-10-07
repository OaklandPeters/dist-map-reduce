from __future__ import absolute_import
import os
import json
import collections
from ..interfaces import IndexABC
#from .recordchunk import RecordChunk
#from .urldispatcher import URLDispatcher
from ..extern.clsproperty import VProperty
from .shared import (dirpath_to_confpath, confpath_to_dirpath, 
    directory_to_config, flatten, is_nonstringsequence)
from .classify import classify_index


__all__ = ['IndexDispatcher']


class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, filepath, port=None):
        self.configpath = self._validate_confpath(filepath)
        self.dirpath = confpath_to_dirpath(self.configpath)
        
        if not os.path.exists(self.configpath):
            self.write(self.dirpath, port=self.port)
        self.config = self.read_config()
        
        
        # If port is provided - use it (whether config['port'] exists or not)
#         if port is not None:
#             self.config['port'] = port    
#         else: # Default - 
#             if 'port' not in self.config:
#                 self.config['port'] = 5000

            
            
        self.data = None # 'sleeping'

    @VProperty
    class port(object):
        """Port number for this, if used as a webindex."""
        def _get(self):
            if 'port' not in self.config: #pylint: disable=no-member
                self.config['port'] = 5000 #pylint: disable=no-member
            return self.config['port'] #pylint: disable=no-member
        def _set(self, value):
            self.config['port'] = value #pylint: disable=no-member
        def _val(self, value):
            if not isinstance(value, int):
                try:
                    value = int(value)
                except ValueError:
                    raise TypeError(str.format(
                        "'port' must be integer, or string convertible to "
                        + "an integer. Not {0}.",
                        type(value).__name__
                    ))
            return value
            

    #--------------------------------------------------------------------------
    #    Map/Reduce
    #--------------------------------------------------------------------------
    def map(self, query):
        """Load data for this instance, and recurse .find() command to that data."""
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

    #--------------------------------------------------------------------------
    #    Dispatching
    #--------------------------------------------------------------------------
    dispatcher_extensions = ['.json', '.config']
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
    @classmethod
    def valid(cls, filepath):
        return cls.valid_confpath(filepath)

    
    #--------------------------------------------------------------------------
    #    File Interaction
    #--------------------------------------------------------------------------
    def read(self):
        """Read configuration file, and return iterator over it's data."""
        for elm in self.config['data']:
            if is_nonstringsequence(elm):
                yield os.path.join(*elm)
            elif isinstance(elm, basestring):
                yield elm
            else:
                raise RuntimeError("Logic error.")
    @classmethod
    def write(cls, dirpath, **keywords):
        """Create configuration file, based on a directory."""
        return directory_to_config(dirpath, **keywords)
    def read_config(self):
        with open(self.configpath, 'r') as config_file: #pylint: disable=no-member
            return json.load(config_file) #pylint: disable=attribute-defined-outside-init
    def write_config(self):
        with open(self.configpath, 'w') as config_file:
            json.dump(self.config, config_file)
    # ----------------------------   Wake/Sleep Interface
    @property
    def awake(self):
        if self.data is None:
            return False
        else:
            return True
    def sleep(self):
        """Recursively remove data."""
        if self.awake:
            for index in self.data:
                index.sleep()
        self.data = None
    def wake_up(self):
        self.data = list(self.wake_iter())

    def wake_iter(self):
        """
        Expand this, so that it creates the wrapper objects for each.
        Assumes each element from self.read() is a basestring.
        """
        for elm in self.read():
            index = classify_index(elm) # Find index type
            yield index(elm) # Instantiate and return type

    #--------------------------------------------------------------------------
    #    Properties
    #--------------------------------------------------------------------------
    @property
    def name(self):
        _, confname = os.path.split(self.configpath)
        name, _ = os.path.splitext(confname)
        return name
    @VProperty
    class config(object):
        """Contents of configuration file. Immutable."""
        def _get(self): #cache contents of config file
            if not hasattr(self, '_config'):
                with open(self.configpath, 'r') as config_file: #pylint: disable=no-member
                    self._config = json.load(config_file) #pylint: disable=attribute-defined-outside-init
            return self._config
        def _set(self, value):
            self._config = value
        def _del(self):
            del self._config

    @property
    def port(self):
        return self.config.get('port', 5000) #pylint: disable=no-member
    
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
            #... limit length displayed
            data = [str(elm)[:20] for elm in self.data]
        )
    def __repr__(self):
        return "{name}({data})".format(
            name = type(self).__name__,
            #... limit length displayed
            data = [repr(elm)[:20] for elm in self.data]
        )

