#!/usr/bin/env python
from __future__ import absolute_import
import random
import datetime
import csv
from ..timerange import datetime_to_timestamp
from ..interfaces import Record

__all__ = [
    'write_records_csv',
    'read_records_csv',
    'convert_records_csv',
    'read_records',
    'IPv4',
    'TimeStamp'
]

def main(count):
    """The original function given in the problem statement."""
    for x in xrange(count): 
        first_number = random.randint(0, 255)
        second_number = random.randint(0, 255)
        third_number = random.randint(0, 255)
        fourth_number = random.randint(0, 255)
    print "%d.%d.%d.%d" % (first_number, second_number, third_number, fourth_number)

def IPv4():
    """Factory for IPv4 strings."""
    return "%d.%d.%d.%d" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
def TimeStamp(start=None, interval=None):
    """Factory for TimeStamps.
    start: None --> use now
    interval: None --> at start
        float --> seconds after start
        function --> execute to get interval (eg. for randomization)
    """
    if start is None:
        start = datetime_to_timestamp(datetime.datetime.now())
    if interval is None:
        interval = 0.0
    if callable(interval):
        interval = interval()
    # Typechecking
    if not isinstance(start, float):
        raise TypeError("'start' should be a float.")
    if not isinstance(interval, float):
        raise TypeError("'interval' should be a float.")
    return start + interval

def record(ip=None, ts=None):
    if ip is None:
        ip = IPv4()
    if ts is None:
        ts = TimeStamp()
    return (repr(ip), repr(ts))

def rand_records(count=1000, interval=100.0):
    if interval is None:
        interval = 0
    if not isinstance(interval, float):
        raise TypeError("'interval' should be an integer.")
    
    for x in xrange(count):
        yield (
            IPv4(),
            TimeStamp(start=None, interval=x*interval)
        )

def write_records_csv(filename, count=1000, interval=100.0):
    """
    Write to flat CSV file. Why CSV instead of JSON?
    Smaller files, and faster for simple data (which this is).
    """
    records = rand_records(count=count, interval=interval)
    with open(filename, 'w') as out:
        csvwriter = csv.writer(out, lineterminator='\n',)
        csvwriter.writerows(records)

def read_records_csv(filename):
    with open(filename, 'rb') as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            yield row[0], row[1]

def convert_records_csv(filename):
    for ip, ts in read_records_csv(filename):
        #How to convert?
        yield ip, float(ts)

def read_records(filename):
    return [
        Record(ip, ts)
        for ip, ts in convert_records_csv(filename)
    ]
