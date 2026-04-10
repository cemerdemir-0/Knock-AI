from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_door_image(door_title: str) -> Image.Image:
    prompts = {
        "Billy": "a weathered wooden door in the american wild west desert, 1970s film grain, dusty, cinematic, dark mood, photorealistic",
        "Vietnam": "a dark military bunker door, 1973 vietnam war era, foggy jungle, cinematic, film grain, melancholic, photorealistic",
        "Dylan": "a bohemian apartment door with protest posters, 1973 new york city, counterculture, gritty, film grain, photorealistic"
    }

    prompt = prompts["Billy"]
    for key in prompts:
        if key.lower() in door_title.lower():
            prompt = prompts[key]
            break

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"]
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            return image

    return None


if __name__ == "__main__":
    print("Görsel üretiliyor...")
    img = generate_door_image("Billy the Kid's Door")
    if img:
        img.save("test_door.png")
        print("test_door.png kaydedildi!")
    else:
        print("Görsel üretilemedi.")