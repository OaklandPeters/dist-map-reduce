from __future__ import absolute_import
import unittest
import os
from endgame.deploy import write_records_csv, read_records, convert_records_csv
from endgame.interfaces import Record

class DeployTests(unittest.TestCase):
    def setUp(self):
        self.filename = '1k.csv'
        self.count = 1000
        if os.path.exists(self.filename):
            os.remove(self.filename)
    def test_write(self):
        self.assert_(not os.path.exists(self.filename))
        write_records_csv(self.filename, count=self.count)
        self.assert_(os.path.exists(self.filename))
    def test_convert_records(self):
        write_records_csv(self.filename, count=self.count)
        results = list(convert_records_csv(self.filename))
        self.assertEqual(len(results), self.count)
        self.assert_(isinstance(results[0][0], str))
        self.assert_(isinstance(results[0][1], float))
    def test_read_records(self):
        write_records_csv(self.filename, count=self.count)
        results = read_records(self.filename)
        self.assertEqual(len(results), self.count)
        self.assert_(isinstance(results[0], Record))
    def test_100k(self):
        filename = '100k.csv'
        count = 100000
        if os.path.exists(filename):
            os.remove(filename)
        write_records_csv(filename, count=count)
        self.assert_(os.path.exists(filename))
        
if __name__ == "__main__":
    unittest.main()