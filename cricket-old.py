import datetime
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_team_score(team, date):
    # look into my database and get this data
    # wrote a bunch of code to fetch the score
    #
    if team == "IND":
        return {"score": 247}
    elif team == "ENG":
        return {"score": 186}


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

history = []
while True:
    prompt = input("User: ")
    if prompt == "exit":
        break

    history.append({"role": "user", "content": prompt})
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="You are a cricket enthusiast. When users ask you about any cricket match, you invoke the right tool and use the response to form your response to the user. Today is: "
        + datetime.datetime.now().strftime("%Y-%m-%d"),
        tools=[
            {
                "type": "function",
                "name": "get_team_score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team": {"type": "string", "enum": ["IND", "ENG"]},
                        "date": {"type": "string"},
                    },
                    "required": ["team", "date"],
                    "additionalProperties": False,
                },
            }
        ],
        input=history,
    )

    output = response.output[0]

    if output.type == "message":
        print(f"Assistant: {output.text}")
        history.append({"role": "assistant", "content": output.text})
        continue

    if output.type == "function_call":
        history.append(output)

        args = json.loads(output.arguments)
        result = get_team_score(args["team"], args["date"])
        history.append(
            {
                "type": "function_call_output",
                "call_id": output.call_id,
                "output": json.dumps(result),
            }
        )

        r = client.responses.create(model="gpt-4.1-mini", input=history)

        print(f"Assistant: {r.output_text}")
        history.append({"role": "assistant", "content": r.output_text})
        continue
