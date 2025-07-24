import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

r = client.images.generate(
    prompt="Generate a image of snow mountains near beach",
    n=1,
    size="1024x1024",
    model="gpt-image-1",
)

b64 = r.data[0].b64_json
decoded_b64 = base64.b64decode(b64)
with open("generated/snow_mountains_near_beach.png", "wb") as f:
    f.write(decoded_b64)
