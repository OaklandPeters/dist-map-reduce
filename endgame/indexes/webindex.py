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


#class WebIndex(object):
class WebIndex(IndexABC):
    def __init__(self, index, baseurl=None):
        """
        dispatcher: either an IndexDispatcher object, or a valid argument 
            into IndexDisptacher.__init__ - config file path, or data directory path 
        """
        self.index = index
        self.app = self.build_app()
        self.server = None # 'sleeping'
        self.process = None
        self.baseurl = baseurl



    
    @property
    def awake(self):
        return self.app
        #INVALID
    

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
        if 'port' not in kwargs:
            kwargs['port'] = self.port
        ret = self.app.run(*args, **kwargs)
        print(ret)
        return ret
    
        return self.app.run(*args, **kwargs)
    def process_up(self, *args, **kwargs):
        self.process = Process(
            target=startup_webindex,
            args=(self.configpath,)+args,
            kwargs=kwargs
        )
        
        self.process.start()
        #p.join()
        return self.process
    def process_down(self):
        """I heavily doubt this works correctly.
        Consider it a placeholder."""
        if hasattr(self.process, 'terminate'):
            #self.process.join()
            self.process.terminate()
    
    def sleep(self, datano=None):
        if datano is None:
            self._sleep_all()
        elif isinstance(datano, int):
            self._sleep_datano(datano)
    def _sleep_all(self):
        """Put index (and its data) to sleep - and then shutdown webserver."""
        # Note: index.sleep should already recursively put it's data to sleep
        #for elm in self.index.data:
        #    elm.sleep()
        self.index.sleep()
            
        try:
            shutdown_webindex()
            return "Shutting down WebIndex '{0}'".format(self.name)
        except WebSleepError:
            return "WebIndex '{0}' appears to be already shutdown."
    def _sleep_datano(self, datano):
        """Put single data connection to sleep."""
        self.index.data[datano].sleep()
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sleep()
        self.process_down()

    def build_app(self):
        """Build app. Put url-map type converters in place, and then setup
        REST API."""
        app = Flask(self.index.name)
        app.url_map.converters['list'] = ListConverter
        app.url_map.converters['float'] = FloatConverter
        
        def finder(*args, **kwargs):
            return self.find_response(*args, **kwargs)
        def sleeper(*args, **kwargs):
            return self.sleep_response(*args, **kwargs)
        
        app.route(self.find_rule)(finder)
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
    @VProperty
    class baseurl(object):
        def _get(self):
            if not hasattr(self, '_baseurl'):
                self._baseurl = 'http://127.0.0.1'
            return self._baseurl
        def _set(self, value):
            self._baseurl = value
        def _val(self, value):
            if value is None:
                return 'http://127.0.0.1'
            if not isinstance(value, basestring):
                raise TypeError("'baseurl' must be a basestring.")
            return value
    
    @property
    def name(self):
        return self.index.name
    @property
    def port(self):
        return self.index.config['port']
    @property
    def configpath(self):
        return self.index.configpath
    # Validation
    @classmethod
    def valid(cls, instring):
        """Asks if instring is a valid WebIndex. Defers to IndexDispatcher.valid"""
        return IndexDispatcher.valid(instring)
    _baseurl = 'http://'
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
    def sleep_response(self, datano=None):
        self.sleep(datano=datano)
    #def sleep_response(self):
    #    shutdown_webindex()
    
    static_sleep_rule = '/sleep'
    @staticmethod
    def static_sleep_response():
        shutdown_webindex()

    
        
        





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