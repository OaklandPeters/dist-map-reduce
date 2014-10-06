from __future__ import absolute_import
import unittest
import os

from endgame.indexes import IndexDispatcher, directory_to_config, RecordChunk
from endgame.interfaces import Query, Record
import endgame.test.sample_query as stable_query

testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)



class IndexDispatcherTests(unittest.TestCase):
    """
    Note that the target_record naturally occurs in stable_1k_2.csv
    I have also injected it into the end of stable_1k_0.csv
    """
    def setUp(self):
        self.dirpath = 'stable_dispatcher'
        self.config_path = 'stable_dispatcher.json'
        if not os.path.exists(self.dirpath):
            raise RuntimeError("Necessary test data directory does not exist.")
        
        #import endgame.test.stable_query as stable_query
        self.target_entry = stable_query.target_entry
        self.target_record = stable_query.target_record
        self.query = stable_query.query
#         self.target_entry = ('34.53.12.162', 1412534621.53)
#         self.target_record = Record(*self.target_entry)
#         self.query = Query(
#             '34.53.12.162',
#             (1412534621.529, 1412534621.531)
#         )
        
    def test_directory_to_config(self):
        config_path = directory_to_config(self.dirpath)
        self.assert_(os.path.exists(config_path))
    def test_config_constructor(self):
        config_path = directory_to_config(self.dirpath)
        disp = IndexDispatcher(config_path)
        disp.wake_up()
        self.assertEqual(len(disp.data), 5)
        self.assert_(isinstance(disp.data[0], RecordChunk))

    def test_dir_constructor(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        disp = IndexDispatcher(self.dirpath)
        disp.wake_up()
        self.assert_(os.path.exists(self.config_path))
        self.assertEqual(len(disp.data), 5)
        self.assert_(isinstance(disp.data[0], RecordChunk))

    def test_find(self):
        dispatcher = IndexDispatcher(self.dirpath)
        results = dispatcher.find(self.query)

        self.assert_(self.target_record in results)
        self.assert_(len(results) >= 2)


if __name__ == "__main__":
    unittest.main()