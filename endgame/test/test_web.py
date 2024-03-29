"""
Unit-tests for the Flask mini-server / REST API portions.
This may have to integrate closely with:  endgame.indexes.urldispatcher

@todo: Add to FlaskTests: Boot up webserver
"""

from __future__ import absolute_import
import os
import unittest
from flask import Flask
from multiprocessing import Process
from endgame.indexes import URLDispatcher, WebIndex, IndexDispatcher
from endgame.interfaces import Query, Record
import endgame.test.stable_query as stable_query

# Center on data directory
testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)

# (1) How to launch a process for the server,
# (2) Continue in current process
# (3) And later stop the process?


def launch(configpath):
    index = IndexDispatcher(configpath)
    web = WebIndex(index)
    web.wake_up(debug=True)


class WebIndexTests(unittest.TestCase):
    def setUp(self):
        self.metapath = os.path.join(datadir, 'stable_metaindex.json')
        self.metapath2 = os.path.join(datadir, 'stable_metaindex2.json')
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
        self.baseurl = 'http://127.0.0.1'
        self.port = 5005
        self.fullurl = self.baseurl+":"+str(self.port)+"/"
        # Example url:
        # http://127.0.0.1:5000/find/[3.42.225.161]/1412619807.79/1412619808.59/
        
    
    def unusued_test_basic(self):
        index = IndexDispatcher(self.metapath)
        web = WebIndex(index)
  
        web.wake_up(debug=True)
        
    def test_multiprocess(self):
        index = IndexDispatcher(self.metapath)
        
        with WebIndex(index) as web:
            web.process_up()
            results = web.find(self.query)
            
        #web = WebIndex(index)
        #web.process_up()
        #results = web.find(self.query)
        #web.sleep()
        
        self.assert_(len(results) >= 3)
        self.assert_(self.target_record in results)

    def test_from_urldispatcher(self):
        index = IndexDispatcher(self.metapath)
        
        with WebIndex(index) as web:
            web.process_up()
            
            urldisp = URLDispatcher.from_url_parts(self.baseurl, self.port)
            results = urldisp.find(self.query)
            
#             with URLDispatcher.from_url_parts(self.baseurl, self.port) as urldisp:
#                 results = urldisp.find(self.query)
        
        self.assert_(len(results) >= 3)
        self.assert_(self.target_record in results)
    
    def test_urldispatcher_to_urldispatcher(self):
        index1 = IndexDispatcher(self.metapath)
        index2 = IndexDispatcher(self.metapath2)
        
        # Web-server/REST API #1
        with WebIndex(index1) as web1:
            web1.process_up()
            
            # Web-server/REST API #2
            with WebIndex(index2) as web2:
                web2.process_up()
                
                web2.index.wake_up()
                for i, elm in enumerate(web2.index.data):
                    results = elm.find(self.query)
                    if i == 0:
                        self.assert_(len(results) >= 1)
                        self.assert_(isinstance(elm, IndexDispatcher))
                    elif i == 1:
                        self.assert_(len(results) >= 0)
                        self.assert_(isinstance(elm, IndexDispatcher))
                    elif i == 2:
                        self.assert_(len(results) >= 3)
                        self.assert_(isinstance(elm, URLDispatcher))
                    print(i, type(elm).__name__, elm.find(self.query))



if __name__ == "__main__":
    unittest.main()