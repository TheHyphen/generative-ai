import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
                    "file_id": "file-VxqXsJnRveudMJXSWuaPdk",
                },
            ],
        }
    ],
)

print(response.output_text)
