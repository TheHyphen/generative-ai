import os

import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


def main():
    prompt = input("Enter the prompt: ")
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
        },
        json={
            "model": "gpt-4.1",
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    text = r.json()["choices"][0]["message"]["content"]
    print(text)


if __name__ == "__main__":
    main()
