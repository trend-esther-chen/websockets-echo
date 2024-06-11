import base64
import json
import logging

from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

HTTP_SERVER_PORT = 8080

@sockets.route('/media')
def echo(ws):
    # A lot of messages will be sent rapidly. We'll stop showing after the first one.
    has_seen_media = False
    message_count = 0
    while not ws.closed:
        message = ws.receive()
        if message is None:
            ws.send("No message received...")
            continue

        # Messages are a JSON encoded string
        data = json.loads(message)

        # Using the event type you can determine what type of message you are receiving
        if data['event'] == "connected":
            ws.send(f"Connected Message received: {format(message)}")
        if data['event'] == "start":
            ws.send(f"Start Message received: {format(message)}")
        if data['event'] == "media":
            if not has_seen_media:
                ws.send(f"Media message: {format(message)}")
                payload = data['media']['payload']
                ws.send(f"Payload is: {format(payload)}")
                chunk = base64.b64decode(payload)
                ws.send(f"That's {format(len(chunk))} bytes")
                ws.send(f"Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "stop":
            ws.send(f"Stop Message received: {format(message)}")
            break
        message_count += 1
    ws.send(f"Connection closed. Received a total of {format(message_count)} messages")


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    console.log("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    server.serve_forever()
