import base64
import os
from pathlib import Path

from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

print("API_KEY", API_KEY)

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

# Function to encode the image
def encode_image(image_path: os.PathLike) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


image_path = "image.jpg"

# Getting the base64 string
base64_image = encode_image(Path(image_path))

reqsponse = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What’s in this image? "
                            "Produce only semantic search terms which can be used to look for this image"
                            "Mention the objects, people, places, actions, activities, colors and text in the image."
                            "Recognise all the text to be able to search for it."
                            "Create terms in english and then in russian language."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
            ],
        },
    ],
    max_tokens=300,
)

print(reqsponse)