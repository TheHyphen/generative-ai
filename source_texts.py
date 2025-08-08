import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

results = []
while True:
    responses = client.responses.create(
        model="gpt-4.1-nano", input="Say something random", temperature=0.9
    )
    print(responses.output_text)
    results.append(responses.output_text)
    if len(results) >= 20:
        break
# write to file
with open("inputs/results.txt", "w") as f:
    for result in results:
        f.write(result + "\n")
