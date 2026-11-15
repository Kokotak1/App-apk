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
# Photo calibration (15 Nov 2026): the green dial center was at x~422.5
# but the physical bezel center at x~415 on the photographed watch.
# Compensate with a left shift of 9 WFF units, applying the same correction
# to dial artwork, AOD, all three hands, center cap, live count and date.
SOURCE_CENTER = (221.5, 219.0)
TARGET_CENTER = (S / 2 - 9, S / 2)  # -9px x correction, measured from real watch photo
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
    x1, y1 = 216+r1*cos(a), 225+r1*sin(a)
    x2, y2 = 216+r2*cos(a), 225+r2*sin(a)
    d.line((x1,y1,x2,y2), fill=(82,84,84,255) if i%3 == 0 else (46,49,49,255), width=3 if i%3 == 0 else 2)
d.text((216, 82), "12", fill=(100,100,100,255), font=font(35, True), anchor="mm")
d.text((382,225), "3", fill=(95,95,95,255), font=font(29,True), anchor="mm")
d.text((216,384), "6", fill=(95,95,95,255), font=font(29,True), anchor="mm")
d.text((51,225), "9", fill=(95,95,95,255), font=font(29,True), anchor="mm")
aod.save(OUT / "aod_background.png", optimize=True)

def hand(name, w, h, base):
    """Slim, elongated, tapered instrument hands; all pivots at x=216,y=225."""
    z = 6  # antialias at 6x resolution
    im = Image.new("RGBA", (w*z, h*z), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w / 2
    def poly(points):
        return [(round(x*z), round(y*z)) for x,y in points]
    if name == "second":
        d.line(poly([(cx,5),(cx,h-7)]),fill=(6,40,12,240),width=round(4*z))
        d.line(poly([(cx,5),(cx,h-7)]),fill=(24,233,42,255),width=round(2*z))
    else:
        # Thin sword profile, capped around 15-19 px wide at its widest.
        outer=[
            (cx,3), (cx+w*.09,12), (cx+w*.31,base*.54),
            (cx+w*.28,base*.78), (cx+w*.19,base+5),
            (cx+w*.11,h-5), (cx-w*.11,h-5),
            (cx-w*.19,base+5), (cx-w*.28,base*.78),
            (cx-w*.31,base*.54), (cx-w*.09,12)]
        d.polygon(poly([(x+0.7,y+1.3) for x,y in outer]),fill=(0,0,0,130))
        d.polygon(poly(outer),fill=(228,235,239,255))
        # Narrow green central channel; the silver edge remains readable.
        core=[
            (cx,17), (cx+w*.052,22), (cx+w*.17,base*.55),
            (cx+w*.13,base*.77), (cx+w*.07,base-8),
            (cx-w*.07,base-8), (cx-w*.13,base*.77),
            (cx-w*.17,base*.55), (cx-w*.052,22)]
        d.polygon(poly(core),fill=(8,36,15,255))
        glow=[
            (cx,22), (cx+w*.036,27), (cx+w*.12,base*.56),
            (cx+w*.095,base*.76), (cx+w*.035,base-12),
            (cx-w*.035,base-12), (cx-w*.095,base*.76),
            (cx-w*.12,base*.56), (cx-w*.036,27)]
        d.polygon(poly(glow),fill=(25,236,45,255))
        d.line(poly([(cx-w*.24,base*.58),(cx-w*.21,base*.77)]),
               fill=(255,255,255,235),width=round(1.6*z))
        # Only a short visible tail behind the central bearing.
        d.line(poly([(cx,base+7),(cx,h-6)]),
               fill=(101,113,119,255),width=round(2.8*z))
    im.resize((w,h),Image.Resampling.LANCZOS).save(OUT / (name + ".png"))

# Common mechanical pivot, left-shifted together with the photographed dial:
# hour 75+150=225; minute 47+178=225; second 35+190=225.
hand("hour",30,174,150)
hand("minute",24,194,178)
hand("second",6,213,190)
pivot=Image.new("RGBA",(16,16),(0,0,0,0))
dc=ImageDraw.Draw(pivot)
dc.ellipse((1,1,15,15),fill=(123,134,140,255),outline=(235,243,246,255),width=2)
dc.ellipse((6,6,10,10),fill=(32,235,44,255))
pivot.save(OUT / "center.png")

# Preview is illustrative; the WFF clock, count, and date remain live.
preview=art.copy()
dp=ImageDraw.Draw(preview)
dp.text((162,157),"80",font=font(70,True),fill=RED,anchor="mm",
        stroke_width=1,stroke_fill=(80,0,0))
dp.text((213,319),"18.11.2026",font=font(21),fill=(245,245,245),anchor="mm")
# Simulated 14:15:30 preview: same images, angles and center as runtime.
# Text is drawn afterward just as the live WFF text overlays the hands.
for name, x, y, clockwise in [
    ("hour", 201, 75, 67.5),
    ("minute", 204, 47, 90.0),
    ("second", 213, 35, 180.0),
]:
    hand_img = Image.open(OUT / (name + ".png")).convert("RGBA")
    layer = Image.new("RGBA",(S,S),(0,0,0,0))
    layer.alpha_composite(hand_img,(x,y))
    preview=Image.alpha_composite(
        preview.convert("RGBA"),
        layer.rotate(-clockwise,resample=Image.Resampling.BICUBIC,center=(216,225)))
preview.alpha_composite(Image.open(OUT / "center.png").convert("RGBA"),(208,217))
# Last: live counter + date, corresponding to the WFF layer order.
dp=ImageDraw.Draw(preview)
dp.text((162,157),"80",font=font(70,True),fill=RED,anchor="mm",
        stroke_width=1,stroke_fill=(80,0,0))
dp.text((213,319),"18.11.2026",font=font(21),fill=(245,245,245),anchor="mm")
preview.save(OUT / "preview.png",optimize=True)
print("Generated Pip-Boy background, AOD background, hands and preview")
