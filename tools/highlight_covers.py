#!/usr/bin/env python3
"""Instagram Story Highlight covers, 1080 x 1920, from the design tokens.

Usage: python tools/highlight_covers.py [out_dir]   (default out/highlights)
Instagram crops the centre into a circle, so each mark sits well inside the middle ~600px.
"""
import io
import json
import os
import sys

import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = {t["name"]: t["value"] for t in json.load(open(os.path.join(ROOT, "design", "tokens.json")))["color"]["tokens"]}


def hexc(name):
    v = TOK[name]
    v = v["light"] if isinstance(v, dict) else v
    return tuple(int(v.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def svg(path, w, h):
    png = cairosvg.svg2png(url=os.path.join(ROOT, "design", "svg", path), output_width=w, output_height=h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


COVERS = [  # file name, ground token, svg, (w, h)
    ("1-anak-pintar", "seri-pintar-bg", "seri-anak-pintar.svg", (380, 380)),
    ("2-mpasi", "seri-mpasi-bg", "seri-mpasi.svg", (380, 380)),
    ("3-main-di-rumah", "seri-main-bg", "seri-main-di-rumah.svg", (380, 380)),
    ("4-siap-sekolah", "seri-sekolah-bg", "seri-siap-sekolah.svg", (380, 380)),
    ("5-ayah-baru", "seri-ayah-bg", "seri-ayah-baru.svg", (380, 380)),
    ("6-ibu", "seri-ibu-bg", "seri-ibu.svg", (380, 380)),
    ("7-contekan", "surface-100", "tunas/tunas-riset.svg", (420, 490)),
]


def main(out):
    os.makedirs(out, exist_ok=True)
    for name, ground, mark, (w, h) in COVERS:
        img = Image.new("RGB", (1080, 1920), hexc(ground))
        m = svg(mark, w, h)
        img.paste(m, ((1080 - w) // 2, (1920 - h) // 2), m)
        img.save(os.path.join(out, f"highlight-{name}.jpg"), quality=94)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out", "highlights"))
