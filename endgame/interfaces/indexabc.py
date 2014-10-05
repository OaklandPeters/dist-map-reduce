from __future__ import absolute_import
import abc

class IndexABC(object):
    """
    @todo: Give MutableSequence behavior, based on data. Inherit from BasicMutableSequence
    
    
    map should return iterable
    """
    __metaclass__ = abc.ABCMeta
    # Map/Reduce Interface
    map = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    reduce = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    
    # Wake/Sleep Interface
    awake = abc.abstractproperty()
    state = abc.abstractproperty()
    wake_up = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
        
    #==========================================================================
    #    Mixin Methods
    #==========================================================================
    def find(self, query):
        """The recursion step. Combines map + reduce
        Single argument should be a Query object.
        """
        # Map
        # found = map(finder(query), self.data)
        found = self.map(query)
        
        # Reduce
        # This step should be changed for RecordChunk indexes 
        # ... filter
        reduced = self.reduce(found, query) 
        
        return reduced
