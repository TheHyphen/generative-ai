import json
import os
from enum import Enum

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


class VisitingCard(BaseModel):
    name: str
    phone: str
    email: str
    company: str
    address: str | None
    position: str
    qualification: str | None

class WeddingInvite(BaseModel):
    groom: str
    bride: str
    address: str | None
    date: str | None
    time: str | None


class Type(str, Enum):
    event = "event"
    visiting_card = "visiting_card"
    wedding_invite = "wedding_invite"


types = {
    Type.event: {
        "prompt": "You are a event parser. Given an input image, extract the information from the event. Properly format the text for each field.",
        "schema": Event
    },
    Type.visiting_card: {
        "prompt": "You are a visiting card parser. Given an input image, extract the information from the visiting card. Properly format the text for each field.",
        "schema": VisitingCard
    },
    Type.wedding_invite: {
        "prompt": "You are a wedding invite parser. Given an input image, extract the information from the wedding invite. Properly format the text for each field.",
        "schema": WeddingInvite
    }
}

class Category(BaseModel):
    type: Type

# input_content = [
#    # visiting_card
#     {
#         "type": "input_image",
#         "file_id": "file-NHryhbcY8wNPwdHpUKFZdk",
#     },
# ]
input_content = [
    # event
    {
        "type": "input_image",
        "file_id": "file-Qvue1YjQFBQKiUCv7sQSHr",
    }
]

res = client.responses.parse(
    model="gpt-4.1-nano",
    input=[
        {
            "role": "user",
            "content": input_content,
        }
    ],
    instructions="You are a smart categorizer. Given an input image, respond with what the image represents.",
    text_format=Category
)
type = res.output_parsed.type


response = client.responses.parse(
    model="gpt-4.1-mini",
    instructions=types[type]["prompt"],
    input=[
        {
            "role": "user",
            "content": input_content,
        }
    ],
    text_format=types[type]["schema"]
)

print(response.output_parsed)
