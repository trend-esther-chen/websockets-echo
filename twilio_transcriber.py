import os
import assemblyai as aai
from app_logger import Logger

aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

TWILIO_SAMPLE_RATE = 8000 # Hz

logger = Logger(__name__)

def on_open(session_opened: aai.RealtimeSessionOpened):
    "Called when the connection has been established."
    logger.info(f"Session ID:{session_opened.session_id}", )


def on_data(transcript: aai.RealtimeTranscript):
    "Called when a new transcript has been received."
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        logger.info(f"{transcript.text}\r\n")
    else:
        logger.info(f"{transcript.text}\r")


def on_error(error: aai.RealtimeError):
    "Called when the connection has been closed."
    logger.error(f"An error occured:{error}")


def on_close():
    "Called when the connection has been closed."
    logger.info("Closing Session")


class TwilioTranscriber(aai.RealtimeTranscriber):
    def __init__(self):
        super().__init__(
            on_data=on_data,
            on_error=on_error,
            on_open=on_open, # optional
            on_close=on_close, # optional
            sample_rate=TWILIO_SAMPLE_RATE,
            encoding=aai.AudioEncoding.pcm_mulaw
        )
