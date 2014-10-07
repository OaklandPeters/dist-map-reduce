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
        self.process = None

    #--------------------------------------------------------------------------
    #    Map/Reduce
    #--------------------------------------------------------------------------
    def map(self, query):
        return self.index.map(query)
    def reduce(self, records, query):
        return self.index.reduce(records, query)
    def find(self, query):
        records = self.map(query)
        return self.reduce(records, query)    

    #--------------------------------------------------------------------------
    #    App Up/Down
    #--------------------------------------------------------------------------
    def wake_up(self, *args, **kwargs):
        ret = self.app.run(*args, **kwargs)
        print(ret)
        return ret
    
        return self.app.run(*args, **kwargs)
    
    
    def sleep(self, datano=None):
        if datano is None:
            for elm in self.index.data:
                elm.sleep()
        self.index.sleep()
        try:
            shutdown_webindex()
            return "Shutting down WebIndex '{0}'".format(self.name)
        except WebSleepError:
            return "WebIndex '{0}' appears to be already shutdown."

    def build_app(self):
        app = Flask(self.index.name)
        app.url_map.converters['list'] = ListConverter
        app.url_map.converters['float'] = FloatConverter
        
        def finder(*args, **kwargs):
            return self.find_response(*args, **kwargs)
        def sleeper(*args, **kwargs):
            return self.sleep_response(*args, **kwargs)
        #finder = lambda *args, **kwargs: self.find_response(*args, **kwargs)
        #sleeper = lambda *args, **kwargs: self.sleep_response(*args, **kwargs)
        
        app.route(self.find_rule)(finder)
        #app.route(self.static_sleep_rule)(self.static_sleep_response)
        app.route(self.sleep_rule)(sleeper)
        
        return app
    
    #--------------------------------------------------------------------------
    #    Properties
    #--------------------------------------------------------------------------
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
    def name(self):
        return self.index.name
    @property
    def port(self):
        return self.index.config['port']
    @property
    def configpath(self):
        return self.index.configpath


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
        
    
    sleep_rule = '/sleep/<int:datano>/'
    #def sleep_response(self, datano=None):
    #    self.sleep()
    def sleep_response(self):
        shutdown_webindex()
    
    static_sleep_rule = '/sleep'
    @staticmethod
    def static_sleep_response():
        shutdown_webindex()

    def process_up(self, *args, **kwargs):
        self.process = Process(
            target=startup_webindex,
            args=(self.configpath,)+args,
            kwargs=kwargs
        )
        
        self.process.start()
        #p.join()
        return self.process
        
        





#--------------------------------------------------------------------------
#    Local Utility
#--------------------------------------------------------------------------
class WebSleepError(RuntimeError):
    pass

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

def startup_webindex(confpath, *args, **kwargs):
    """Startup a webindex corresponding to a configuration file path.
    Necessary as a top-level function to allow multiprocessing to work.
    """
    index = IndexDispatcher(confpath)
    web = WebIndex(index)
    return web.wake_up(*args, **kwargs)
    
    

def shutdown_webindex():
    try:
        down = request.environ.get('werkzeug.server.shutdown')
    except RuntimeError as exc: #recast as more specific exception
        raise WebSleepError("Cannot sleep. "+str(exc))
    
    if down is None:
        raise RuntimeError('Not using werkzeug. Why?')
    down()