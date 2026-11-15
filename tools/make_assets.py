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
    """Draw a fully extended hand inside its actual WFF image bounds.

    The clock's pivot is at base/h, and the blade stretches from the pivot
    to the tip. Oversample for anti-aliased diagonal edges.
    """
    z = 4
    im = Image.new("RGBA", (w * z, h * z), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    def point(x, y):
        return (round(x*z), round(y*z))
    x = w/2
    if name == "second":
        draw.line([point(x, 4), point(x, h-2)], fill=GREEN, width=round(w*.40*z))
        draw.ellipse([point(x-3,base-3),point(x+3,base+3)], fill=SOFT)
    else:
        # Metallic arrow, green inset, narrow tail behind center pivot.
        contour = [
            point(x, 3),
            point(x+w*.12, 8),
            point(x+w*.33, base*.65),
            point(x+w*.33, base+5),
            point(x+w*.14, h-3),
            point(x-w*.14, h-3),
            point(x-w*.33, base+5),
            point(x-w*.33, base*.65),
            point(x-w*.12, 8),
        ]
        draw.polygon(contour, fill=color)
        draw.line([point(x, 12), point(x, base-11)],
                  fill=GREEN, width=round(max(3, w*.14)*z))
        draw.line([point(x-w*.33,base*.67), point(x-w*.33,base+5)],
                  fill=(150,157,165,255), width=max(1,z//2))
    im.resize((w, h), Image.Resampling.LANCZOS).save(OUT / f"{name}.png")

hand("hour", 40, 100, 80, 0, (201, 209, 218, 255))
hand("minute", 24, 134, 121, 0, (226, 231, 239, 255))
hand("second", 8, 180, 155, 0, GREEN)
center = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
dc = ImageDraw.Draw(center)
dc.ellipse((2, 2, 38, 38), fill=(22, 25, 28, 255), outline=GREEN, width=5)
dc.ellipse((16, 16, 24, 24), fill=SOFT)
center.resize((20, 20), Image.Resampling.LANCZOS).save(OUT / "center.png")

# Preview is a static 10:10 example, with the same hands used at runtime.
thumb = back.resize((450, 450), Image.Resampling.LANCZOS)

def add_preview_hand(name, clockwise_angle, pivot_y):
    img = Image.open(OUT / f"{name}.png").convert("RGBA")
    w, h = img.size
    lay = Image.new("RGBA", (450,450), (0,0,0,0))
    lay.alpha_composite(img, (round(225-w/2), round(225-h*pivot_y)))
    lay = lay.rotate(-clockwise_angle, center=(225,225), resample=Image.Resampling.BICUBIC)
    thumb.alpha_composite(lay)

add_preview_hand("hour", 305, 0.8)
add_preview_hand("minute", 60, 0.903)
add_preview_hand("second", 210, 0.861)
thumb.alpha_composite(Image.open(OUT / "center.png").convert("RGBA"), (215,215))
# Keep the counter and single date readable even beneath crossed hands.
overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
p = ImageDraw.Draw(overlay)
p.text((S/2, 288), "ZBÝVÁ", font=font(47), fill=SOFT, anchor="mm")
p.text((S/2, 384), "80", font=font(143), fill=GREEN, anchor="mm")
p.text((S/2, 664), "15.11.2026", font=font(53, False), fill=SOFT, anchor="mm")
thumb.alpha_composite(overlay.resize((450,450), Image.Resampling.LANCZOS))
thumb.save(OUT / "preview.png")
print("Created:", ", ".join(p.name for p in OUT.glob("*.png")))
