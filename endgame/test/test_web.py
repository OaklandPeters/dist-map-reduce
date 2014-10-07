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
        self.configpath = os.path.join(datadir, 'stable_metaindex.json')
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
        self.baseurl = 'http://127.0.0.1:5000/'
        # Example url:
        # http://127.0.0.1:5000/find/[3.42.225.161]/1412619807.79/1412619808.59/
#     def test_basic(self):
#         index = IndexDispatcher(self.configpath)
#         web = WebIndex(index)
# 
#         web.wake_up(debug=True)
    def test_multiprocess(self):
        index = IndexDispatcher(self.configpath)
        web = WebIndex(index)
        web.process_up()
        
        results = web.find(self.query)
        web.sleep()
        
        self.assert_(len(results) >= 3)
        self.assert_(self.target_record in results)

    def test_from_urldispatcher(self):
        index = IndexDispatcher(self.configpath)
        web = WebIndex(index)
        web.process_up()
        urldisp = URLDispatcher(self.baseurl)
        urldisp.find(self.query)
        
        print()
        #Setup URLDispatcher, pointing to the webindex
        #Send the call
        #Receive it, and decode from string



if __name__ == "__main__":
    unittest.main()