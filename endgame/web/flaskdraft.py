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


os.chdir(os.path.join('..', 'test', 'datafiles'))

webdispatch = Flask(__name__)

# Fake configuration file
data = [
    'stable_dispatcher.json',
    'stable_dispatcher2.json'
]

for key, value in conf.items():
    @webdispatch.route(key)
    def 

@webdispatch.route('/')
def myfunction():
    return 'stuff'

if __name__ == "__main__":
    webdispatch.run()