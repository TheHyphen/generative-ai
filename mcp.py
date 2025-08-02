import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
neon_api_key = os.getenv("NEON_TOKEN")

client = OpenAI(api_key=key)

while True:
    prompt = input("User: ")
    history = []
    history.append({"role": "user", "content": prompt})
    response = client.responses.create(
        instructions="You are a helpful assistant, if there are errors, return errors verbatim",
        model="gpt-4.1-mini",
        input=history,
        tools=[
            {
                "type": "mcp",
                "server_label": "neon",
                "server_url": "https://mcp.neon.tech/mcp",
                "require_approval": "never",
                "headers": {"Authorization": f"Bearer {neon_api_key}"},
            },
        ],
    )

    history.append({"role": "assistant", "content": response.output_text})

    print(response.output_text)
