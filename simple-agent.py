from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

english = Agent(
    instructions="You are a helpful assistant that is very polite and keeps the conversation short. You always speak in English. You will introduce yourself as 'English Agent'.",
    name="English Agent",
    handoff_description="When the user speaks English, you should hand off the conversation to the English Agent.",
)

telugu = Agent(
    instructions="You are a helpful assistant that is very polite and keeps the conversation short. You always speak in Telugu. You will introduce yourself as 'Telugu Agent'.",
    name="Telugu Agent",
    handoff_description="When the user speaks Telugu, you should hand off the conversation to the Telugu Agent.",
)

first = Agent(
    instructions="You are a helpful assistant that will handover to other agents based on the user's language",
    name="First Agent",
    handoffs=[english, telugu],
)

prompt = input("User: ")
result = Runner.run_sync(first, prompt)
print(result.final_output)
