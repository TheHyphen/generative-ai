# similarity between embeddings
import os

import orjson
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
results = []
with open("inputs/source_texts.txt", "r") as f:
    source_texts = f.read().splitlines()
    for source_text in source_texts:
        response = client.embeddings.create(
            input=[source_text], model="text-embedding-3-small", dimensions=512
        )
        embeddings = response.data[0].embedding
        results.append({"embeddings": embeddings, "text": source_text})

with open("inputs/embeddings.txt", "w") as f:
    f.write(orjson.dumps(results).decode("UTF-8"))
