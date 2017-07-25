from flask import Flask, make_response, jsonify



from util import dbhelper

import json


app = Flask(__name__)

@app.route('/')
def hello_world():
    resp = make_response(jsonify({"errno":0,"errmsg":None}))
    resp.headers['content-type'] = 'application/json'
    return resp


@app.route('/trailList')
def trailList():
    one = dbhelper.DBHelper()
    items = one.selectAll()
    items = json.dumps(items)
    resp = make_response(items)
    resp.headers['content-type'] = 'application/json'
    return resp

if __name__ == '__main__':
    app.run()