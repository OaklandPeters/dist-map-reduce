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
        self.assert_(not meta.awake)
        meta.wake_up()
        self.assert_(meta.awake)
        self.assertEqual(len(meta.data), 2)
        for elm in meta.data:
            self.assert_(isinstance(elm, IndexDispatcher))
            self.assert_(not elm.awake)
         
    def test_find(self):
        meta = IndexDispatcher(self.meta_path)
        meta.wake_up()
        results = meta.find(self.query)
        
        self.assertGreaterEqual(len(results), 3)
        for record in results:
            self.assert_(record in self.query)


if __name__ == "__main__":
    unittest.main()