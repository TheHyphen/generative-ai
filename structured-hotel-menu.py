import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

# read the menu.txt from inputs


def read_menu():
    with open("inputs/menu.txt", "r") as f:
        return f.read()


def main():
    client = OpenAI(api_key=key)
    prompt = read_menu()
    r = client.responses.create(
        model="gpt-4o",
        input=prompt,
        instructions="You are a natural language to JSON parser to help with restaurant menus.",
        text={
            "format": {
                "type": "json_schema",
                "name": "menu_parsing",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the restaurant",
                        },
                        "dishes": {
                            "type": "array",
                            "description": "The 3 letter currency code to convert to",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the dish",
                                    },
                                    "price": {
                                        "type": "number",
                                        "description": "The price of the dish",
                                    },
                                    "category": {
                                        "type": "string",
                                        "description": "The category of the dish",
                                    },
                                    "ingredients": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "description": "The ingredients of the dish",
                                        },
                                    },
                                },
                                "required": [
                                    "name",
                                    "price",
                                    "category",
                                    "ingredients",
                                ],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["name", "dishes"],
                    "additionalProperties": False,
                },
            }
        },
    )
    menu = json.loads(r.output_text)
    for dish in menu["dishes"]:
        print(f"{dish['name']} ({dish['category']}): ${dish['price']}")
        print("Ingredients:")
        for ingredient in dish["ingredients"]:
            print(f"- {ingredient}")
        print()


if __name__ == "__main__":
    main()
