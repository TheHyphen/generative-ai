import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_match_score(team):
    if team == "IND":
        return 347

    if team == "ENG":
        return 234

    if team == "NZL":
        return 123

    if team == "AUS":
        return 320


tools = [
    {
        "type": "function",
        "name": "get_match_score",
        "description": "Get the score of a cricket team",
        "parameters": {
            "type": "object",
            "properties": {
                "team": {"type": "string", "enum": ["IND", "ENG", "NZL", "AUS"]}
            },
            "required": ["team"],
            "additionalProperties": False,
        },
    }
]

history = []
while True:
    prompt = input("User: ")
    history.append({"role": "user", "content": prompt})

    response = client.responses.create(
        model="gpt-4.1-nano",
        tools=tools,
        instructions="You are a cricket expert, when asked for team score, call the get_match_score function to get the score.",
        input=history,
    )

    output = response.output[0]

    if output.type == "message":
        print(f"Assistant: {response.output_text}")
        history.append({"role": "assistant", "content": response.output_text})
        continue

    if output.type == "function_call":
        args = json.loads(output.arguments)
        score = get_match_score(args["team"])

        history.append(output)
        history.append(
            {
                "type": "function_call_output",
                "call_id": output.call_id,
                "output": str(score),
            }
        )

        tool_response = client.responses.create(
            model="gpt-4.1-nano",
            input=history,
        )

        print(f"Assistant: {tool_response.output_text}")
        history.append({"role": "assistant", "content": tool_response.output_text})

        continue
