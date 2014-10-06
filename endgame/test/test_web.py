"""
Unit-tests for the Flask mini-server / REST API portions.
This may have to integrate closely with:  endgame.indexes.urldispatcher
"""

from __future__ import absolute_import
import os
import unittest
from flask import Flask
from endgame.indexes import IndexDispatcher, directory_to_config, RecordChunk
from endgame.interfaces import Query, Record

# Center on data directory
testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)

# (1) How to launch a process for the server,
# (2) Continue in current process
# (3) And later stop the process?


class FlaskTest(unittest.TestCase):
    def setUp(self):
        pass

