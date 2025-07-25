import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Speaker(BaseModel):
    name: str
    company: str | None
    position: str | None

class Event(BaseModel):
    title: str
    subtitle: str | None
    company: str | None
    address: str | None
    date: str | None
    time: str | None
    speakers: list[Speaker]

response = client.responses.parse(
    model="gpt-4.1-mini",
    instructions="You are a event parser. Given an input image, extract the information from the event. Properly format the text for each field..",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "file_id": "file-Qvue1YjQFBQKiUCv7sQSHr",
                },
            ],
        }
    ],
    text_format=Event,
)

card = response.output_parsed
print(card)
print("Event information:")
print(f"Title: {card.title}")
print(f"Subtitle: {card.subtitle}")
print(f"Company: {card.company}")
print(f"Address: {card.address}")
print(f"Date: {card.date}")
print(f"Time: {card.time}")
print("Speakers:")
for speaker in card.speakers:
    print(f"  Name: {speaker.name}")
    print(f"  Company: {speaker.company}")
    print(f"  Position: {speaker.position}")
