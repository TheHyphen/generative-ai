import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VisitingCard(BaseModel):
    name: str
    phone: str
    email: str
    company: str
    address: str | None
    position: str
    qualification: str | None


response = client.responses.parse(
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
    text_format=VisitingCard
)

card = response.output_parsed
print("Visiting card information:")
print(f"Name: {card.name}")
print(f"Phone: {card.phone}")
print(f"Email: {card.email}")
print(f"Company: {card.company}")
print(f"Address: {card.address}")
print(f"Position: {card.position}")
print(f"Qualification: {card.qualification}")
