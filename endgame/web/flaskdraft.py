"""
This needs functions, so I can use the Flask.route() decorator
in inline style.

funcs = {}

for 
funcs[key] = webdispatch.route(key)(func)


[] I also need a mapping from the configuration file names to url divisions

"""
from __future__ import absolute_import
import os
from flask import Flask

from ..indexes import IndexDispatcher


os.chdir(os.path.join('..', 'test', 'datafiles'))

webdispatch = Flask(__name__)

# Fake configuration file
data = [
    'stable_dispatcher.json',
    'stable_dispatcher2.json'
]

def invoke_dispatcher(config_path, query):
    return 

query = Query()

for config_path in data:
    cext, cfile = os.path.splitext(config_path)
    webdispatch.route(cext)


for key, value in conf.items():
    @webdispatch.route(key)
    def 

@webdispatch.route('/')
def myfunction():
    return 'stuff'

if __name__ == "__main__":
    webdispatch.run()
    #Access via browser to:
    #http://127.0.0.1:5000/