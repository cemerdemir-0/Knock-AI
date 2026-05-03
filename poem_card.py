from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os


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


def create_poem_card(door_title, poem_lines):
    width, height = 800, 600

    themes = {
        "Billy":    (210, 180, 140),
        "Vietnam":  (160, 175, 155),
        "Dylan":    (200, 185, 160),
        "Survivor": (185, 185, 195),
    }

    bg_color = themes["Billy"]
    for key in themes:
        if key.lower() in door_title.lower():
            bg_color = themes[key]
            break

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Parchment texture
    for _ in range(2000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(0, 40)
        dark = tuple(max(0, c - r) for c in bg_color)
        draw.point((x, y), fill=dark)

    # Border frames
    for i in range(3):
        draw.rectangle(
            [20 + i * 4, 20 + i * 4, width - 20 - i * 4, height - 20 - i * 4],
            outline=(101, 67, 33),
            width=1,
        )

    # Decorative lines
    draw.line([(60, 80), (width - 60, 80)], fill=(101, 67, 33), width=2)
    draw.line([(60, 85), (width - 60, 85)], fill=(101, 67, 33), width=1)
    draw.line([(60, height - 80), (width - 60, height - 80)], fill=(101, 67, 33), width=1)
    draw.line([(60, height - 85), (width - 60, height - 85)], fill=(101, 67, 33), width=2)

    font_title = _load_font(32)
    font_poem  = _load_font(22)
    font_footer = _load_font(18)

    # Title
    draw.text((width // 2, 50), door_title,
              fill=(60, 30, 10), anchor="mm", font=font_title)

    # Poem lines
    y_start = 150
    line_height = 55
    for line in poem_lines:
        draw.text((width // 2, y_start), line,
                  fill=(40, 20, 5), anchor="mm", font=font_poem)
        y_start += line_height

    # Footer
    draw.text((width // 2, height - 50), "— 1973 —",
              fill=(101, 67, 33), anchor="mm", font=font_footer)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    return img


if __name__ == "__main__":
    img = create_poem_card(
        "Billy the Kid's Door",
        [
            "The dust is kickin' up behind,",
            "Leavin' shadows where I been.",
            "Nowhere to run, nowhere to hide,",
            "Just the wind and a brand new sin.",
        ],
    )
    img.save("test_card.png")
    print("test_card.png kaydedildi!")
