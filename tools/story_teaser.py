#!/usr/bin/env python3
"""Instagram Story teasers (1080 x 1920) built from a post's already-rendered Instagram slides.

Usage: python tools/story_teaser.py stories/<batch>.json [out_dir]

Each story puts one approved slide in a frame on the series colour, with a series tag on top and two short
lines under it. Everything stays inside the Story safe zone (y 250 to 1670), clear of the profile bar
and the reply bar. Copy in the batch file goes through tools/lint_copy.py like any post.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import SERIES, color, font, svg_image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SW, SH = 1080, 1920
FRAME_W = 860
TOP, BOTTOM = 250, 1670


def ground_and_ink(series):
    if series == "contekan":
        return color("surface-100", "light"), color("ink", "light")
    return color(f"seri-{series}-bg", "light"), color(f"seri-{series}-ink", "light")


def centred(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((SW - w) / 2, y), text, font=f, fill=fill)


def story(item, out):
    series = item["series"]
    bg, ink = ground_and_ink(series)
    img = Image.new("RGB", (SW, SH), bg)
    d = ImageDraw.Draw(img)

    # tag: icon + label, centred
    if series == "contekan":
        label, icon = "CONTEKAN", svg_image("tunas/tunas-riset.svg", 60, 70)
    else:
        label, icon_name = SERIES[series]
        icon = svg_image(icon_name, 56)
    tf = font("body800", 34)
    tw = d.textlength(label, font=tf) + 4 * len(label)
    total = icon.width + 16 + tw
    x = (SW - total) / 2
    img.paste(icon, (int(x), TOP + 10 + (56 - icon.height) // 2), icon)
    cx = x + icon.width + 16
    for ch in label:
        d.text((cx, TOP + 18), ch, font=tf, fill=ink)
        cx += d.textlength(ch, font=tf) + 4

    # the slide, framed, with a soft shadow
    slide = Image.open(os.path.join(ROOT, "out", item["slug"] + "-ig", f"slide-{item.get('slide', 1)}.png")).convert("RGB")
    fh = round(slide.height * FRAME_W / slide.width)
    slide = slide.resize((FRAME_W, fh), Image.LANCZOS)
    fx, fy = (SW - FRAME_W) // 2, TOP + 110
    mask = Image.new("L", slide.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, FRAME_W, fh), radius=36, fill=255)
    sh = Image.new("L", (SW, SH), 0)
    ImageDraw.Draw(sh).rounded_rectangle((fx, fy + 14, fx + FRAME_W, fy + fh + 14), radius=36, fill=70)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    img.paste(Image.new("RGB", (SW, SH), tuple(int(c * 0.82) for c in bg)), (0, 0), sh)
    img.paste(slide, (fx, fy), mask)

    # two lines under the frame
    y = fy + fh + 44
    centred(d, y, item["line1"], font("display", 54), color("ink", "light"))
    y += 74
    centred(d, y, item["line2"], font("body700", 34), ink)
    if y + 44 > BOTTOM:
        raise SystemExit(f"{item['slug']}: text ends at {y + 44}px, past the safe zone ({BOTTOM}px)")

    name = f"story-{item['id']}.jpg"
    img.save(os.path.join(out, name), quality=92)
    return name


def main(batch, out):
    os.makedirs(out, exist_ok=True)
    spec = json.load(open(batch, encoding="utf-8"))
    for item in spec["stories"]:
        print(story(item, out))


if __name__ == "__main__":
    b = sys.argv[1]
    main(b, sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "out", "stories"))
