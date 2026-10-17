#!/usr/bin/env python3
"""Build a phone-friendly review PDF: one landscape page per post with slides, score, job and caption.

Usage: python tools/review_sheet.py out/review.pdf posts/d01-*.json posts/d02-*.json ...
Run render.py first so out/<slug>/slide-N.png exist.
"""
import io
import json
import os
import sys

from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from score_post import machine, judged  # noqa: E402

W, H = landscape(A4)
INK, MUTED, SAGE, TERRA, CREAM = (0.29, 0.25, 0.21), (0.48, 0.42, 0.37), (0.25, 0.42, 0.32), (0.77, 0.38, 0.25), (0.98, 0.96, 0.92)
JOB = {"send": "DIKIRIM / DI-TAG", "save": "DISIMPAN", "comment": "DIKOMENTARI"}
SERIES = {"pintar": "Seri Anak Pintar", "mpasi": "Seri MPASI", "main": "Seri Main di Rumah",
          "sekolah": "Seri Siap Sekolah", "ayah": "Seri Ayah Baru"}


def font_setup():
    # DejaVu covers Bahasa Indonesia and punctuation; emoji in captions are stripped for the PDF.
    pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def grid(slug):
    d = os.path.join(ROOT, "out", slug)
    files = sorted((f for f in os.listdir(d) if f.startswith("slide-")), key=lambda f: int(f[6:-4]))
    tw, th, g, cols = 300, 400, 16, 5
    rows = (len(files) + cols - 1) // cols
    img = Image.new("RGB", (cols * tw + (cols + 1) * g, rows * th + (rows + 1) * g), (236, 228, 216))
    for i, f in enumerate(files):
        im = Image.open(os.path.join(d, f)).convert("RGB").resize((tw, th), Image.LANCZOS)
        img.paste(im, (g + (i % cols) * (tw + g), g + (i // cols) * (th + g)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    buf.seek(0)
    return ImageReader(buf), img.size


def wrap(c, text, fname, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, fname, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def strip_emoji(s):
    return "".join(ch for ch in s if ord(ch) < 0x2190 or 0x2E80 <= ord(ch) < 0x1F000 and ord(ch) not in range(0x2600, 0x2800))


def main(out, paths):
    font_setup()
    cal = json.load(open(os.path.join(ROOT, "posts", "calendar.json"), encoding="utf-8"))
    bydate = {d["slug"]: d for d in cal["days"]}
    jpath = os.path.join(ROOT, "data", "judged.json")
    table = json.load(open(jpath, encoding="utf-8")) if os.path.exists(jpath) else {}
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("TemanTumbuh: review konten")
    for p in paths:
        spec = json.load(open(p, encoding="utf-8"))
        slug = os.path.splitext(os.path.basename(p))[0]
        cal_row = bydate.get(slug, {})
        m, notes = machine(spec)
        jd, jnote = judged(slug, table)
        total = m + (jd or 0)
        c.setFillColorRGB(*CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # header
        c.setFillColorRGB(*MUTED)
        c.setFont("DV", 10)
        c.drawString(28, H - 30, f"Hari {cal_row.get('day', '?')}  ·  {cal_row.get('date', '')}  ·  {SERIES.get(spec['series'], spec['series'])}  ·  19:00 WIB")
        c.setFillColorRGB(*INK)
        c.setFont("DVB", 17)
        c.drawString(28, H - 52, cal_row.get("title", slug))
        # score badge
        verdict = "PRIORITAS" if total >= 90 else "REVIEW" if total >= 70 else "TULIS ULANG"
        col = SAGE if total >= 90 else (0.55, 0.45, 0.2) if total >= 70 else TERRA
        c.setFillColorRGB(*col)
        c.roundRect(W - 288, H - 62, 260, 40, 10, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("DVB", 15)
        c.drawCentredString(W - 158, H - 40, f"{total:.0f}/100  {verdict}")
        c.setFont("DV", 8)
        c.drawCentredString(W - 158, H - 54, f"mesin {m}/40 · nilai {jd or 0:.0f}/60 · tugas: {JOB.get(spec.get('job'), '-')}")
        # slides grid
        reader, (iw, ih) = grid(slug)
        gw = W - 56
        gh = gw * ih / iw
        top = H - 74
        c.drawImage(reader, 28, top - gh, width=gw, height=gh)
        # notes + caption
        y = top - gh - 18
        c.setFillColorRGB(*INK)
        c.setFont("DVB", 9.5)
        c.drawString(28, y, "Catatan:")
        c.setFont("DV", 9.5)
        note = jnote + ("  " + " · ".join(notes) if notes else "")
        for line in wrap(c, note, "DV", 9.5, W - 120)[:2]:
            c.drawString(80, y, line)
            y -= 13
        c.setFont("DVB", 9.5)
        c.drawString(28, y - 2, "Caption:")
        c.setFont("DV", 9.5)
        y -= 2
        for line in wrap(c, strip_emoji(spec.get("caption", "")), "DV", 9.5, W - 120)[:3]:
            c.drawString(80, y, line)
            y -= 13
        c.showPage()
    c.save()
    print(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
