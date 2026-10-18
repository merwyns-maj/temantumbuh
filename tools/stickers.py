#!/usr/bin/env python3
"""WhatsApp sticker pack from a spec: Tunas pose + a short line, with the white sticker outline.

Usage: python tools/stickers.py stickers/<pack>.json [out_dir]

WhatsApp rules this follows: 512 x 512 WebP with a transparent background, under 100 KB each,
3 to 30 stickers per pack, a 96 x 96 PNG tray icon, and up to 3 emoji per sticker (in the spec).
Writes sticker-<id>.webp, tray.png and preview.png (a contact sheet on krem for review).
"""
import io
import json
import os
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import color, font  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TUNAS = os.path.join(ROOT, "design", "svg", "tunas")
S = 512
PAD = 16          # room for the outline inside the canvas
OUTLINE = 12      # white sticker border


def pose(name, w, h):
    png = cairosvg.svg2png(url=os.path.join(TUNAS, name + ".svg"), output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def fit_lines(draw, text, maxw):
    """One line if it fits at 46px, else the most even two-line split, sized down to fit."""
    words = text.split()
    best = None
    for size in range(46, 29, -2):
        f = font("display", size)
        if draw.textlength(text, font=f) <= maxw:
            return [text], f
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            wa, wb = draw.textlength(a, font=f), draw.textlength(b, font=f)
            if max(wa, wb) <= maxw and (best is None or abs(wa - wb) < best[0]):
                best = (abs(wa - wb), [a, b])
        if best:
            return best[1], f
    raise SystemExit(f"'{text}' does not fit in two lines")


def sticker(item):
    bg, ink = color(f"seri-{item['series']}-bg", "light"), color(f"seri-{item['series']}-ink", "light")
    art = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(art)

    lines, f = fit_lines(d, item["label"], S - 2 * PAD - 2 * OUTLINE - 48)
    lh = int(f.size * 1.12)
    box_h = lh * len(lines) + 24
    box_w = max(d.textlength(l, font=f) for l in lines) + 48
    box_y1 = S - PAD - OUTLINE
    box_y0 = box_y1 - box_h

    # Tunas fills the space above the label and tucks in behind its top edge
    avail = box_y0 - PAD - OUTLINE + 18
    mh = min(avail, 380)
    mw = round(mh * 120 / 140)
    m = pose(item["pose"], mw, mh)
    art.alpha_composite(m, ((S - mw) // 2, PAD + OUTLINE + (avail - mh) // 2))

    bx0 = (S - box_w) / 2
    d.rounded_rectangle((bx0, box_y0, bx0 + box_w, box_y1), radius=26, fill=bg + (255,))
    y = box_y0 + 10
    for l in lines:
        w = d.textlength(l, font=f)
        d.text(((S - w) / 2, y), l, font=f, fill=ink)
        y += lh

    # white outline: grow the alpha, fill white, then the art on top
    a = art.split()[3].point(lambda v: 255 if v > 20 else 0)
    for _ in range(OUTLINE // 3):
        a = a.filter(ImageFilter.MaxFilter(7))
    a = a.filter(ImageFilter.GaussianBlur(1.2))
    out = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    out.putalpha(a)
    white = Image.new("RGBA", (S, S), (255, 255, 255, 255))
    out = Image.composite(white, out, a)
    out.alpha_composite(art)
    return out


def main(spec_path, out):
    os.makedirs(out, exist_ok=True)
    spec = json.load(open(spec_path, encoding="utf-8"))
    items = spec["stickers"]
    if not 3 <= len(items) <= 30:
        raise SystemExit("a pack needs 3 to 30 stickers")
    made = []
    for it in items:
        im = sticker(it)
        p = os.path.join(out, f"sticker-{it['id']}.webp")
        im.save(p, "WEBP", quality=88, method=6)
        kb = os.path.getsize(p) / 1024
        if kb > 100:
            raise SystemExit(f"{p} is {kb:.0f} KB, over WhatsApp's 100 KB")
        made.append(im)
    tray = pose("tunas-halo", 82, 96)
    t = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    t.alpha_composite(tray, (7, 0))
    t.save(os.path.join(out, "tray.png"))

    cols = 4
    rows = -(-len(made) // cols)
    sheet = Image.new("RGB", (cols * 270 + 10, rows * 270 + 10), color("surface-200", "light"))
    for i, im in enumerate(made):
        sheet.paste(im.resize((256, 256), Image.LANCZOS), (10 + (i % cols) * 270, 10 + (i // cols) * 270), im.resize((256, 256), Image.LANCZOS))
    sheet.save(os.path.join(out, "preview.png"))
    print(out, len(made), "stickers")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "out", "stickers"))
