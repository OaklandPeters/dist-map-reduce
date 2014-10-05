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
        self.file_time_range = [1412525393.52, 1412625293.615]
        self.target_entry = ('210.173.97.67', 1412536793.528)
        self.target_record = Record(*self.target_entry)
        #entry #114, line # 229
        # ('21.188.253.146', 1412536693.528)
        self.query = Query(
            '210.173.97.67',
            (1412536793.527, 1412536793.531)
        )
    def test_waken(self):
        chunk = RecordChunk(self.filename)
        chunk.waken()
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
        chunk.waken()
        
        found = chunk.find(self.query)
        self.assert_(Record('210.173.97.67', 1412536793.528) in found)
        self.assert_(self.target_record in found)
        
        

if __name__ == "__main__":
    unittest.main()