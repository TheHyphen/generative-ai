import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

chats_dir = "chats"


def retrieve_chat():
    # read files list
    files = os.listdir(chats_dir)
    print("Existing chats:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    choice = int(input("Choose a chat: ")) - 1
    file = open(chats_dir + "/" + files[choice], "r")
    history = json.loads(file.read())
    file.close()
    chat_id = files[choice].split(".")[0]
    return chat_id, history


def save_chat(chat_id, history):
    file = open(chats_dir + "/" + chat_id + ".json", "w")
    file.write(json.dumps(history))
    file.close()


def main():
    client = OpenAI(api_key=key)
    history = []
    choose_existing = input("Choose an existing chat? Y/n")
    if choose_existing == "Y":
        chat_id, history = retrieve_chat()

    while True:
        prompt = input("User: ")
        if prompt == "exit":
            break
        history.append({"role": "user", "content": prompt})
        r = client.responses.create(
            model="gpt-4o",
            input=history,
            instructions="Use a lot of emojis in your responses",
        )
        print(f"Assistant: {r.output_text}")
        history.append({"role": "assistant", "content": r.output_text})

    save_chat(chat_id, history)


if __name__ == "__main__":
    main()
