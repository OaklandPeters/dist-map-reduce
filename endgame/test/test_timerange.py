from __future__ import absolute_import
import unittest
import datetime

from endgame.time import TimeRange, datetime_to_timestamp, timestamp_to_datetime

class TimeRangeTests(unittest.TestCase):
    def setUp(self):
        
        self.now = datetime.datetime.now()
        self.now_ts = datetime_to_timestamp(self.now)
        self.delta = datetime.timedelta(seconds=60)
        self.then = self.now + self.delta
        self.then_ts = datetime_to_timestamp(self.then)
        self.second = 1000
        self.minute = 60 * self.second
        
        self.inside = self.now_ts + self.second * 10
        self.outside = self.now_ts + self.minute * 10

#     def gamut(self, start, end):
#         tr = TimeRange(start, end)
#         print(start, end)
#         print(self.inside in tr, self.outside in tr)
    # None, datetime, timestamp
    def test_None_to_None(self):
        tr = TimeRange(None, None)
        self.assert_(self.inside not in tr)
        self.assert_(self.outside not in tr)
    def test_None_to_datetime(self):
        tr = TimeRange(None, self.then)
        self.assert_(self.inside in tr)
        self.assert_(self.outside not in tr)
    def test_None_to_timestamp(self):
        tr = TimeRange(None, self.then_ts)
        self.assert_(self.inside in tr)
        self.assert_(self.outside not in tr)
    def test_datetime_to_None(self):
        import time
        time.sleep(0.1)
        # None --> a time AFTER self.now
        lam = lambda: TimeRange(self.now, None)
        print()
        
        
        
        self.assertRaises(ValueError, lambda: TimeRange(self.now, None))
        #self.assert_(self.inside not in tr)
        #self.assert_(self.outside not in tr)
    def test_datetime_to_datetime(self):
        tr = TimeRange(self.now, self.then)
        self.assert_(self.inside in tr)
        self.assert_(self.outside not in tr)
    def test_datetime_to_ts(self):
        tr = TimeRange(self.now, self.then_ts)
        self.assert_(self.inside in tr)
        self.assert_(self.outside not in tr)
    def test_timestamp_to_None(self):
        self.assertRaises(ValueError, lambda: TimeRange(self.now_ts, None))
#         tr = TimeRange(self.now_ts, None)
#         self.assert_(self.inside not in tr)
#         self.assert_(self.outside not in tr)
    def test_timestamp_to_datetime(self):
        tr = TimeRange(self.now_ts, self.then)
        self.assert_(self.inside in tr)
        self.assert_(self.outside not in tr)
    def test_timestamp_to_timestamp(self):
        tr = TimeRange(self.now_ts, self.then_ts)
        self.assert_(self.inside not in tr)
        self.assert_(self.outside not in tr)

    def test_range_contains(self):
        tr = TimeRange(self.now_ts, self.then_ts)
        
#         a, b =self.now_ts+10, self.then_ts-10
#         print(a,b)
#         print()
        
        smaller = TimeRange(self.now_ts+10, self.then_ts-10)
        larger = TimeRange(self.now_ts-10, self.then_ts+10)
        self.assert_(smaller in tr)
        self.assert_(larger not in tr)
    def test_erroring(self):
        self.assertRaises(TypeError, lambda: TimeRange(None, 'stal'))
        self.assertRaises(TypeError, lambda: TimeRange(12.0, 12))
        
        print()
        tr = TimeRange(-11000, 1000)
        
if __name__ == "__main__":
    unittest.main()