# from datasets import load_dataset

# # ds = load_dataset("stanfordnlp/coqa")

# # vds = ds["validation"]

# # svds = vds.select(range(20))


# # def format_row(row):
# #     result = []
# #     result.append(
# #         {
# #             "role": "system",
# #             "content": "look at this story and answer questions based on the infromation in the story: {}".format(
# #                 row["story"]
# #             ),
# #         }
# #     )
# #     for idx, question in enumerate(row["questions"]):
# #         answer = row["answers"]["input_text"][idx]
# #         result.append({"role": "user", "content": question})
# #         result.append({"role": "assistant", "content": answer})
# #     return {"messages": result}


# # svds.map(
# #     format_row, remove_columns=["source", "story", "questions", "answers"]
# # ).to_json("generated/fine-tuning-eval.jsonl")


import json

# import dotenv
# from together import Together
# dotenv.load_dotenv()
# with open("generated/fine-tuning-eval.jsonl", "r") as f:
#     lines = f.readlines()
#     data = [json.loads(line) for line in lines]
# client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
# result = []
# for index, item in enumerate(data):
#     orignal_answer = item["messages"][2]["content"]
#     input = item["messages"][:2]
#     fine_tuned_response = client.chat.completions.create(
#         model="mdfaizuddin15_d4a7/Meta-Llama-3.1-8B-Instruct-Reference-4000fd27",
#         messages=input,
#     )
#     fine_tuned_answer = fine_tuned_response.choices[0].message.content
#     base_response = client.chat.completions.create(
#         model="meta-llama/Llama-3-8b-chat-hf",
#         messages=input,
#     )
#     base_answer = base_response.choices[0].message.content
#     print(f"Done: {index}")
#     result.append(
#         {
#             "original_answer": orignal_answer,
#             "fine_tuned_answer": fine_tuned_answer,
#             "base_answer": base_answer,
#             "input": input,
#         }
#     )
# with open("generated/fine-tuning-eval-results.jsonl", "w") as f:
#     f.write(json.dumps(result))
import transformers.data.metrics.squad_metrics as squad_metrics


def get_metrics(original_answers, answers):
    f1_metrics = []

    for original, answer in zip(original_answers, answers):
        f1_metrics.append(squad_metrics.compute_f1(original, answer))

    return sum(f1_metrics) / len(f1_metrics)


with open("generated/fine-tuning-eval-results.jsonl", "r") as f:
    input_data = json.loads(f.read())

    base_answers = [item["base_answer"] for item in input_data]
    fine_tuned_answers = [item["fine_tuned_answer"] for item in input_data]
    original_answers = [item["original_answer"] for item in input_data]

    base_metrics = get_metrics(original_answers, base_answers)
    fine_tuned_metrics = get_metrics(original_answers, fine_tuned_answers)

    print(f"Base Model Metrics: F1={base_metrics}")
    print(f"Fine-Tuned Model Metrics: F1={fine_tuned_metrics}")
