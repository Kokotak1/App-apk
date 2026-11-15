#!/usr/bin/env python3
"""Prepare the approved Pip-Boy artwork, live hands, and low-power AOD assets."""
from pathlib import Path
from io import BytesIO
from math import radians, sin, cos
import base64
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "watchface/src/main/res/drawable"
OUT.mkdir(parents=True, exist_ok=True)
S = 450
RED = (255, 25, 25, 255)
GREEN = (40, 242, 40, 255)
SILVER = (236, 241, 245, 255)

def font(sz, bold=False):
    fam = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + fam, sz)

src = ROOT / "tools/pipboy_bg.b64"
art = Image.open(BytesIO(base64.b64decode(src.read_text().strip()))).convert("RGB")
# Calibrate the source artwork to the physical screen. The neon outer ring
# was measured at (221.5, 219.0) in the source 450x450 image, whereas WFF
# places the clock hands at (225, 225). Shift and enlarge the whole scene
# together so the printed dial and rotating hands have a common center.
SOURCE_CENTER = (221.5, 219.0)
TARGET_CENTER = (S / 2, S / 2)
DIAL_SCALE = 1.04  # leaves a small safety margin inside the round screen
art = art.resize((S, S), Image.Resampling.LANCZOS)
inverse_scale = 1.0 / DIAL_SCALE
art = art.transform(
    (S, S),
    Image.Transform.AFFINE,
    (
        inverse_scale, 0,
        SOURCE_CENTER[0] - TARGET_CENTER[0] * inverse_scale,
        0, inverse_scale,
        SOURCE_CENTER[1] - TARGET_CENTER[1] * inverse_scale,
    ),
    resample=Image.Resampling.BICUBIC,
    fillcolor=(0, 0, 0),
)
art.save(OUT / "background.png", optimize=True)

# Always-on display: dark background with sparse neutral markings.
aod = Image.new("RGBA", (S, S), (0, 0, 0, 255))
d = ImageDraw.Draw(aod)
for i in range(12):
    a = radians(i * 30 - 90)
    r1, r2 = (187, 203) if i % 3 == 0 else (194, 202)
    x1, y1 = 225+r1*cos(a), 225+r1*sin(a)
    x2, y2 = 225+r2*cos(a), 225+r2*sin(a)
    d.line((x1,y1,x2,y2), fill=(82,84,84,255) if i%3 == 0 else (46,49,49,255), width=3 if i%3 == 0 else 2)
d.text((225, 82), "12", fill=(100,100,100,255), font=font(35, True), anchor="mm")
d.text((391,225), "3", fill=(95,95,95,255), font=font(29,True), anchor="mm")
d.text((225,384), "6", fill=(95,95,95,255), font=font(29,True), anchor="mm")
d.text((60,225), "9", fill=(95,95,95,255), font=font(29,True), anchor="mm")
aod.save(OUT / "aod_background.png", optimize=True)

def hand(name, w, h, base, color, accent=None):
    """Oversampled industrial blades: sculpted silver edges and a wide neon inset."""
    z = 6
    im = Image.new("RGBA", (w*z, h*z), (0,0,0,0))
    cx = w/2
    def coords(points, dx=0, dy=0):
        return [(round((x+dx)*z), round((y+dy)*z)) for x,y in points]
    d = ImageDraw.Draw(im)
    if name == "second":
        d.line(coords([(cx,5),(cx,h-5)]), fill=(5,36,8,245), width=round(4.6*z))
        d.line(coords([(cx,5),(cx,h-5)]), fill=GREEN, width=round(2.9*z))
        d.ellipse((round((cx-3.3)*z),round((base-3.3)*z),
                   round((cx+3.3)*z),round((base+3.3)*z)),fill=SILVER)
    else:
        # Sword-shaped silhouette. Unlike the previous 26px hand,
        # the blade's actual width is roughly 60% of its image.
        outline = [(cx,3),
                   (cx+w*.115,16),
                   (cx+w*.335,base*.37),
                   (cx+w*.335,base*.78),
                   (cx+w*.285,base+6),
                   (cx+w*.10,h-4),
                   (cx-w*.10,h-4),
                   (cx-w*.285,base+6),
                   (cx-w*.335,base*.78),
                   (cx-w*.335,base*.37),
                   (cx-w*.115,16)]
        d.polygon(coords(outline,1.0,2.0),fill=(0,0,0,140))
        d.polygon(coords(outline),fill=(25,31,33,255))
        metal = [(cx,6),
                 (cx+w*.105,18),
                 (cx+w*.30,base*.39),
                 (cx+w*.30,base*.77),
                 (cx+w*.255,base+4),
                 (cx+w*.075,h-7),
                 (cx-w*.075,h-7),
                 (cx-w*.255,base+4),
                 (cx-w*.30,base*.77),
                 (cx-w*.30,base*.39),
                 (cx-w*.105,18)]
        d.polygon(coords(metal),fill=(207,218,228,255))
        # Raised polished edges and dark recessed central slot.
        d.line(coords([(cx-w*.105,18),(cx-w*.30,base*.39),
                       (cx-w*.30,base*.77),(cx-w*.255,base+4)]),
               fill=(250,252,253,255),width=round(2.7*z),joint="curve")
        d.line(coords([(cx+w*.105,18),(cx+w*.30,base*.39),
                       (cx+w*.30,base*.77),(cx+w*.255,base+4)]),
               fill=(91,103,117,255),width=round(2.5*z),joint="curve")
        inset = [(cx,24),
                 (cx+w*.07,29),
                 (cx+w*.19,base*.43),
                 (cx+w*.19,base*.73),
                 (cx+w*.12,base-13),
                 (cx-w*.12,base-13),
                 (cx-w*.19,base*.73),
                 (cx-w*.19,base*.43),
                 (cx-w*.07,29)]
        d.polygon(coords(inset),fill=(4,23,9,255))
        glow = [(cx,28),
                (cx+w*.055,33),
                (cx+w*.155,base*.44),
                (cx+w*.155,base*.70),
                (cx+w*.10,base-17),
                (cx-w*.10,base-17),
                (cx-w*.155,base*.70),
                (cx-w*.155,base*.44),
                (cx-w*.055,33)]
        d.polygon(coords(glow),fill=(32,236,44,255))
        d.line(coords([(cx-w*.055,35),(cx-w*.14,base*.45),
                       (cx-w*.14,base*.69)]), fill=(174,255,158,245),
               width=round(1.8*z),joint="curve")
        # Short gunmetal tail behind the pivot.
        d.line(coords([(cx,base+8),(cx,h-8)]),
               fill=(65,76,82,255), width=round(4*z))
    im.resize((w,h), Image.Resampling.LANCZOS).save(OUT / (name+".png"))

# Full metal blades, not the hairline hands from the previous APK.
# The minute tip is 165px from center, safely inside the ~190px green ring.
hand("hour",56,173,149,SILVER,GREEN)
hand("minute",46,190,168,SILVER,GREEN)
hand("second",8,218,200,GREEN)
pivot=Image.new("RGBA",(20,20),(0,0,0,0))
dc=ImageDraw.Draw(pivot)
dc.ellipse((1,1,19,19),fill=(120,128,133,255),outline=(223,231,236,255),width=3)
dc.ellipse((8,8,12,12),fill=GREEN)
pivot.save(OUT / "center.png")

# Preview is illustrative; the WFF clock, count, and date remain live.
preview=art.copy()
dp=ImageDraw.Draw(preview)
dp.text((171,157),"80",font=font(70,True),fill=RED,anchor="mm",
        stroke_width=1,stroke_fill=(80,0,0))
dp.text((222,319),"18.11.2026",font=font(21),fill=(245,245,245),anchor="mm")
preview.save(OUT / "preview.png",optimize=True)
print("Generated Pip-Boy background, AOD background, hands and preview")
