from __future__ import absolute_import
import unittest
import os
import shutil
from endgame.deploy import write_records_csv, read_records, convert_records_csv
from endgame.deploy import write_record_dir
from endgame.interfaces import Record


testdir = os.path.split(__file__)[0]
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)



class DeployRecordsTests(unittest.TestCase):
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

class DeployDispatcherTests(unittest.TestCase):
    def setUp(self):
        self.dirname = 'test_dispatcher'
        self.namestub = 'test_1k'
        self.filecount = 5
        self.recordcount = 1000
        
        self.expected_names = [
            'test_1k_0.csv',
            'test_1k_1.csv',
            'test_1k_2.csv',
            'test_1k_3.csv',
            'test_1k_4.csv'
        ]
        if os.path.exists(self.dirname):
            shutil.rmtree(self.dirname)
    def test_basic(self):
        self.assert_(not os.path.exists(self.dirname))
        write_record_dir(self.dirname, self.namestub, 
            filecount=self.filecount, recordcount=self.recordcount
        )
        
        created = os.listdir(self.dirname) 
        for name in self.expected_names:
            self.assert_(name in created)

if __name__ == "__main__":
    unittest.main()