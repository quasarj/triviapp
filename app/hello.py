from flask import Flask
from flask_sockets import Sockets
import json
from pprint import pprint

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
def echo_socekt(ws):
    while True:
        message = ws.receive()
        ws.send(message)

@sockets.route('/test')
def test_socket(ws):
    ws.send("Welcome to the websocket test.")
    while True:
        message = ws.receive()
        ws.send("Well, this here is a test!")

@sockets.route('/main')
def main_socket(ws):
    while True:
        message = ws.receive()
        handle_message(message, ws)


def handle_message(message, ws):
    print "Handling message: " + message
    try:
        msg = json.loads(message)
    except:
        print "Received message but it wasn't JSON :("
        ws.send("error")
    print "Message follows:"
    pprint(msg)
    ws.send("message handled")


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    # Note that the websockets will not work this way!
    # Instead use: gunicorn -k flask_sockets.worker hello:app 
    app.debug = True
    app.run()
