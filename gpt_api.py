import base64
import os
from io import BytesIO
from typing import Final

from openai import AsyncOpenAI

API_KEY: Final[str] = os.getenv("OPENAI_API_KEY")
OPEN_AI_CLIENT: Final[AsyncOpenAI] = AsyncOpenAI(api_key=API_KEY)


# Function to encode the image
def encode_image(data: BytesIO) -> str:
    return base64.b64encode(data.getbuffer()).decode('utf-8')


async def chat_gpt_description(data: BytesIO) -> str:
    # Getting the base64 string
    base64_image = encode_image(data)

    response = await OPEN_AI_CLIENT.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image? "
                                "Produce only semantic search terms which can be used to look for this image"
                                "Mention the objects, people, places, actions, activities, "
                                "colors and text in the image."
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

    return str(response.choices[0].message.content)
