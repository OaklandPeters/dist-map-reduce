"""
Provides a REST API to an IndexDispatcher.
"""

from __future__ import absolute_import
import os
import json
from multiprocessing import Process
from flask import Flask, request
from ..interfaces import IndexABC, Query
from .indexdispatcher import IndexDispatcher
from ..extern.clsproperty import VProperty
from werkzeug.routing import BaseConverter

__all__ = ['WebIndex']


class WebIndex(object):
#class WebIndex(IndexABC):
    def __init__(self, index):
        """
        dispatcher: either an IndexDispatcher object, or a valid argument 
            into IndexDisptacher.__init__ - config file path, or data directory path 
        """
        self.index = index
        self.app = self.build_app()
        self.server = None # 'sleeping'
    

    
    def wake_up(self, *args, **kwargs):
        return self.app.run(*args, **kwargs)
    def sleep(self):
        shutdown_webindex()
    def build_app(self):
        app = Flask(self.index.name)
        app.url_map.converters['list'] = ListConverter
        app.url_map.converters['float'] = FloatConverter
        
        
        finder = lambda *args, **kwargs: self.find_response(*args, **kwargs)
        app.route(self.find_rule)(finder)
        #app.route(self.find_rule)(self.find_response)
        app.route(self.sleep_rule)(self.sleep_response)
        return app
        
    @VProperty
    class index(object):
        def _get(self):
            return self._index
        def _set(self, value):
            self._index = value
        def _val(self, value):
            if isinstance(value, IndexDispatcher):
                return value
            elif isinstance(value, basestring):
                return IndexDispatcher(value)
            else:
                raise TypeError("Invalid 'index': should be IndexDispatcher, "
                    "or path to config file or data directory.")
    @property
    def confpath(self):
        return self.index.confpath

    def map(self, query):
        return self.index.map(query)
    def reduce(self, records, query):
        return self.index.reduce(records, query)
    def find(self, query):
        records = self.map(query)
        return self.reduce(records, query)
    #--------------------------------------------------------------
    #    REST API
    #--------------------------------------------------------------
    find_rule = '/find/<list:ips>/<float:start>/<float:end>/'
    #@staticmethod
    #def find_response(ips, start, end):
    def find_response(self, ips, start, end):
        query = Query(ips, (start, end))
        found = self.index.find(query)
        return str(found)
        
        msg = "query {klass}: {value}".format(
            klass = type(query).__name__, value = query
        )
        return msg
    sleep_rule = '/sleep'
    @staticmethod
    def sleep_response():
        shutdown_webindex()
        return "Shutting down WebIndex"
    
    def process_up(self):
        p = Process(target=startup_webindex, args=(self.confpath,))
        p.start()
        #p.join()
        return p
        
        

    #Alternate shutdown - using multiprocessing
    #from multiprocessing import Process
#     def process_up(self):
#         self.server = Process(target=self.app.run)
#         self.server.start
#     def process_down(self):
#         self.server.terminate()
#         self.server.join()

def startup_webindex(confpath):
    index = IndexDispatcher(confpath)
    web = WebIndex(index)
    web.wake_up()
    

def shutdown_webindex():
    down = request.environ.get('werkzeug.server.shutdown')
    if down is None:
        raise RuntimeError('Not using werkzeug. Why?')
    down()

#--------------------------------------------------------------------------
#    Local Utility
#--------------------------------------------------------------------------
class ListConverter(BaseConverter):
    def to_python(self, value):
        return str(value).strip('[]').split(',')
    def to_url(self, values):
        return "[{0}]".format(
            ','.join(BaseConverter.to_url(value) for value in values) #pylint: disable=no-value-for-parameter
        ) 

class FloatConverter(BaseConverter):
    def to_python(self, value):
        return float(value)
    def to_url(self, value):
        return str(value)