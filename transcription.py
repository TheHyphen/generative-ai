import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

r = client.audio.transcriptions.create(
    model="gpt-4o-mini-transcribe", file=open("inputs/sample.m4a", "rb")
)

print(r.text)
