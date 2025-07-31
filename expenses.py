import csv
import datetime
import json
import os
import base64

from dotenv import load_dotenv
from openai import OpenAI


def add_row(args):
    amount = args["amount"]
    description = args["description"]
    category = args["category"]
    date = args["date"]
    type = args["type"]

    # ensure expenses file exists in the data directory
    if not os.path.exists("data/expenses.csv"):
        with open("data/expenses.csv", "w") as file:
            writer = csv.DictWriter(
                file, fieldnames=["amount", "description", "category", "date", "type"]
            )
            writer.writeheader()

    # ensure expenses file exists in the data directory
    with open("data/expenses.csv", "a") as file:
        writer = csv.DictWriter(
            file, fieldnames=["amount", "description", "category", "date", "type"]
        )
        writer.writerow(
            {
                "amount": amount,
                "description": description,
                "category": category,
                "date": date,
                "type": type,
            }
        )


def get_total_by_category(args):
    category = args["category"]
    with open("data/expenses.csv", "r") as file:
        reader = csv.DictReader(file)
        total = sum(
            float(row["amount"]) for row in reader if row["category"] == category
        )
    return str(total)


def get_total_by_date(args):
    start = args["start"]
    end = args["end"]
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    with open("data/expenses.csv", "r") as file:
        reader = csv.DictReader(file)
        total = sum(
            float(row["amount"])
            for row in reader
            if start_date
            <= datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
            <= end_date
        )
    return str(total)

# read image as base64 string
def read_image(args):
    img_path = args["path"]
    with open(img_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode("utf-8")

    return parse_image(img_data)

tools = [
    {
        "type": "function",
        "name": "add_row",
        "description": "Add a new expense row to the expenses.csv file",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount of the expense",
                },
                "description": {
                    "type": "string",
                    "description": "A very short description of the expense",
                },
                "category": {
                    "type": "string",
                    "description": "The category of the expense",
                    "enum": [
                        "food",
                        "transport",
                        "entertainment",
                        "shopping",
                        "rent",
                        "utilities",
                        "medicine",
                        "other",
                    ],
                },
                "date": {
                    "type": "string",
                    "description": "The date of the expense, formatted as YYYY-MM-DD",
                },
                "type": {
                    "type": "string",
                    "description": "The type of the expense",
                    "enum": ["income", "expense"],
                },
            },
            "required": ["amount", "description", "category", "date", "type"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_total_by_category",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The category of the expense",
                    "enum": [
                        "food",
                        "transport",
                        "entertainment",
                        "shopping",
                        "rent",
                        "utilities",
                        "medicine",
                        "other",
                    ],
                },
            },
            "required": ["category"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_total_by_date",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "The start date of the expense in the format YYYY-MM-DD",
                },
                "end": {
                    "type": "string",
                    "description": "The end date of the expense in the format YYYY-MM-DD",
                },
            },
            "required": ["start", "end"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "read_image",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the image file",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
]

fns = {
    "add_row": add_row,
    "get_total_by_category": get_total_by_category,
    "get_total_by_date": get_total_by_date,
    "read_image": read_image,
}

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=key)

def parse_image(image_data):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_data}"
                    }
                ]
            }
        ],
        instructions="Extract all the text from the image, focus on the expenses in the image."
    )
    return response.output_text

history = []
while True:
    prompt = input("User: ")
    if prompt == "exit":
        break
    history.append({"role": "user", "content": prompt})
    response = client.responses.create(
        instructions=f"You are an expense tracker. To add an expense, call the add_row function. To get totals, call the get_total_by_* functions. Keep your responses short. Today's date is {
            datetime.datetime.now().strftime('%Y-%m-%d')
        }.",
        input=history,
        tools=tools,
        model="gpt-4.1-mini",
    )

    for output in response.output:

        if output.type == "message":
            print(f"Assistant: {output.content[0].text}")
            history.append({"role": "assistant", "content": output.content[0].text})

        elif output.type == "function_call":
            history.append(output)

            function_name = output.name
            function_args = json.loads(output.arguments)

            fn = fns[function_name]
            result = fn(function_args)
            if not result:
                history.append(
                    {
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": "success",
                    }
                )
            else:
                history.append(
                    {
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": result,
                    }
                )

            tool_call_response = client.responses.create(
                input=history, model="gpt-4.1-mini"
            )
            print(f"Assistant: {tool_call_response.output[0].content[0].text}")
            history.append(
                {
                    "role": "assistant",
                    "content": tool_call_response.output[0].content[0].text,
                }
            )
