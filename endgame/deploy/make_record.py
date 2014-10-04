#!/usr/bin/env python 
import sys
import random
import datetime
import csv


def main(count): 
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
        int --> seconds after start
        function --> execute to get interval (eg. for randomization)
    """
    if start is None:
        start = datetime.datetime.now().microsecond
    if interval is None:
        interval = 0
    if callable(interval):
        interval = interval()
    # Typechecking
    if not isinstance(start, int):
        raise TypeError("'start' should be an integer.")
    if not isinstance(interval, int):
        raise TypeError("'interval' should be an integer.")
    return start + interval

def record(ip=None, ts=None):
    if ip is None:
        ip = IPv4()
    if ts is None:
        ts = TimeStamp()
    return (repr(ip), repr(ts))

def rand_records(count=1000, interval=100):
    if interval is None:
        interval = 0
    if not isinstance(interval, int):
        raise TypeError("'interval' should be an integer.")
    
    for x in xrange(count):
        yield (
            IPv4(),
            TimeStamp(start=None, interval=x*interval)
        )

def write_records_csv(filename, count=1000, interval=100):
    """
    Write to flat CSV file. Why CSV instead of JSON?
    Smaller files, and faster for simple data (which this is).
    """
    records = rand_records(count=count, interval=interval)
    with open(filename, 'w') as out:
        csvwriter = csv.writer(out)
        csvwriter.writerows(records)

def read_records_csv(filename):
    with open(filename, 'rb') as infile:
        csvreader = csv.reader(infile)
        for row in csvreader:
            yield row[0], row[1]

def convert_records_csv(filename):
    for ip, ts in read_records_csv(filename):
        #How to convert?
        yield ip, int(ts)
    
        

if __name__ == "__main__":

    write_records_csv('100k.csv', count=100000)
    
    #Time test this
    results = list(convert_records_csv('1k.csv'))
    
    print()