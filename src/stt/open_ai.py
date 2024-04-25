from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def stt(fpath):
    raise Exception("You are using openAI stt. Please update this code and test it before using it again.")
    client = OpenAI()

    with open(fpath, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript