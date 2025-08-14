import csv
import os

import orjson
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
pinecone_token = os.environ.get("PINECONE_API_TOKEN")
openai_token = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_token)
pc = Pinecone(api_key=pinecone_token)
index = pc.Index(host="https://movie-search-lrfa8ru.svc.aped-4627-b74a.pinecone.io")

with open("inputs/movies_metadata.csv", "r") as file:
    reader = csv.DictReader(file)
    movies = {
        movie["id"]: {"title": movie["original_title"], "overview": movie["overview"]}
        for movie in list(reader)
    }

with open("generated/batch_689b5732bb70819092365a43a1bb00d7_output.jsonl", "r") as file:
    lines = [orjson.loads(line) for line in file.readlines()]
    embeddings = [
        {
            "id": line["custom_id"],
            "values": line["response"]["body"]["data"][0]["embedding"],
            "metadata": {"title": movies[line["custom_id"]]["title"]},
        }
        for line in lines
    ]

# chunk into batches of 500
chunk_size = 500
chunks = [embeddings[i : i + chunk_size] for i in range(0, len(embeddings), chunk_size)]

for chunk in chunks:
    print(f"Processing chunk {chunks.index(chunk) + 1}/{len(chunks)}")
    index.upsert(vectors=chunk)
