#Getting url query:
from flask import request

app = Flask(__name__)
@app.route('/data')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('user')