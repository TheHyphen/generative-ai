import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")


def main():
    prompt = input("Enter the prompt: ")
    client = OpenAI(api_key=key)
    r = client.responses.create(
        model="gpt-4o",
        input=prompt,
        instructions="Use a lot of emojis in your responses",
    )
    print(r.output_text)


if __name__ == "__main__":
    main()
