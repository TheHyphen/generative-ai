import json
import os
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are an image parser. After parsing the image, call the right tool with the provided schema.",
    input=[
        {
            "role": "user",
            "content": [{
                "type": "input_image",
                "file_id": "file-Qvue1YjQFBQKiUCv7sQSHr",
            }]
        }
    ],
    tools=[
        {
            "type": "function",
            "name": "parsed_event",
            "description": "Parse an event from an image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "date": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["title", "date", "location"],
                "additionalProperties": False
            }
        },
        {
            "type": "function",
            "name": "parsed_visiting_card",
            "description": "Parse a visiting card from an image.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"}
                },
                "required": ["name", "phone", "email"],
                "additionalProperties": False
            }
        }
    ]
)

type = response.output[0].name

if type == "parsed_event":
    print("Event: ")
    print(response.output[0].arguments)

elif type == "parsed_visiting_card":
    print("Visiting Card: ")
    print(response.output[0].arguments)
