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
    wake_up = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    
    # Identifies valid input for constructor
    #     Used to 'dispatch' to the appropriate type:
    #        IndexDispatcher, RecordChunk, or URLDispatcher
    valid = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    #==========================================================================
    #    Mixin Methods
    #==========================================================================
    def find(self, query):
        """The recursion step. Combines map + reduce
        Single argument should be a Query object.
        """
        found = self.map(query)
        reduced = self.reduce(found, query)
        return reduced
    def __enter__(self):
        #self.wake_up() - actually should NOT always wake_up
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sleep()
        
        
    