import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

context = []

while True:
    user_input = input("User: ")
    context.append({"role": "user", "content": user_input})
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=context,
        instructions="You are a JSON parser for parsing Home Automation commands",
        text={
            "format": {
                "type": "json_schema",
                "name": "home_automation_commands",
                "schema": {
                    "type": "object",
                    "properties": {
                        "equipment": {
                            "type": "string",
                            "description": "The name of the equipment to control",
                            "enum": ["light", "ac", "fan", "water motor"],
                        },
                        "desired_status": {
                            "type": "boolean",
                            "description": "The desired status of the equipment",
                        },
                        "location": {
                            "type": "string",
                            "description": "The location of the equipment",
                            "enum": [
                                "living_room",
                                "bedroom",
                                "kitchen",
                                "bathroom",
                                "unknown",
                            ],
                        },
                    },
                    "required": ["equipment", "desired_status", "location"],
                    "additionalProperties": False,
                },
            }
        },
    )
    context.append({"role": "assistant", "content": response.output_text})
    print(response.output_text)
