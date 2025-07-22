import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

history = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "What do you think is the brand of the car in the image?",
            },
            {
                "type": "input_image",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Bugatti_Typ_13_Brescia_Sport-Racing_1922.jpg",
            },
        ],
    }
]
while True:
    prompt = input("User: ")
    history.append({"role": "user", "content": prompt})
    response = client.responses.create(
        model="gpt-4o",
        input=history,
    )
    history.append({"role": "assistant", "content": response.output_text})

    print(response.output_text)
