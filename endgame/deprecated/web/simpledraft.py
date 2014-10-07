from __future__ import absolute_import
import os

from flask import Flask

webdispatch = Flask('simpleapplication')

lam = lambda: "Little lamb."

D = {}

D = webdispatch.route('/')(lam)



if __name__ == "__main__":
    
    webdispatch.run()
    #Access via browser to:
    #http://127.0.0.1:5000/