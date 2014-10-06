from __future__ import absolute_import
import os
import abc
from .shared import dirpath_to_confpath

__all__ = [
    'IndexValidatorABC',
    'IndexDispatcherValidator',
    'URLDispatcherValidator'
]


class IndexValidatorABC(object):
    __metaclass__ = abc.ABCMeta
    valid = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)


class IndexDispatcherValidator(IndexValidatorABC):
    """Validation functions for IndexDispatcher.
    Intended to be inherited."""
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


class URLDispatcherValidator(IndexValidatorABC):
    """Validation functions for URLDispatcher.
    Intended to be inherited."""
    @classmethod
    def _validate_url(cls, url):
        """
        @todo: Expand this.
        """
        if not isinstance(url, basestring):
            raise TypeError("'url' must be a basestring.")
        else: # string
            if url.startswith("http://"):
                return url
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
    
class RecordChunkValidator(IndexValidatorABC):
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
    


#------------------------------------------------------------------------------
#    Function to Dispatch on instrings from config files
#------------------------------------------------------------------------------
# def classify_index(instring, *index_types):
#     """classify_index(basestring: instring) --> IndexABC subclass
# 
#     Based on instring, return a appropriate IndexABC subclass - one
#     descendant of IndexABC (RecordChunk or IndexDispatcher or URLDispatcher).
#     'instring' is usually read from IndexDispatcher's config file
#     
#     classify_index(elm, RecordChunk, IndexDispatcher, URLDispatcher
#     """
#     for index in index_types:
#         if index.valid(instring):
#             return index
#     raise TypeError("Unrecognized index type for "+str(instring))
#     
#     if RecordChunk.valid(instring):
#         return RecordChunk
#     elif IndexDispatcher.valid(instring):
#         return IndexDispatcher
#     elif URLDispatcher.valid(instring):
#         return URLDispatcher
#     else:
#         raise TypeError("Unrecognized index type for "+str(instring))
