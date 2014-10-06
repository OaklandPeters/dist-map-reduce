from __future__ import absolute_import
import os
import shutil
from endgame.deploy import write_record_dir

class DispatcherDir(object):
    """Operator style class.""" 
    @classmethod
    def make(cls):
        if os.path.exists(cls.dirname):
            shutil.rmtree(cls.dirname)
        write_record_dir(
            cls.dirname,
            cls.namestub,
            filecount = cls.filecount,
            recordcount = cls.recordcount,
            startat = cls.startat
        )
#     # Default Values
#     dirname = 'stable_dispatcher'
#     namestub = 'stable_1k'
#     filecount = 5
#     recordcount = 1000
#     startat = 0

class Stable1(DispatcherDir):
    dirname = 'stable_dispatcher'
    namestub = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 0

class Stable2(DispatcherDir):
    dirname   = 'stable_dispatcher2'
    namestub  = 'stable_1k'
    filecount = 5
    recordcount = 1000
    startat = 5

#Stable1.make()
#Stable2.make()
