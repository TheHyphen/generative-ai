# source text -> embeddings (numbers)
# target text -> embeddings (numbers)
# similarity between embeddings
import os

import orjson
from dotenv import load_dotenv
from openai import OpenAI
from scipy import spatial

load_dotenv()

# vector database
#
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
with open("inputs/embeddings.txt", "r") as f:
    sources = orjson.loads(f.read())

while True:
    prompt = input("S: ")
    target_text = prompt

    target_response = client.embeddings.create(
        model="text-embedding-3-small", input=[target_text]
    )
    v2 = target_response.data[0].embedding

    results = [
        {
            "text": source["text"],
            "similarity": 1
            - spatial.distance.cosine(
                source["embedding"],
                v2,
            ),
        }
        for source in sources
    ]

    print(sorted(results, key=lambda x: x["similarity"], reverse=True)[0]["text"])
