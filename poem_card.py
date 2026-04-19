from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os


def create_poem_card(door_title: str, poem_lines: list) -> Image.Image:
    # Boyut
    width, height = 800, 600

    # Arka plan rengi - kapıya göre
    themes = {
        "Billy": (210, 180, 140),  # Kum rengi
        "Vietnam": (180, 190, 170),  # Soluk yeşil
        "Dylan": (200, 185, 170),  # Soluk kahve
        "Survivor": (190, 190, 190),  # Gri
    }

    bg_color = themes["Billy"]
    for key in themes:
        if key.lower() in door_title.lower():
            bg_color = themes[key]
            break

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Parşömen dokusu - rastgele lekeler
    import random
    for _ in range(2000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(0, 40)
        dark = tuple(max(0, c - r) for c in bg_color)
        draw.point((x, y), fill=dark)

    # Kenar çerçevesi
    for i in range(3):
        draw.rectangle(
            [20 + i * 4, 20 + i * 4, width - 20 - i * 4, height - 20 - i * 4],
            outline=(101, 67, 33),
            width=1
        )

    # Üst süsleme çizgisi
    draw.line([(60, 80), (width - 60, 80)], fill=(101, 67, 33), width=2)
    draw.line([(60, 85), (width - 60, 85)], fill=(101, 67, 33), width=1)

    # Alt süsleme çizgisi
    draw.line([(60, height - 80), (width - 60, height - 80)], fill=(101, 67, 33), width=1)
    draw.line([(60, height - 85), (width - 60, height - 85)], fill=(101, 67, 33), width=2)

    # Başlık
    draw.text((width // 2, 50), door_title, fill=(60, 30, 10), anchor="mm")

    # Şiir satırları
    y_start = 140
    line_height = 60
    for line in poem_lines:
        draw.text((width // 2, y_start), line, fill=(40, 20, 5), anchor="mm")
        y_start += line_height

    # Alt bilgi
    draw.text((width // 2, height - 50), "— 1973 —", fill=(101, 67, 33), anchor="mm")

    # Hafif blur - eski kağıt hissi
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    return img


if __name__ == "__main__":
    img = create_poem_card(
        "Billy the Kid's Door",
        [
            "The dust is kickin' up behind,",
            "Leavin' shadows where I been.",
            "Nowhere to run, nowhere to hide,",
            "Just the wind and a brand new sin."
        ]
    )
    img.save("test_card.png")
    print("test_card.png kaydedildi!")