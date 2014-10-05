from __future__ import absolute_import
import unittest
import sys
import os

from endgame.indexes import RecordChunk
from endgame.interfaces import Record

    
class RecordChunkTests(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.join('endgame', 'test'))
    def test_1k(self):
        chunk = RecordChunk('1k.csv')
        chunk.waken()
        self.assertEqual(
            len(chunk.data),
            1000
        )
        self.assert_(isinstance(chunk.data[0], Record))
        self.assert_(
            isinstance(chunk.data[0][0], str)
        )
        self.assert_(
            isinstance(chunk.data[0].ip, str)
        )

        self.assert_(
            isinstance(chunk.data[0][1], int)
        )
        self.assert_(
            isinstance(chunk.data[0].timestamp, int)
        )

if __name__ == "__main__":
    unittest.main()