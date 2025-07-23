import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


response = client.responses.create(
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
    text={
        "format": {
            "type": "json_schema",
            "name": "event",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the event",
                    },
                    "subtitle": {
                        "type": ["string", "null"],
                        "description": "The subtitle of the event",
                    },
                    "company": {
                        "type": "string",
                        "description": "The company organizing the event",
                    },
                    "address": {
                        "type": "string",
                        "description": "The address of the event",
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of the event formatted as dd/mm/yyyy",
                    },
                    "time": {
                        "type": "string",
                        "description": "The time of the event formatted as hh:mm",
                    },
                    "speakers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the speaker",
                                },
                                "company": {
                                    "type": "string",
                                    "description": "The company of the speaker",
                                },
                                "position": {
                                    "type": "string",
                                    "description": "The position of the speaker",
                                },
                            },
                            "required": [
                                "name",
                                "company",
                                "position",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": [
                    "title",
                    "subtitle",
                    "company",
                    "address",
                    "date",
                    "time",
                    "speakers",
                ],
                "additionalProperties": False,
            },
        }
    },
)

print(response.output_text)
card = json.loads(response.output_text)
print("Event information:")
print(f"Title: {card['title']}")
print(f"Subtitle: {card['subtitle']}")
print(f"Company: {card['company']}")
print(f"Address: {card['address']}")
print(f"Date: {card['date']}")
print(f"Time: {card['time']}")
print("Speakers:")
for speaker in card["speakers"]:
    print(f"  Name: {speaker['name']}")
    print(f"  Company: {speaker['company']}")
    print(f"  Position: {speaker['position']}")
