from __future__ import absolute_import
import unittest
import os

from endgame.indexes import IndexDispatcher
import endgame.test.sample_query as stable_query

testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)



class MetaIndexTests(unittest.TestCase):
    def setUp(self):
        self.meta_path = 'stable_metaindex.json'
        #stable_1k_2.csv, row #50
        #also added to stable_dispatcher2/stable_1k_5.csv row #1001
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
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
        
        self.assert_(len(results) >= 3)
        for record in results:
            self.assert_(record in self.query)

class MetaMetaTests(unittest.TestCase):
    def setUp(self):
        self.meta_path = 'stable_metaindex.json'
        self.meta2_path = 'stable_metaindex2.json'
        #stable_1k_2.csv, row #50
        #also added to stable_dispatcher2/stable_1k_5.csv row #1001
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
    def test_find(self):
        meta2 = IndexDispatcher(self.meta2_path)
        meta2.wake_up()
        results = meta2.find(self.query)

        self.assert_(len(results) >= 4)
        for record in results:
            self.assert_(record in self.query)
        
        
if __name__ == "__main__":
    unittest.main()