"""
@todo: Pair with this something which writes the config file
... or something which builds a config file based on the folder
"""
from __future__ import absolute_import
import os
from .make_record import write_records_csv

__all__ = [
    'write_record_dir'
]

def write_record_dir(dirpath, namestub, filecount=5, recordcount=1000):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    
    # Remove any potential file name
    namestub, _ = os.path.splitext(namestub)
    
    for fileno in xrange(filecount):
        filename = "{0}_{1}.csv".format(namestub, fileno) 
        fullpath = os.path.join(dirpath, filename)
        
        write_records_csv(fullpath, count=recordcount)