import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are a visiting card parser. Given an input image, extract the information from the visiting card. Properly format the text for each field..",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "file_id": "file-NHryhbcY8wNPwdHpUKFZdk",
                },
            ],
        }
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "visiting_card",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person",
                    },
                    "phone": {
                        "type": "string",
                        "description": "The phone number of the person. Always include the country code.",
                    },
                    "email": {
                        "type": "string",
                        "description": "The email address of the person",
                    },
                    "company": {
                        "type": "string",
                        "description": "The company name of the person",
                    },
                    "address": {
                        "type": ["string", "null"],
                        "description": "The address of the company",
                    },
                    "position": {
                        "type": "string",
                        "description": "The position of the person",
                    },
                    "qualification": {
                        "type": ["string", "null"],
                        "description": "The qualification of the person",
                    },
                },
                "required": [
                    "name",
                    "phone",
                    "email",
                    "company",
                    "address",
                    "position",
                    "qualification",
                ],
                "additionalProperties": False,
            },
        }
    },
)

print(response.output_text)
card = json.loads(response.output_text)
print("Visiting card information:")
print(f"Name: {card['name']}")
print(f"Phone: {card['phone']}")
print(f"Email: {card['email']}")
print(f"Company: {card['company']}")
print(f"Address: {card['address']}")
print(f"Position: {card['position']}")
print(f"Qualification: {card['qualification']}")
