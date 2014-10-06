from __future__ import absolute_import
import unittest
import os

from endgame.indexes import RecordChunk
from endgame.interfaces import Record, Query
from endgame.deploy import IPv4

rootdir = os.getcwd()
testdir = os.path.join(rootdir, 'endgame', 'test')

class RecordChunkTests(unittest.TestCase):
    def setUp(self):
        os.chdir(testdir)
        self.filename = 'stable_1k.csv'
        self.count = 1000
        #stable_1k_2.csv, row #50
        self.target_entry = ('34.53.12.162', 1412534621.53)
        self.target_record = Record(*self.target_entry)
        self.query = Query(
            '34.53.12.162',
            (1412534621.529, 1412534621.531)
        )
    def test_waken(self):
        chunk = RecordChunk(self.filename)
        chunk.wake_up()
        self.assertEqual(
            len(chunk.data),
            self.count
        )
        self.assert_(isinstance(chunk.data[0], Record))
        self.assert_(
            isinstance(chunk.data[0][0], str)
        )
        self.assert_(
            isinstance(chunk.data[0].ip, str)
        )

        self.assert_(
            isinstance(chunk.data[0][1], float)
        )
        self.assert_(
            isinstance(chunk.data[0].timestamp, float)
        )
    def test_find(self):
        chunk = RecordChunk(self.filename)
        chunk.wake_up()
        
        found = chunk.find(self.query)
        self.assert_(self.target_record in found)
        
        
        

if __name__ == "__main__":
    unittest.main()