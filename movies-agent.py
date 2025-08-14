import csv
import json
import os

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
pinecone_token = os.environ.get("PINECONE_API_TOKEN")
openai_token = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_token)
pc = Pinecone(api_key=pinecone_token)
index = pc.Index(host="https://movie-search-lrfa8ru.svc.aped-4627-b74a.pinecone.io")

load_dotenv()

with open("inputs/movies_metadata.csv", "r") as file:
    reader = csv.DictReader(file)
    movies = {movie["id"]: movie for movie in list(reader)}


@function_tool
def movie_search(search_term: str):
    """
    Search for movies based on the search term.
    """
    response = client.embeddings.create(
        input=search_term, model="text-embedding-3-small", dimensions=512
    )
    search_embedding = response.data[0].embedding
    results = index.query(vector=search_embedding, top_k=3, include_metadata=True)
    return json.dumps(
        [
            {
                "title": result.metadata["title"],
                "score": result.score,
                "overview": movies[result.id]["overview"],
            }
            for result in results.matches
        ]
    )


@function_tool
def movie_booking(movie_id: str, pax_count: int):
    """
    Book a movie ticket for the given movie ID and number of people.
    """
    return json.dumps(
        {
            "status": "success",
            "message": f"Ticket booked for {movie_id} for {pax_count} people",
        }
    )


@function_tool
def movie_info(movie_id: str):
    """
    Get information about a movie based on the movie ID.
    """
    return json.dumps(movies[movie_id])


main = Agent(
    instructions="You are a helpful movie agent that will run the required tools to execute tasks for the user based on the user's query. Always make sure to ask user to search for available movies before prompting for booking.",
    name="Movie Agent",
    tools=[movie_search, movie_booking, movie_info],
)

history = []
while True:
    prompt = input("User: ")
    if prompt.lower() == "exit":
        break
    history.append({"role": "user", "content": prompt})
    result = Runner.run_sync(main, history)
    print(f"Assistant: {result.final_output}")
    history.append({"role": "assistant", "content": result.final_output})
