from datasets import load_dataset

ds = load_dataset("stanfordnlp/coqa")
# { "messsages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hello!"}] }


def format_row(row):
    result = []
    result.append(
        {
            "role": "system",
            "content": "look at this story and answer questions based on the infromation in the story: {}".format(
                row["story"]
            ),
        }
    )
    for idx, question in enumerate(row["questions"]):
        answer = row["answers"]["input_text"][idx]
        result.append({"role": "user", "content": question})
        result.append({"role": "assistant", "content": answer})
    return {"messages": result}


ds["train"].map(
    format_row, remove_columns=["source", "story", "questions", "answers"]
).to_json("generated/fine-tuning.jsonl")
