import base64
import csv
import datetime
import os
from enum import Enum

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


class Category(str, Enum):
    food = "food"
    transportation = "transportation"
    entertainment = "entertainment"
    utilities = "utilities"
    shopping = "shopping"
    rent = "rent"
    medicine = "medicine"
    other = "other"


class Expense(BaseModel):
    amount: float
    description: str
    category: Category
    date: datetime.date
    type: str
    """type is either income or expense"""


class CategoryQuery(BaseModel):
    category: Category


class DateRangeQuery(BaseModel):
    start: datetime.date
    end: datetime.date


@function_tool
def add_row(expense: Expense):
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
                "amount": expense.amount,
                "description": expense.description,
                "category": expense.category,
                "date": expense.date,
                "type": expense.type,
            }
        )


@function_tool
def get_total_by_category(query: CategoryQuery):
    category = query.category
    with open("data/expenses.csv", "r") as file:
        reader = csv.DictReader(file)
        total = sum(
            float(row["amount"]) for row in reader if row["category"] == category
        )
    return str(total)


@function_tool
def get_total_by_date(query: DateRangeQuery):
    start_date = query.start
    end_date = query.end
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


@function_tool
def read_image(img_path: str):
    """
    Reads an image file from the given path and returns the text content within the image.
    """
    with open(img_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode("utf-8")

    return parse_image(img_data)


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
                        "image_url": f"data:image/png;base64,{image_data}",
                    }
                ],
            }
        ],
        instructions="Extract all the text from the image, focus on the expenses in the image.",
    )
    return response.output_text


agent = Agent(
    name="Expense Manager",
    instructions=f"You are a helpful expense manager. When user inputs a new expense, you should call the available tools to perform actions or respond. Today is {datetime.date.today()}",
    tools=[add_row, get_total_by_category, get_total_by_date, read_image],
)

history = []
while True:
    prompt = input("User: ")
    if prompt.lower() == "exit":
        break
    history.append({"role": "user", "content": prompt})
    result = Runner.run_sync(agent, history)
    print(f"Assistant: {result.final_output}")
    history.append({"role": "assistant", "content": result.final_output})
