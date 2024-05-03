from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def stt(fpath):
    with open(fpath, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text
