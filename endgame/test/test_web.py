"""
Unit-tests for the Flask mini-server / REST API portions.
This may have to integrate closely with:  endgame.indexes.urldispatcher

@todo: Add to FlaskTests: Boot up webserver
"""

from __future__ import absolute_import
import os
import unittest
from flask import Flask
from endgame.indexes import URLDispatcher
from endgame.interfaces import Query, Record

import endgame.test.stable_query as stable_query

# Center on data directory
testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)

# (1) How to launch a process for the server,
# (2) Continue in current process
# (3) And later stop the process?


class FlaskTests(unittest.TestCase):
    def setUp(self):
        self.configpath = os.path.join(datadir, 'stable_metaindex.json')
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
        
        # [] boot up web-server
    def test_find(self):
        #urldisp = URLDispatcher(self.configpath)
        #urldisp.find(query)
        pass
