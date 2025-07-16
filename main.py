import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


def main():
    prompt = input("Enter the prompt: ")
    client = OpenAI(api_key=key)
    r = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    print(r.choices[0].message.content)


if __name__ == "__main__":
    main()
