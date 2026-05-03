import requests
import base64
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\georgia.ttf",
    r"C:\Windows\Fonts\Georgia.ttf",
    r"C:\Windows\Fonts\GEORGIA.TTF",
    r"C:\Windows\Fonts\times.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
]

def _load_font(size):
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_door_image(door_title):
    prompts = {
        "Billy":    "a weathered wooden saloon door in the american wild west at dusk, 1970s film grain, dusty amber light, cinematic, dark mood, photorealistic, dramatic shadows",
        "Vietnam":  "a heavy military bunker door in a foggy jungle, 1973 vietnam war era, green-grey tones, cinematic film grain, melancholic, photorealistic, mist and darkness",
        "Dylan":    "a bohemian apartment door covered in protest posters and handwritten notes, 1973 new york city greenwich village, warm lamplight, counterculture gritty, film grain, photorealistic",
        "Survivor": "a cracked concrete doorway standing alone in earthquake rubble at dawn, debris and dust, cold grey light, mourning and silence, cinematic, dark, photorealistic",
    }
    negative = "text, watermark, cartoon, painting, illustration, bright colors, daytime, cheerful"

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
            "Accept": "application/json",
        },
        json={
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative, "weight": -1},
            ],
            "cfg_scale": 8,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 35,
        },
    )

    if response.status_code != 200:
        print("Hata:", response.status_code, response.text[:200])
        return None

    data = response.json()
    image_data = data["artifacts"][0]["base64"]
    return Image.open(BytesIO(base64.b64decode(image_data)))


def overlay_poem_on_image(image, poem_lines):
    """Kapı gorselinin altina yari-saydam gradient + siir satirlari ekler."""
    if not poem_lines:
        return image

    img = image.copy().convert("RGBA")
    width, height = img.size

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    gradient_top = int(height * 0.52)
    for y in range(gradient_top, height):
        progress = (y - gradient_top) / (height - gradient_top)
        alpha = int(215 * (progress ** 0.7))
        draw_overlay.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    font_poem = _load_font(34)
    font_small = _load_font(20)

    line_height = 50
    poem_block_height = len(poem_lines) * line_height + 55
    y_pos = height - poem_block_height

    for line in poem_lines:
        draw.text((width // 2 + 2, y_pos + 2), line,
                  fill=(0, 0, 0, 150), anchor="mm", font=font_poem)
        draw.text((width // 2, y_pos), line,
                  fill=(240, 215, 155, 235), anchor="mm", font=font_poem)
        y_pos += line_height

    draw.text((width // 2, height - 24), "— 1973 —",
              fill=(160, 130, 80, 180), anchor="mm", font=font_small)

    return img.convert("RGB")


if __name__ == "__main__":
    print("Gorsel uretiliyor...")
    img = generate_door_image("Billy the Kid's Door")
    if img:
        lines = [
            "The dust is kickin' up behind,",
            "Leavin' shadows where I been.",
            "Nowhere to run, nowhere to hide,",
            "Just the wind and a brand new sin.",
        ]
        overlay_poem_on_image(img, lines).save("test_door_overlay.png")
        print("test_door_overlay.png kaydedildi!")
