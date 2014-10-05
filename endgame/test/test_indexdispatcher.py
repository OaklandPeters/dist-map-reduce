from __future__ import absolute_import
import unittest
import os

from endgame.indexes import IndexDispatcher, directory_to_config, RecordChunk

class IndexDispatcherTests(unittest.TestCase):
    def setUp(self):
        self.dirpath = 'stable_dispatcher'
        self.config_path = 'stable_dispatcher.json'
        
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

if __name__ == "__main__":
    unittest.main()