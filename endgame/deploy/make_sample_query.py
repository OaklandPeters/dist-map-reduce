from __future__ import absolute_import
import csv
import os
import random
from endgame.interfaces import Record, Query


testdir = os.path.join(
    os.path.split(__file__)[0],
    '..', 'test'
)
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)

# Needs to create
#from sample_query import target_entry, target_record, query


#stable_1k_0.csv

#204.156.219.159,1412682642.48
#added to end of:
#   stable_dispatcher/stable_1k_2.csv

#Algorithm for making this:
# read 100th entry from stable_dispatcher
# copy to end of:
#    stable_dispatcher/stable_1k_2.csv
#    stable_dispatcher2/stable_1k_9.csv
#    

add_to_files = [
    os.path.join('stable_dispatcher', 'stable_1k_2.csv'),
    os.path.join('stable_dispatcher2', 'stable_1k_9.csv'),
    os.path.join('stable_dispatcher3', 'stable_1k_10.csv'),
    
]
basefile = os.path.join('stable_dispatcher', 'stable_1k_0.csv')
baserownumber = 100
query_time_variance = 0.4 #must be bigger than data point variance 'trange'
trange = 0.1
querypath = os.path.join(testdir,'sample_query.py')
append_files_flag = True


def make_sample():
    base_record = get_base()
    query_range = [
        base_record.timestamp - query_time_variance,
        base_record.timestamp + query_time_variance
    ]
    
    # Add to files, modified slightly
    if append_files_flag:
        for afile in add_to_files:
            randomized_append(
                afile,
                trange=0.1,
                columns=[base_record.ip, base_record.timestamp]
            )
    # Write import-able Python config file containing query and sample record
    write_sample_query(querypath, base_record, query_range)

def write_sample_query(filepath, base_record, query_range):
    
    msg = "from ..interfaces import Query, Record\n"
    msg += "# From file '{0}' row number {1}\n".format(basefile, baserownumber)
    msg += "# added to end of files: {0}\n".format(add_to_files)
    msg += "target_entry = ['{0}', {1}]\n".format(
        base_record.ip, str(base_record.timestamp)
    )
    msg += "target_record = Record('{0}', {1})\n".format(
        base_record.ip, str(base_record.timestamp)
    )
    msg += ("query = Query(\n"
        + "    '{0}',\n"
        + "    ({1}, {2})\n"
        + ")\n"
    ).format(base_record.ip, query_range[0], query_range[1])
    msg += "\n"
    
    with open(filepath, 'w') as queryfile:
        queryfile.write(msg)


def get_base():
    with open(basefile, 'rb') as infile:
        csvreader = csv.reader(infile)
        for i, row in enumerate(csvreader):
            if i == baserownumber:
                return Record(row[0], row[1])


def randomized_append(filepath, trange=0.0, columns=None):
    ip, timestamp = columns
    X = random.randint(0, 2)
    if X == 0:
        timestamp = timestamp - trange
    if X == 2:
        timestamp = timestamp + trange
    append_to_file(filepath, ip, timestamp)
        

def append_to_file(filepath, *columns):
    with open(filepath, 'a') as out:
        csvwriter = csv.writer(out, lineterminator='\n',)
        csvwriter.writerow(columns)

if __name__ == "__main__":
    make_sample()