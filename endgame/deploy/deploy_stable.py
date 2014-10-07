"""
Script for building test-files.
"""

from __future__ import absolute_import
import os
import shutil
from endgame.deploy import write_record_dir
from endgame.extern.abf import ABFMeta
import abc

#__all__ = ['DispatcherDirABF']



class DispatcherDirABF(object):
    """Operator style class.
    Essentially a functional-style equivalent to Python Abstract Base Classes.""" 
    __metaclass__ = ABFMeta
    dirname = abc.abstractproperty()
    namestub = abc.abstractproperty()
    filecount = abc.abstractproperty()
    recordcount = abc.abstractproperty()
    datadir = os.path.join('..', 'test', 'datafiles') #defaultvalue
    startat = 0 #default value
    @classmethod
    def __call__(cls):
        return cls.make()
    @classmethod
    def make(cls):
        dirpath = os.path.join(cls.datadir, cls.dirname)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        write_record_dir(
            dirpath,
            cls.namestub,
            filecount = cls.filecount,
            recordcount = cls.recordcount,
            startat = cls.startat
        )

class Stable1(DispatcherDirABF):
    dirname = 'stable_dispatcher'
    namestub = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 0

class Stable2(DispatcherDirABF):
    dirname   = 'stable_dispatcher2'
    namestub  = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 5

class Stable3(DispatcherDirABF):
    dirname   = 'stable_dispatcher3'
    namestub  = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 10
    
class Stable4(DispatcherDirABF):
    #dirname   = os.path.join('..', 'test', 'datafiles', 'stable_dispatcher4')
    dirname = 'stable_dispatcher4'
    namestub  = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 15

if __name__ == "__main__":
    Stable1.make()
    Stable2.make()
    Stable3.make()
    Stable4.make()
    from .make_sample_query import make_sample
    make_sample() # setup query file - for unittests
    
    from .set_config_files import set_stable_configs
    set_stable_configs()
