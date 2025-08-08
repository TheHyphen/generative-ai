import os

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
pinecone_token = os.environ.get("PINECONE_API_TOKEN")
openai_token = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_token)
pc = Pinecone(api_key=pinecone_token)
index = pc.Index(host="https://videos-lrfa8ru.svc.aped-4627-b74a.pinecone.io")

prompt = input("Search: ")
response = client.embeddings.create(
    input=[prompt], model="text-embedding-3-small", dimensions=512
)
vec = response.data[0].embedding

results = index.query(
    vector=vec,
    top_k=3,
    include_metadata=True,
)
print(results.matches[0].metadata["text"])
