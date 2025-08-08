# source text -> embeddings (numbers)
# target text -> embeddings (numbers)
# similarity between embeddings
import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


source_text = "I like burgers"
source_response = client.embeddings.create(
    model="text-embedding-3-small", input=[source_text]
)
v1 = source_response.data[0].embedding

while True:
    prompt = input("S: ")
    target_text = prompt

    target_response = client.embeddings.create(
        model="text-embedding-3-small", input=[target_text]
    )
    v2 = target_response.data[0].embedding

    cosine_similarity = np.dot(v1, v2) / np.linalg.norm(v1) * np.linalg.norm(v2)
    print(cosine_similarity)
