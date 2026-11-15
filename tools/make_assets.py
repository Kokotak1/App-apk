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
art = art.resize((S, S), Image.Resampling.LANCZOS)
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
    z=4
    im=Image.new("RGBA", (w*z,h*z),(0,0,0,0))
    draw=ImageDraw.Draw(im)
    p=lambda x,y:(round(x*z),round(y*z))
    cx=w/2
    if name=="second":
        draw.line((p(cx,3),p(cx,h-3)),fill=GREEN,width=max(4,int(w*.4*z)))
    else:
        draw.polygon([p(cx,2),p(cx+w*.14,9),p(cx+w*.34,base*.69),
                      p(cx+w*.34,base+4),p(cx+w*.12,h-3),
                      p(cx-w*.12,h-3),p(cx-w*.34,base+4),
                      p(cx-w*.34,base*.69),p(cx-w*.14,9)],fill=color)
        if accent:
            draw.line((p(cx,13),p(cx,base-15)),fill=accent,width=max(3,int(w*.14*z)))
    im.resize((w,h), Image.Resampling.LANCZOS).save(OUT / (name+".png"))

hand("hour",40,100,80,SILVER,(75,230,71,255))
hand("minute",24,134,121,SILVER,(75,230,71,255))
hand("second",8,180,155,GREEN)
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
