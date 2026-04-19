import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def generate_door_image(door_title: str) -> Image.Image:
    prompts = {
        "Billy": "a weathered wooden door in the american wild west desert, 1970s film grain, dusty, cinematic, dark mood, photorealistic",
        "Vietnam": "a dark military bunker door, 1973 vietnam war era, foggy jungle, cinematic, film grain, melancholic, photorealistic",
        "Dylan": "a bohemian apartment door with protest posters, 1973 new york city, counterculture, gritty, film grain, photorealistic",
        "Survivor": "a collapsed concrete door in earthquake rubble, debris, dust, grey, mourning, cinematic, dark, photorealistic"
    }

    prompt = prompts["Billy"]
    for key in prompts:
        if key.lower() in door_title.lower():
            prompt = prompts[key]
            break

    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json={
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30
        }
    )

    if response.status_code != 200:
        print("Hata:", response.status_code, response.text[:200])
        return None

    data = response.json()
    image_data = data["artifacts"][0]["base64"]

    import base64
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    return image


if __name__ == "__main__":
    print("Görsel üretiliyor...")
    img = generate_door_image("Billy the Kid's Door")
    if img:
        img.save("test_door.png")
        print("test_door.png kaydedildi!")