import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from github import readme
from youtube import transcript

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_youtube_transcript(args):
    url = args["url"]
    result = transcript.download(url)
    return result


def get_github_repo_readme(args):
    repo = args["repo"]
    result = readme.download(repo)
    return result


fns = {
    "get_youtube_transcript": get_youtube_transcript,
    "get_github_repo_readme": get_github_repo_readme,
}

tools = [
    {
        "type": "function",
        "name": "get_youtube_transcript",
        "description": "Get the transcript of a YouTube video",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL of the YouTube video"}
            },
            "required": ["url"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_github_repo_readme",
        "description": "Get the README file of a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {
                    "type": "string",
                    "description": "The repo of the GitHub repository in the form of username/repo",
                }
            },
            "required": ["repo"],
            "additionalProperties": False,
        },
    },
]

history = []
while True:
    prompt = input("User: ")
    history.append({"role": "user", "content": prompt})

    response = client.responses.create(
        model="gpt-4.1-nano",
        tools=tools,
        instructions="You are a summary generator. When you receive a link, get the content using one of the functions and then return a short summary from the content",
        input=history,
    )

    output = response.output[0]

    if output.type == "message":
        print(f"Assistant: {response.output_text}")
        history.append({"role": "assistant", "content": response.output_text})
        continue

    if output.type == "function_call":
        args = json.loads(output.arguments)

        history.append(output)
        history.append(
            {
                "type": "function_call_output",
                "call_id": output.call_id,
                "output": fns[output.name](args),
            }
        )

        tool_response = client.responses.create(
            model="gpt-4.1-nano",
            input=history,
        )

        print(f"Assistant: {tool_response.output_text}")
        history.append({"role": "assistant", "content": tool_response.output_text})

        continue
