import orjson
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# with open("inputs/animals.txt", "r") as f:
#     text = f.read()

# with open("generated/batch.jsonl", "w") as f:
#     for line in text.split("\n"):
#         id = uuid.uuid4()
#         req = {
#             "custom_id": str(id),
#             "method": "POST",
#             "url": "/v1/embeddings",
#             "body": {
#                 "input": [line.strip()],
#                 "model": "text-embedding-3-small",
#                 "dimensions": 512,
#             },
#         }
#         req_json = orjson.dumps(req).decode("utf-8")
#         f.write(req_json + "\n")


# file = client.files.create(file=open("generated/batch.jsonl", "rb"), purpose="batch")

# response = client.batches.create(
#     input_file_id=file.id,
#     endpoint="/v1/embeddings",
#     completion_window="24h",
# )

# print(response)


inputs = {}
with open("generated/batch.jsonl", "r") as f:
    for line in f.readlines():
        req = orjson.loads(line)
        inputs[req["custom_id"]] = req

outputs = []
with open("generated/batch_6896a5b5d84c8190997d75675864c538_output.jsonl", "r") as f:
    for line in f.readlines():
        parsed = orjson.loads(line)
        input = inputs[parsed["custom_id"]]
        outputs.append(
            {
                "text": input["body"]["input"][0],
                "vector": parsed["response"]["body"]["data"][0]["embedding"],
            }
        )

with open("generated/embeddings.json", "w") as f:
    f.write((orjson.dumps(outputs).decode("utf-8")))
