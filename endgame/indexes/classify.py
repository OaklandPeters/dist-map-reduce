from __future__ import absolute_import

def classify_index(instring, *index_types):
    """classify_index(basestring: instring) --> IndexABC subclass

    Based on instring, return a appropriate IndexABC subclass - one
    descendant of IndexABC (RecordChunk or IndexDispatcher or URLDispatcher).
    'instring' is usually read from IndexDispatcher's config file
    
    classify_index(elm, RecordChunk, IndexDispatcher, URLDispatcher
    """
    # imports 'in-function' are generally a bad practice
    # ... however, I do not see how else to access them
    from .recordchunk import RecordChunk
    from .indexdispatcher import IndexDispatcher
    from .urldispatcher import URLDispatcher
    
    if RecordChunk.valid(instring):
        return RecordChunk
    elif IndexDispatcher.valid(instring):
        return IndexDispatcher
    elif URLDispatcher.valid(instring):
        return URLDispatcher
    else:
        raise TypeError("Unrecognized index type for "+str(instring))
