import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


def main():
    client = OpenAI(api_key=key)
    prompt = input("User: ")
    r = client.responses.create(
        model="gpt-4o",
        input=prompt,
        instructions="You are a natural language to JSON parser to help with currency conversion. When you receive an input, convert it into JSON with the following properties: 'from' (3 letter currency code), 'to' (3 letter currency code) and the amount which is the amount. Do not use markdown formatting.",
        text={
            "format": {
                "type": "json_schema",
                "name": "currency_conversion",
                "schema": {
                    "type": "object",
                    "properties": {
                        "from": {
                            "type": "string",
                            "description": "The 3 letter currency code to convert from",
                        },
                        "to": {
                            "type": "string",
                            "description": "The 3 letter currency code to convert to",
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount to convert",
                        },
                    },
                    "required": ["from", "to", "amount"],
                    "additionalProperties": False,
                },
            }
        },
    )
    print(r.output_text)


if __name__ == "__main__":
    main()
