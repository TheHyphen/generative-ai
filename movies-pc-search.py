import csv
import os

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

prompt = input("Search: ")
response = client.embeddings.create(
    input=prompt, model="text-embedding-3-small", dimensions=512
)
search_embedding = response.data[0].embedding

results = index.query(vector=search_embedding, top_k=10, include_metadata=True)
for result in results.matches:
    print(
        f"{result.metadata['title']} ({result.score:.2f}) - {movies[result.id]['overview']}"
    )
