import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# image -> base64 -> text

image_path = "images/book.jpg"

with open(image_path, "rb") as image:
    image_base64 = base64.b64encode(image.read()).decode("utf-8")

print(image_base64)
response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "What is this book about?",
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}",
                },
            ],
        }
    ],
)

print(response.output_text)
