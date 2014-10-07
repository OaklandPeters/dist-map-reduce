"""
Provides a REST API to an IndexDispatcher.
"""

from __future__ import absolute_import
import os
import json
from ..interfaces import IndexABC
from .indexdispatcher import IndexDispatcher


#Need something that maps a request + function --> query + function --> function(query)

def get_query(request):

def app_from_dispatcher(dispatcher):
    
    if not isinstance(dispatcher, IndexDispatcher):
        raise TypeError("'dispatcher' must be an IndexDispatcher.")

    app = Flask(dispatcher.name)

    app.route(urlpath)(responding_function)


# class WebIndex(IndexABC):    
#     map = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
#     reduce = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
#     
#     # Wake/Sleep Interface
#     awake = abc.abstractproperty()
#     wake_up = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
#     sleep = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)
#     
#     # Identifies valid input for constructor
#     #     Used to 'dispatch' to the appropriate type:
#     #        IndexDispatcher, RecordChunk, or URLDispatcher
#     valid = abc.abstractmethod(lambda *args, **kwargs: NotImplemented)