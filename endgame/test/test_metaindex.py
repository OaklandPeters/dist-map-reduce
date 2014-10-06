from __future__ import absolute_import
import unittest
import os

from endgame.indexes import IndexDispatcher, directory_to_config, RecordChunk
from endgame.interfaces import Query, Record


class MetaIndexTests(unittest.TestCase):
    def setUp(self):
        self.meta_path = 'stable_metaindex.json'
        #stable_1k_2.csv, row #50
        #also added to stable_dispatcher2/stable_1k_5.csv row #1001
        self.target_entry = ('34.53.12.162', 1412534621.53)
        self.target_record = Record(*self.target_entry)
        self.query = Query(
            '34.53.12.162',
            (1412534621.529, 1412534621.531)
        )
    def test_open(self):
        meta = IndexDispatcher(self.meta_path)
        self.assert_(isinstance(meta, IndexDispatcher))
        meta.wake_up()
        
        print()
        print()
        
    def test_find(self):
        meta = IndexDispatcher(self.meta_path)
        meta.wake_up()
        results = meta.find(self.query)
        print(len(results))
        print()

if __name__ == "__main__":
    unittest.main()