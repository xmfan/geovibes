from calcthread import CalcThread
from flask import Flask, request
from threading import Lock
app = Flask(__name__)

lock = Lock()

@app.route("/")
def hello():
    return "Hello! I'm the server for geovibes"

@app.route("/events", methods=['GET'])
def get_events():
    news = []
    with lock:
        with open('events_write.txt', 'r') as f:
            for line in f:
                print line
                news.append(line)
    return str(news)

if __name__ == "__main__":
    thread = CalcThread(lock)
    thread.start()
    app.run()
