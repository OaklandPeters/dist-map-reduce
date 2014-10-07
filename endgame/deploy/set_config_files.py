from __future__ import absolute_import
import os

from endgame.indexes import IndexDispatcher

testdir = os.path.join(
    os.path.split(__file__)[0],
    '..', 'test'
)
datadir = os.path.join(testdir, 'datafiles')
os.chdir(datadir)

def setport(config, port):
    with IndexDispatcher(config) as ind:
        ind.config['port'] = port

def set_stable_configs():
    setport('stable_dispatcher.json', 5001)
    setport('stable_dispatcher2.json', 5002)
    setport('stable_dispatcher3.json', 5003)
    setport('stable_dispatcher4.json', 5004)
    setport('stable_metaindex.json', 5005)
    setport('stable_metaindex2.json', 5006)

if __name__ == "__main__":
    set_stable_configs()