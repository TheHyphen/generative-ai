import os
from uuid import uuid4

import orjson
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
pinecone_token = os.environ.get("PINECONE_API_TOKEN")

pc = Pinecone(api_key=pinecone_token)
index = pc.Index(host="https://videos-lrfa8ru.svc.aped-4627-b74a.pinecone.io")


with open("generated/embeddings.json", "r") as f:
    embeddings = orjson.loads(f.read())


vectors = [
    {
        "id": str(uuid4()),
        "values": embedding["vector"],
        "metadata": {"text": embedding["text"]},
    }
    for embedding in embeddings
]

index.upsert(vectors=vectors)
