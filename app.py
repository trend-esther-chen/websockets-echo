import base64
import json

from fastapi import FastAPI, WebSocket
from app_logger import Logger
import uvicorn

from twilio_transcriber import TwilioTranscriber

app = FastAPI()

SERVER_PORT = 8000
logger = Logger(__name__)

@app.websocket("/media")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    message_count = 0
    try:
        while True:
            message = await websocket.receive_text()
            logger.info(f"Message text was: {message}")
            if message is None:
                logger.info("No message received...")
                websocket.send_text("No message received...")
                continue
            # Messages are a JSON encoded string
            data = json.loads(message)

            # Using the event type you can determine what type of message you are receiving
            if data['event'] == "connected":
                logger.info("Connected Message received: {}".format(message))
                await websocket.send_text(f"Connected Message received: {format(message)}")
                transcriber = TwilioTranscriber()
                transcriber.connect()
            if data['event'] == "start":
                logger.info("Start Message received: {}".format(message))
                await websocket.send_text(f"Start Message received: {format(message)}")
            if data['event'] == "media":
                payload_b64 = data['media']['payload']
                payload_mulaw = base64.b64decode(payload_b64)
                transcriber.stream(payload_mulaw)
            if data['event'] == "stop":
                logger.info("Stop Message received: {}".format(message))
                await websocket.send_text(f"Stop Message received: {format(message)}")
                transcriber.close()
                break
            message_count += 1
    except Exception as e:
        logger.error(f"Connection error: {e}")
    finally:
        await websocket.close()
    logger.info("Connection closed. Received a total of {} messages".format(message_count))


if __name__ == '__main__':
    logger.debug(f"Server started on port {SERVER_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
    
