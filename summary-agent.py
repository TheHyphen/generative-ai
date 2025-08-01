from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

from github import readme
from youtube import transcript

load_dotenv()


@function_tool
def get_youtube_video_transcript(url: str):
    result = transcript.download(url)
    return result


@function_tool
def get_github_readme(repo: str):
    """
    Fetches the README.md file of a GitHub repository given the repository in the format <user>/<repo>.
    """
    return readme.download(repo)


youtube = Agent(
    instructions="You are a helpful assistant that is good at summarizing YouTube videos. When user gives a URL, download the transcript and then summarize it",
    name="YouTube Agent",
    handoff_description="When the user says they want to summarize a YouTube video",
    tools=[get_youtube_video_transcript],
)

github = Agent(
    instructions="You are a helpful assistant that is good at summarizing GitHub repositories",
    name="GitHub Agent",
    handoff_description="When the user says they want to summarize a GitHub repository",
    tools=[get_github_readme],
)

agent = Agent(
    instructions="You are a helpful assistant that will handover to other agents based on the user's summarizing request",
    name="Agent",
    handoffs=[youtube, github],
)

prompt = input("User: ")
result = Runner.run_sync(agent, prompt)
print(result.final_output)
