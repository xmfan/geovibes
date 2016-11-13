from calcthread import CalcThread
from flask import Flask, request
from flask_cors import CORS, cross_origin
from threading import Lock
import json

app = Flask(__name__)
CORS(app)

lock = Lock()

@app.route("/")
@cross_origin()
def hello():
    return "Hello! I'm the server for geovibes"

@app.route("/events", methods=['GET'])
@cross_origin()
def get_events():
    js = '{ \'response\': ['
    with lock:
        with open('events_write.txt', 'r') as f:
            for line in f:
                js += str(line) + ','
    js += ']}'
    return js

def start_calc():
    print "threads started"
    thread = CalcThread(lock)
    thread.start()

app.before_first_request(start_calc)

if __name__ == "__main__":
    print "hello i started"
    app.run()
