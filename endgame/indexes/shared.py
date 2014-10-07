from __future__ import absolute_import
import os
import json
import collections
import itertools

__all__ = [
    'dirpath_to_confpath',
    'confpath_to_dirpath',
    'directory_to_config'
]


def dirpath_to_confpath(dirpath):
    if dirpath[-1] == os.sep:
        confpath = dirpath[:-1] + ".json"
    else:
        confpath = dirpath + ".json"
    return confpath

def confpath_to_dirpath(confpath):
    cname, _ = os.path.splitext(confpath)
    return cname

def pathsequence(fullpath):
    return fullpath.split(os.sep)

def directory_to_config(dirpath):
    """Create a configuration file for dirpath, and return it's filepath.
    Place the configuration file on level with the directory. IE:
    parent/
        {dirpath}/
        {dirpath}.json
        
    """
    if not os.path.isdir(dirpath):
        raise ValueError("{0} is not an existing directory.".format(dirpath))
    # Write config_path: remove trailing seperator
    confpath = dirpath_to_confpath(dirpath)
    #Get all csv files
    record_files = [
        pathsequence(os.path.join(dirpath, filepath))
        for filepath in os.listdir(dirpath)
        if filepath.endswith('.csv')
    ]
    # Write JSON config file
    with open(confpath, 'w') as config_file:
        json.dump({'data': record_files}, config_file)
    return confpath

def is_nonstringsequence(value):
    return isinstance(value, collections.Sequence) and not isinstance(value, basestring)

def flatten(seq_of_seq):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(seq_of_seq)

def query_to_url(query):
    """Convert a query object to a URL query term."""
    template = "find/{ips}/{start}/{end}/"
    return template.format(
        ips = query.ips,
        start = query.timerange.start,
        end = query.timerange.end
    )