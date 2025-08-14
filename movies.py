import csv
import json


def deduplicate_movies(movies_list):
    return list({movie["id"]: movie for movie in movies_list}.values())


with open("inputs/movies_metadata.csv", "r") as file:
    reader = csv.DictReader(file)
    movies = [
        {"title": movie["title"], "overview": movie["overview"], "id": movie["id"]}
        for movie in list(reader)
    ]

batch = "\n".join(
    [
        json.dumps(
            {
                "body": {
                    "model": "text-embedding-3-small",
                    "input": [movie["overview"]],
                    "dimensions": 512,
                },
                "method": "POST",
                "url": "/v1/embeddings",
                "custom_id": movie["id"],
            }
        )
        for movie in deduplicate_movies(movies[:5000])
    ]
)

with open("generated/movies-batch.jsonl", "w") as file:
    file.write(batch)
