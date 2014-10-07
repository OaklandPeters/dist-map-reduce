import json
from flask import request, Flask
from flask.ext import restful
from werkzeug.routing import BaseConverter

from endgame.interfaces import Record, Query

app = Flask(__name__)



class ListConverter(BaseConverter):
    def to_python(self, value):
        return str(value).strip('[]').split(',')
    def to_url(self, values):
        return "[{0}]".format(
            ','.join(BaseConverter.to_url(value)
                for value in values)
        ) 

class FloatConverter(BaseConverter):
    def to_python(self, value):
        return float(value)
    def to_url(self, value):
        return str(value)


app.url_map.converters['list'] = ListConverter
app.url_map.converters['float'] = FloatConverter



    

#find/[3.42.225.161]/1412619807.79/1412619808.59/
#... note: no quotes or spaces in ips

#@app.route('/find/<ip>/<float:lower>/<float:upper>')
@app.route('/find/<list:ips>/<float:lower>/<float:upper>/')
def find(ips='a', lower=0.0, upper=0.0):
    #ip = ListConverter.to_python(ip)
    
    query = Query(ips, (lower, upper))
    
    msg = ""
    msg += "ips {klass}: {value}".format(
        klass = type(ips).__name__, value = ips
    )
    msg += "<br>"
    msg += "lower {klass}: {value}".format(
        klass = type(lower).__name__, value = lower
    )
    msg += "<br>"
    msg += "upper {klass}: {value}".format(
        klass = type(upper).__name__, value = upper
    )
    msg += "<br>"
    msg += "query {klass}: {value}".format(
        klass = type(query).__name__, value = query
    )
    
    return msg
        



#==============================================================================
#    Local Utility Functions
#==============================================================================
def query_to_url(query):
    """Migrate this to another location.
    """
    template = "find/{ips}/{start}/{end}/"
    return template.format(
        ips = query.ips,
        start = query.start,
        end = query.end
    )



if __name__ == "__main__":
    app.run(debug=True)
