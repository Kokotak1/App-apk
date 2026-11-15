#!/usr/bin/env python3
"""Generate small, clean PNG assets for the resource-only WFF watch face.
Requires Pillow. This script intentionally avoids copied logos and fonts.
"""
from pathlib import Path
from math import cos, sin, radians
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "watchface/src/main/res/drawable"
OUT.mkdir(parents=True, exist_ok=True)
S = 900
SC = S / 450
GREEN = (67, 255, 17, 255)
SOFT = (245, 245, 250, 255)
GRAY = (130, 138, 151, 255)


def font(size, bold=True):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size)


def xy(r, degrees):
    a = radians(degrees - 90)
    return (S / 2 + r * cos(a), S / 2 + r * sin(a))

back = Image.new("RGBA", (S, S), (0, 0, 0, 255))
d = ImageDraw.Draw(back)
# Matte black dial with glowing marker ring
for i in range(80):
    a = i * 360 / 80
    p1, p2 = xy(370, a + 1), xy(387, a + 1)
    d.line((p1, p2), fill=GREEN, width=8)
for i in range(60):
    a = i * 6
    p1 = xy(336 if i % 5 else 326, a)
    p2 = xy(352, a)
    d.line((p1, p2), fill=SOFT if i % 5 == 0 else GRAY, width=5 if i % 5 == 0 else 2)
# Hour numerals set near cardinal points
numeral = font(88)
for label, x, y in [("12", S / 2, 155), ("3", 755, S / 2),
                    ("6", S / 2, 733), ("9", 143, S / 2)]:
    d.text((x, y), label, font=numeral, fill=SOFT, anchor="mm")
back.save(OUT / "background.png")


def hand(name, w, h, base, tip, color):
    im = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx = im.width // 2
    # Polygon's upper point is toward 12; large bottom portion anchors it.
    draw.polygon([(cx, 4), (cx + w, h), (cx + w // 2, base),
                  (cx - w // 2, base), (cx - w, h)],
                 fill=color)
    draw.line([(cx, 15), (cx, base - 5)], fill=GREEN, width=max(3, w // 2))
    im.resize((w, h), Image.Resampling.LANCZOS).save(OUT / f"{name}.png")

hand("hour", 40, 100, 80, 0, (201, 209, 218, 255))
hand("minute", 24, 134, 121, 0, (226, 231, 239, 255))
hand("second", 8, 180, 155, 0, GREEN)
center = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
dc = ImageDraw.Draw(center)
dc.ellipse((2, 2, 38, 38), fill=(22, 25, 28, 255), outline=GREEN, width=5)
dc.ellipse((16, 16, 24, 24), fill=SOFT)
center.resize((20, 20), Image.Resampling.LANCZOS).save(OUT / "center.png")

# Preview, distinct from live runtime: label, initial count, date, static hands.
prev = back.copy()
p = ImageDraw.Draw(prev)
p.text((S/2, 288), "ZBÝVÁ", font=font(47), fill=SOFT, anchor="mm")
p.text((S/2, 384), "80", font=font(143), fill=GREEN, anchor="mm")
p.text((S/2, 664), "15.11.2026", font=font(53, False), fill=SOFT, anchor="mm")
prev.resize((450, 450), Image.Resampling.LANCZOS).save(OUT / "preview.png")
print("Created:", ", ".join(p.name for p in OUT.glob("*.png")))
