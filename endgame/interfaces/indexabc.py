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
    live = abc.abstractproperty()
    state = abc.abstractproperty()
    waken = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
    
    #data = abc.abstractproperty() # list of entries: IndexDispatcher or RecordChunk    

    def find(self, query):
        """The recursion step. Combines map + reduce

        For now, assume accepts only 1 argument: query
        Todo: allow to accept either:
            find(ip_list, timerange)
                --> query = Query(ip_list, timerange)
                    return self.find(query)
            find(query)
        """
        # Map
        # found = map(finder(query), self.data)
        found = self.map(query)
        
        # Reduce
        # This step should be changed for RecordChunk indexes 
        # ... filter
        reduced = self.reduce(found, query) 
        
        return reduced
