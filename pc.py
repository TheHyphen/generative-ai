import os
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
pinecone_token = os.environ.get("PINECONE_API_TOKEN")
openai_token = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_token)
pc = Pinecone(api_key=pinecone_token)
index = pc.Index(host="https://videos-lrfa8ru.svc.aped-4627-b74a.pinecone.io")

with open("inputs/source_texts.txt", "r") as f:
    source_texts = f.readlines()
    source_texts = [text.strip() for text in source_texts]


for text in source_texts:
    response = client.embeddings.create(
        input=[text], model="text-embedding-3-small", dimensions=512
    )
    vec = response.data[0].embedding
    index.upsert(
        vectors=[
            {"id": str(uuid4()), "values": vec, "metadata": {"text": text}},
        ]
    )
