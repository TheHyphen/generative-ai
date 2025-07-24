import base64
import datetime
import os

from cv2 import VideoCapture, imwrite
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def capture_img():
    cam = VideoCapture(0)
    ret, frame = cam.read()

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    img_path = f"captured/{now}_captured_image.png"
    imwrite(img_path, frame)
    cam.release()

    return img_path


def convert_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(b64):
    r = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Lookup the visiting card and extract as much information as possible",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{b64}",
                    },
                ],
            }
        ],
    )
    return r.output_text


def main():
    img_path = capture_img()
    b64 = convert_to_b64(img_path)
    analysis = analyze_image(b64)
    print(analysis)


if __name__ == "__main__":
    main()
