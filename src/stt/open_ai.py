import logging
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
client = OpenAI()


def stt(fpath):
    logger.info(f"Requesting transcription from openai")
    with open(fpath, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

