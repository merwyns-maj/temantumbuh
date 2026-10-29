#!/usr/bin/env python3
"""Render a TemanTumbuh carousel spec (JSON) into 1080x1440 PNG slides.

Usage: python render.py posts/<post>.json [out_dir]
Reads design/tokens.json (the TemanTumbuh Design System) for every colour, size and spacing,
so the slides follow the system. Fails loudly instead of letting text overlap.
"""
import io
import json
import math
import os
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1440
TOK = json.load(open(os.path.join(ROOT, "design", "tokens.json"), encoding="utf-8"))
FONT_DIR = os.path.join(ROOT, "fonts")
SVG_DIR = os.path.join(ROOT, "design", "svg")

FONTS = {
    "display": "fredoka-latin-600-normal.woff",
    "body600": "nunito-latin-600-normal.woff",
    "body700": "nunito-latin-700-normal.woff",
    "body800": "nunito-latin-800-normal.woff",
}
SERIES = {
    "pintar": ("SERI ANAK PINTAR", "seri-anak-pintar.svg"),
    "mpasi": ("SERI MPASI", "seri-mpasi.svg"),
    "main": ("SERI MAIN DI RUMAH", "seri-main-di-rumah.svg"),
    "sekolah": ("SERI SIAP SEKOLAH", "seri-siap-sekolah.svg"),
    "ayah": ("SERI AYAH BARU", "seri-ayah-baru.svg"),
    "ibu": ("SERI IBU", "seri-ibu.svg"),
}
DISCLAIMER = "Konten edukasi umum. Untuk kondisi khusus, konsultasikan dengan dokter anak."


class LayoutError(Exception):
    pass


# ------------------------------------------------------------------ tokens
def _px(v):
    return int(round(float(str(v).replace("px", ""))))


SPACE = {t["name"]: _px(t["value"]) for t in TOK["spacing"]["tokens"]}
RADIUS = {t["name"]: _px(t["value"]) for t in TOK["radius"]["tokens"]}
STYLES = {s["name"]: s for g in TOK["type"]["groups"] for s in g["styles"]}
COLORS = {t["name"]: t["value"] for t in TOK["color"]["tokens"]}


def color(name, theme):
    v = COLORS[name]
    v = v.get(theme, v.get("light")) if isinstance(v, dict) else v
    if v.startswith("{"):
        return color(v.strip("{}"), theme)
    v = v.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def font(kind, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), size)


def style_font(name):
    s = STYLES[name]
    if s.get("family") == "body":
        kind = {600: "body600", 700: "body700", 800: "body800"}[int(s["fontWeight"])]
    else:
        kind = "display"
    return font(kind, _px(s["fontSize"])), _px(s["lineHeight"])


def svg_ratio(name):
    """width / height from an SVG's viewBox."""
    import re
    vb = re.search(r'viewBox="([^"]+)"', open(os.path.join(ROOT, "design", "svg", name), encoding="utf-8").read(1000))
    _, _, w, h = (float(v) for v in vb.group(1).split())
    return w / h


def svg_image(name, size, height=None):
    png = cairosvg.svg2png(url=os.path.join(SVG_DIR, name), output_width=size, output_height=height or size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


# Series whose corner shapes take the series tint instead of plain surface-200
TINTED = {"mpasi"}
ART_RATIO = 880 / 260  # food/art-*.svg cut diagrams
HERO_RATIO = 880 / 420  # food/hero-*.svg hook illustrations (design v2)
BIG_RATIO = 880 / 500  # food/big-*.svg point scenes (design v2)
# Tunas mascot (design/svg/tunas/*.svg, 120 x 140 viewBox): hook top right, CTA in place of the motif
MASCOT_HOOK = (172, 200)
MASCOT_CTA = (206, 240)
MASCOT_POSES = {"halo", "riset", "mikir", "hore", "kaget", "ngantuk", "sayang", "santai"}


# ------------------------------------------------------------------ text helpers
def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if not cur:
                raise LayoutError(f"word too long for the line: {w!r}")
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def tracked_len(draw, text, f, tracking):
    return sum(draw.textlength(ch, font=f) for ch in text) + tracking * (len(text) - 1)


def bezier(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


# ------------------------------------------------------------------ shared chrome
class Slide:
    def __init__(self, spec, post, idx, total):
        self.spec, self.post, self.idx, self.total = spec, post, idx, total
        self.theme = spec.get("theme", "light")
        self.img = Image.new("RGB", (W, H), self.c("surface-100"))
        self.d = ImageDraw.Draw(self.img)
        self.series = post["series"]
        self.m = SPACE["safe-margin"]

    def c(self, name):
        return color(name, self.theme)

    def chrome(self):
        d = self.d
        blob = self.c(f"seri-{self.series}-bg") if self.series in TINTED and self.theme == "light" else self.c("surface-200")
        d.ellipse([-220, -180, 260, 240], fill=blob)
        d.ellipse([820, 1160, 1320, 1660], fill=blob)
        # logo lockup
        logo = svg_image("tt-primary-dark.svg" if self.theme == "dark" else "tt-primary.svg", 60)
        self.img.paste(logo, (self.m - 2, 54), logo)
        f, _ = style_font("wordmark")
        x, cy = self.m + 60 + SPACE["space-2"] - 4, 84
        for part, col in (("T", "sage-deep"), ("eman", "ink"), ("T", "terra-deep"), ("umbuh", "ink")):
            d.text((x, cy), part, font=f, fill=self.c(col), anchor="lm")
            x += d.textlength(part, font=f)
        self.wordmark_end = x
        # series tag
        label, icon_file = SERIES[self.series]
        tf, _ = style_font("tag")
        tw = tracked_len(d, label, tf, 1)
        h, padl, padr, icon, gap = 52, 16, 24, 32, 10
        w = padl + icon + gap + tw + padr
        x1 = W - self.m
        x0 = x1 - w
        if x0 < self.wordmark_end + 20:
            raise LayoutError("series tag collides with the wordmark")
        d.rounded_rectangle([x0, cy - h / 2, x1, cy + h / 2], radius=h / 2, fill=self.c(f"seri-{self.series}-bg"))
        ic = svg_image(icon_file, icon)
        self.img.paste(ic, (int(x0 + padl), int(cy - icon / 2)), ic)
        tracked(d, (x0 + padl + icon + gap, cy - 15), label, tf, self.c(f"seri-{self.series}-ink"), 1)
        # footer
        gapd, r = 30, 7
        x0 = W / 2 - (self.total - 1) * gapd / 2
        for i in range(self.total):
            col = self.c("terra") if i == self.idx else self.c("dot-inactive")
            d.ellipse([x0 + i * gapd - r, H - 88 - r, x0 + i * gapd + r, H - 88 + r], fill=col)
        cf, _ = style_font("caption")
        d.text((W / 2, H - 46), self.post.get("handle", "@temantumbuhid"), font=cf, fill=self.c("ink-muted"), anchor="mm")

    def chip(self, x, cy, text, fill, ink, outline=None, size=26):
        d = self.d
        f = font("body800", size)
        tw = tracked_len(d, text, f, 1)
        h = size + 30
        w = tw + 44
        d.rounded_rectangle([x, cy - h / 2, x + w, cy + h / 2], radius=h / 2, fill=self.c(fill),
                            outline=self.c(outline) if outline else None, width=2 if outline else 0)
        tracked(d, (x + 22, cy - size * 0.62), text, f, self.c(ink), 1)
        return x + w

    # ---------------- motifs
    def motif(self, kind, x, y):
        d = self.d
        if kind == "sun":
            cx, cy = x + 75, y + 75
            d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=self.c("sun"))
            for k in range(8):
                a = k * math.pi / 4
                d.line([cx + 58 * math.cos(a), cy + 58 * math.sin(a), cx + 72 * math.cos(a), cy + 72 * math.sin(a)],
                       fill=self.c("sun"), width=10)
                for px, py in ((cx + 58 * math.cos(a), cy + 58 * math.sin(a)), (cx + 72 * math.cos(a), cy + 72 * math.sin(a))):
                    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=self.c("sun"))
        elif kind == "moon":
            d.ellipse([x + 24, y + 19, x + 136, y + 131], fill=self.c("sun"))
            d.ellipse([x + 54, y + 10, x + 158, y + 114], fill=self.c("surface-100"))
        elif kind == "leaf":
            pts = bezier((x + 10, y + 40), (x + 30, y + 12), (x + 66, y + 10), (x + 84, y + 26)) + \
                bezier((x + 84, y + 26), (x + 64, y + 50), (x + 30, y + 56), (x + 10, y + 40))
            d.polygon(pts, fill=self.c("sage"))
            self.spark(x + 100, y + 83, 18)
        elif kind == "spark":
            self.spark(x + 70, y + 40, 30)
            self.spark(x + 105, y + 85, 16, "terra")
        elif kind == "heart":
            self.heart(x + 60, y + 52, 44, "terra")

    def spark(self, cx, cy, s, col="sun"):
        pts = [(cx, cy - s), (cx + .28 * s, cy - .28 * s), (cx + s, cy), (cx + .28 * s, cy + .28 * s),
               (cx, cy + s), (cx - .28 * s, cy + .28 * s), (cx - s, cy), (cx - .28 * s, cy - .28 * s)]
        self.d.polygon(pts, fill=self.c(col))

    def heart(self, cx, cy, s, col):
        pts = bezier((cx, cy + s), (cx - 1.6 * s, cy + .1 * s), (cx - .9 * s, cy - 1.1 * s), (cx, cy - .45 * s)) + \
            bezier((cx, cy - .45 * s), (cx + .9 * s, cy - 1.1 * s), (cx + 1.6 * s, cy + .1 * s), (cx, cy + s))
        self.d.polygon(pts, fill=self.c(col))

    # ---------------- slide types
    def hook(self):
        if self.spec.get("hero"):
            return self.hook_hero()
        d, s, m = self.d, self.spec, self.m
        mascot_x = None
        if s.get("mascot"):
            mw, mh = MASCOT_HOOK
            mascot_x = W - m - mw
            im = svg_image(f"tunas/tunas-{s['mascot']}.svg", mw, mh)
            self.img.paste(im, (mascot_x, 150), im)
        elif s.get("motif"):
            self.motif(s["motif"], 840, 200)
        kf, ktrack = font("body800", 28), 1
        kw = tracked_len(d, s["kicker"], kf, ktrack)
        d.rounded_rectangle([m, 250, m + kw + 48, 308], radius=29, fill=self.c("sage-ink"))
        tracked(d, (m + 24, 262), s["kicker"], kf, self.c("on-accent"), ktrack)
        if self.post.get("usia"):
            x0 = m + kw + 48 + 16
            if x0 + tracked_len(d, self.post["usia"], font("body800", 26), 1) + 44 > W - m:
                raise LayoutError("kicker and age chip do not fit on one row")
            end = self.chip(x0, 279, self.post["usia"], "surface-card", "ink-muted", outline="line")
            if mascot_x is not None and end > mascot_x - 10:
                raise LayoutError("kicker and age chip run into the mascot: shorten the kicker")
        hf, lh = style_font("hook-display")
        y = 364
        if len(s["lines"]) > 4:
            raise LayoutError("hook has more than 4 lines")
        for i, line in enumerate(s["lines"]):
            if d.textlength(line, font=hf) > W - 2 * m:
                raise LayoutError(f"hook line too wide: {line!r}")
            d.text((m, y), line, font=hf, fill=self.c("accent-text" if i == s.get("accent") else "ink"))
            y += lh
        y += 30
        d.rounded_rectangle([m, y, m + 250, y + 8], radius=4, fill=self.c("terra"))
        y += 48
        sf, slh = style_font("sub")
        for line in wrap(d, s["sub"], sf, 820):
            d.text((m, y), line, font=sf, fill=self.c("ink-muted"))
            y += slh
        if y > H - 260:
            raise LayoutError("hook sub line runs into the swipe cue")
        if s.get("art"):
            icons = s["art"]
            top, bottom = y + 30, H - 212 - 50
            gap = 20
            size = min(190, bottom - top, (W - 2 * m - gap * (len(icons) - 1)) // len(icons))
            if size < 110:
                raise LayoutError("no room for the hook food row: shorten the sub line")
            x0 = m - 10  # left-aligned with the text, icons have built-in padding
            iy = int(top + (bottom - top - size) / 2)
            for i, name in enumerate(icons):
                im = svg_image(f"food/{name}.svg", size)
                self.img.paste(im, (int(x0 + i * (size + gap)), iy), im)
        self.swipe()

    def hook_hero(self):
        """Hook with a big illustration on top (design v2): the first slide is the thumbnail people scroll past."""
        d, s, m = self.d, self.spec, self.m
        kf, ktrack = font("body800", 28), 1
        kw = tracked_len(d, s["kicker"], kf, ktrack)
        d.rounded_rectangle([m, 170, m + kw + 48, 228], radius=29, fill=self.c("sage-ink"))
        tracked(d, (m + 24, 182), s["kicker"], kf, self.c("on-accent"), ktrack)
        if self.post.get("usia"):
            self.chip(m + kw + 48 + 16, 199, self.post["usia"], "surface-card", "ink-muted", outline="line")
        ratio = svg_ratio(f"food/hero-{s['hero']}.svg")
        hw = W - 2 * m + 40
        hh = int(hw / ratio)
        if hh > 430:
            hh = 430
            hw = int(hh * ratio)
        im = svg_image(f"food/hero-{s['hero']}.svg", hw, hh)
        self.img.paste(im, (int((W - hw) / 2), 250), im)
        hf, lh = style_font("hook-display")
        y = 250 + hh + 20
        if len(s["lines"]) > 3:
            raise LayoutError("hero hook takes at most 3 lines")
        for i, line in enumerate(s["lines"]):
            if d.textlength(line, font=hf) > W - 2 * m:
                raise LayoutError(f"hook line too wide: {line!r}")
            d.text((m, y), line, font=hf, fill=self.c("accent-text" if i == s.get("accent") else "ink"))
            y += lh
        y += 22
        d.rounded_rectangle([m, y, m + 250, y + 8], radius=4, fill=self.c("terra"))
        y += 36
        sf, slh = style_font("sub")
        lines = wrap(d, s["sub"], sf, W - 2 * m)
        if len(lines) > 1:
            raise LayoutError("hero hook sub must fit on one line")
        d.text((m, y), lines[0], font=sf, fill=self.c("ink-muted"))
        if y + slh > H - 240:
            raise LayoutError("hero hook runs into the swipe cue: shorter hero or fewer lines")
        self.swipe()

    def cheat(self):
        """One-page cheat sheet (design v2): every point as a row with its mini illustration, made to be screenshotted."""
        d, s, m = self.d, self.spec, self.m
        self.chip(m, 200, s.get("kicker", "CONTEKAN"), "sage-ink", "on-accent", size=26)
        hf, hlh = style_font("slide-title")
        y = 262
        for line in wrap(d, s["title"], hf, W - 2 * m):
            d.text((m, y), line, font=hf, fill=self.c("ink"))
            y += hlh
        y += 24
        rows = s["rows"]
        bottom = H - SPACE["footer-zone"] - (60 if s.get("note") else 0)
        rh = min(230, (bottom - y) // len(rows))
        if rh < 150:
            raise LayoutError("cheat sheet rows too tight: fewer rows or a shorter title")
        tf = font("body800", 40)
        nf = font("body600", 32)
        for i, r in enumerate(rows):
            ry = y + i * rh
            d.rounded_rectangle([m, ry + 8, W - m, ry + rh - 8], radius=RADIUS["radius-md"], fill=self.c("surface-card"),
                                outline=self.c("line"), width=3)
            self.disc_number(m + 62, ry + rh // 2, 38, str(i + 1), 44)
            aw, ah = 300, int(300 / ART_RATIO)
            im = svg_image(f"food/art-{r['art']}.svg", aw, ah)
            self.img.paste(im, (W - m - aw - 16, int(ry + (rh - ah) / 2)), im)
            tx, tw = m + 124, W - 2 * m - 124 - aw - 30
            lines = wrap(d, r["text"], tf, tw)
            sub = wrap(d, r.get("small", ""), nf, tw) if r.get("small") else []
            if len(lines) > 2 or len(sub) > 1:
                raise LayoutError(f"cheat row too long: {r['text']!r}")
            th = len(lines) * 50 + len(sub) * 42
            ty = ry + (rh - th) / 2
            for line in lines:
                d.text((tx, ty), line, font=tf, fill=self.c("ink"))
                ty += 50
            for line in sub:
                d.text((tx, ty), line, font=nf, fill=self.c("ink-muted"))
                ty += 42
        if s.get("note"):
            d.text((W / 2, bottom + 20), s["note"], font=font("body800", 32), fill=self.c("accent-text"), anchor="mm")

    def swipe(self):
        d = self.d
        f = font("display", 42)
        label = "geser"
        tw = d.textlength(label, font=f)
        total = tw + 18 + 44
        x = W / 2 - total / 2
        y = H - 212
        col = self.c("accent-text")
        d.text((x, y), label, font=f, fill=col, anchor="lm")
        ax = x + tw + 18
        d.line([ax, y + 2, ax + 40, y + 2], fill=col, width=6)
        d.line([ax + 26, y - 12, ax + 41, y + 2], fill=col, width=6)
        d.line([ax + 26, y + 16, ax + 41, y + 2], fill=col, width=6)

    def disc_number(self, cx, cy, r, num, size):
        d = self.d
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=self.c(f"seri-{self.series}-bg"))
        d.text((cx, cy + 4), num, font=font("display", size), fill=self.c(f"seri-{self.series}-ink"), anchor="mm")

    def point(self):
        d, s, m = self.d, self.spec, self.m
        if s.get("motif"):
            self.motif(s["motif"], 880, 180)
        if s.get("number", True):
            self.disc_number(164, 276, 100, s.get("num") or f"{self.idx:02d}", 110)
        if s.get("usia"):
            self.chip(292, 276, s["usia"], "surface-card", "ink-muted", outline="line")
        has_body = bool(s.get("body")) or bool(s.get("art_big"))  # a big scene takes the body's place
        # tips box first: the body yields to it
        lf, llh = style_font("box-label")
        tf, tlh = style_font("tips")
        inner = W - 2 * m - 80 - 6
        tlines = wrap(d, s["tips"], tf, inner)
        max_tips = 3 if has_body else 6
        if len(tlines) > max_tips:
            raise LayoutError(f"tips is {len(tlines)} lines, max {max_tips}: {s['tips']!r}")
        bh = 30 + llh + 14 + len(tlines) * tlh + 30
        # title
        hf, hlh = style_font("slide-title")
        title = s["title"]
        if title.startswith('"') and title.endswith('"'):
            title = "\u201c" + title[1:-1] + "\u201d"
        hlines = wrap(d, title, hf, W - 2 * m)
        if len(hlines) > 3:
            raise LayoutError(f"title is {len(hlines)} lines, max 3")
        y = 420
        if s.get("label"):
            self.chip(m, 438, s["label"], "blush", "terra-ink", size=28)
            y = 500
        for line in hlines:
            d.text((m, y), line, font=hf, fill=self.c("ink"))
            y += hlh
        y += 22
        d.rounded_rectangle([m, y, m + 180, y + 6], radius=3, fill=self.c("sage"))
        y += 34
        # box: anchored above the footer when there is body text, else right under the title
        if has_body:
            by1 = H - SPACE["footer-zone"]
            by0 = by1 - bh
        else:
            by0 = y + 26
            by1 = by0 + bh
            if by1 > H - SPACE["footer-zone"]:
                raise LayoutError("title plus box too tall: cut words")
        bf, blh = style_font("body")
        blines = wrap(d, s["body"], bf, W - 2 * m) if s.get("body") else []
        if y + len(blines) * blh > by0 - 24:
            raise LayoutError(f"body runs into the tips box by {y + len(blines) * blh - (by0 - 24)}px: cut words")
        for line in blines:
            d.text((m, y), line, font=bf, fill=self.c("ink-muted"))
            y += blh
        if s.get("art"):
            big = bool(s.get("art_big"))  # design v2: taller, detailed scene in food/big-<name>.svg
            ratio = svg_ratio(f"food/big-{s['art']}.svg") if big else ART_RATIO
            room = by0 - y - 56
            ah = min(500 if big else 250, room, int((W - 2 * m + (60 if big else 0)) / ratio))
            if ah < (300 if big else 150):
                raise LayoutError(f"no room for art {s['art']!r} ({room}px): cut body or tips words")
            aw = int(ah * ratio)
            im = svg_image(f"food/{'big' if big else 'art'}-{s['art']}.svg", aw, ah)
            self.img.paste(im, (int((W - aw) / 2), int(y + 28 + (room - ah) / 2)), im)
        d.rounded_rectangle([m, by0, W - m, by1], radius=RADIUS["radius-md"], fill=self.c("sage-tint"),
                            outline=self.c("sage"), width=3)
        tracked(d, (m + 40, by0 + 30), s.get("tips_label", "COBA INI"), lf, self.c("sage-ink"), 1)
        ty = by0 + 30 + llh + 14
        for line in tlines:
            d.text((m + 40, ty), line, font=tf, fill=self.c("ink"))
            ty += tlh

    def punch(self):
        d, s, m = self.d, self.spec, self.m
        self.disc_number(W // 2, 520, 150, str(self.idx), 200)
        if s.get("zzz"):
            zf = [font("display", 60), font("display", 46), font("display", 34)]
            for i, f in enumerate(zf):
                d.text((W // 2 + 160 + i * 44, 430 - i * 50), "z", font=f, fill=self.c("ink-muted"))
        size = 130
        while d.textlength(s["word"], font=font("display", size)) > W - 2 * m:
            size -= 6
        d.text((W / 2, 810), s["word"], font=font("display", size), fill=self.c("ink"), anchor="mm")
        d.rounded_rectangle([W / 2 - 90, 900, W / 2 + 90, 906], radius=3, fill=self.c("terra"))
        pf = font("body600", 46)
        y = 960
        lines = wrap(d, s["punch"], pf, 880)
        if y + len(lines) * 68 > H - SPACE["footer-zone"] - 20:
            raise LayoutError("punchline too long")
        for line in lines:
            d.text((W / 2, y), line, font=pf, fill=self.c("ink-muted"), anchor="ma")
            y += 68

    def cta(self):
        d, s, m = self.d, self.spec, self.m
        hf, hlh = style_font("cta-headline")
        sf, slh = style_font("sub")
        cf, clh = style_font("caption")
        pf = font("display", 40)
        blocks = []  # (height, draw_fn)
        if s.get("mascot"):
            mw, mh = MASCOT_CTA
            blocks.append((mh, lambda y: self.img.paste(im := svg_image(f"tunas/tunas-{s['mascot']}.svg", mw, mh), (W // 2 - mw // 2, int(y)), im)))
        elif s.get("motif") == "logo":
            blocks.append((220, lambda y: self.img.paste(lg := svg_image("tt-primary.svg", 220), (W // 2 - 110, int(y)), lg)))
        else:
            def disc(y):
                d.ellipse([W / 2 - 120, y, W / 2 + 120, y + 240], fill=self.c("blush"))
                self.heart(W / 2, y + 128, 50, "terra")
            blocks.append((240, disc))

        def text_block(lines, f, lh, col):
            def fn(y):
                for i, line in enumerate(lines):
                    d.text((W / 2, y + i * lh), line, font=f, fill=self.c(col), anchor="ma")
            return (len(lines) * lh, fn)

        head = wrap(d, s["headline"], hf, W - 2 * m)
        acc = wrap(d, s["accent"], hf, W - 2 * m)
        blocks.append((len(head) * hlh + len(acc) * hlh, lambda y: (text_block(head, hf, hlh, "ink")[1](y),
                                                                     text_block(acc, hf, hlh, "accent-text")[1](y + len(head) * hlh))))
        if s.get("sub"):
            blocks.append(text_block(wrap(d, s["sub"], sf, W - 2 * m), sf, slh, "ink-muted"))
        pw = d.textlength(s["pill"], font=pf) + 112
        if pw > W - 2 * m:
            raise LayoutError("CTA pill text too long")

        def pill(y):
            d.rounded_rectangle([W / 2 - pw / 2, y, W / 2 + pw / 2, y + 100], radius=50, fill=self.c("terra-deep"))
            d.text((W / 2, y + 52), s["pill"], font=pf, fill=self.c("on-accent"), anchor="mm")
        blocks.append((100, pill))
        if s.get("sub2"):
            blocks.append(text_block(wrap(d, s["sub2"], sf, W - 2 * m), sf, slh, "ink-muted"))
        if s.get("source"):
            sf2 = font("body800", 26)
            blocks.append(text_block(wrap(d, s["source"], sf2, 860), sf2, clh, "sage-ink"))
        if s.get("disclaimer"):
            blocks.append(text_block(wrap(d, DISCLAIMER, cf, 820), cf, clh, "ink-muted"))
        gap = 34
        total = sum(h for h, _ in blocks) + gap * (len(blocks) - 1)
        top, bottom = 160, H - 170
        if total > bottom - top:
            raise LayoutError("CTA content too tall")
        y = top + (bottom - top - total) / 2
        for h, fn in blocks:
            fn(y)
            y += h + gap

    def cheatsheet(self):
        """One-pager summary: title plus rows of [what, how]. Built to be screenshotted and forwarded."""
        d, s, m = self.d, self.spec, self.m
        y = 200
        if s.get("kicker"):
            self.chip(m, 210, s["kicker"], "sage-ink", "on-accent", size=26)
            y = 262
        hf, hlh = style_font("slide-title")
        for line in wrap(d, s["title"], hf, W - 2 * m):
            d.text((m, y), line, font=hf, fill=self.c("ink"))
            y += hlh
        y += 26
        lf, rf = font("body800", 34), font("body600", 32)
        lw, gap, rlh, pad = 360, 32, 44, 22
        rw = W - 2 * m - 48 - lw - gap
        rows = []
        icon_w = 64 if any(len(r) > 2 for r in s["rows"]) else 0
        rx = m + 48 + lw + gap
        lw -= icon_w + (14 if icon_w else 0)
        for row in s["rows"]:
            what, how = row[0], row[1]
            ll, rl = wrap(d, what, lf, lw), wrap(d, how, rf, rw)
            rows.append((ll, rl, max(max(len(ll), len(rl)) * rlh, icon_w), row[2] if len(row) > 2 else None))
        card_h = sum(r[2] for r in rows) + pad * 2 * len(rows)
        note_h = 0
        if s.get("note"):
            nf, nlh = style_font("tips")
            nlines = wrap(d, s["note"], nf, W - 2 * m - 80)
            note_h = 28 + len(nlines) * nlh + 56
        if y + card_h + note_h > H - SPACE["footer-zone"]:
            raise LayoutError(f"cheatsheet too tall by {y + card_h + note_h - (H - SPACE['footer-zone'])}px: cut rows or words")
        d.rounded_rectangle([m, y, W - m, y + card_h], radius=RADIUS["radius-md"], fill=self.c("surface-card"),
                            outline=self.c("line"), width=2)
        ry = y
        for i, (ll, rl, h, icon) in enumerate(rows):
            ty = ry + pad
            if icon:
                im = svg_image(f"food/{icon}.svg", 64)
                self.img.paste(im, (m + 18, int(ty + h / 2 - 32)), im)
            else:
                d.ellipse([m + 24, ty + 12, m + 40, ty + 28], fill=self.c(f"seri-{self.series}-ink"))
            for j, line in enumerate(ll):
                d.text((m + 56 + icon_w + (14 if icon_w else 0), ty + j * rlh), line, font=lf, fill=self.c("ink"))
            for j, line in enumerate(rl):
                d.text((rx, ty + j * rlh), line, font=rf, fill=self.c("ink-muted"))
            ry += h + pad * 2
            if i < len(rows) - 1:
                d.line([m + 24, ry, W - m - 24, ry], fill=self.c("line"), width=2)
        if s.get("note"):
            by0 = y + card_h + 28
            d.rounded_rectangle([m, by0, W - m, by0 + len(nlines) * nlh + 56], radius=RADIUS["radius-md"],
                                fill=self.c("sage-tint"), outline=self.c("sage"), width=3)
            ty = by0 + 28
            for line in nlines:
                d.text((m + 40, ty), line, font=nf, fill=self.c("ink"))
                ty += nlh

    def pyramid(self):
        """Our own drawn pyramid: 'tiers' bottom to top as [label, small line]; never a copy of someone else's figure."""
        d, s, m = self.d, self.spec, self.m
        y = 200
        if s.get("kicker"):
            self.chip(m, 210, s["kicker"], "sage-ink", "on-accent", size=26)
            y = 262
        hf, hlh = style_font("slide-title")
        for line in wrap(d, s["title"], hf, W - 2 * m):
            d.text((m, y), line, font=hf, fill=self.c("ink"))
            y += hlh
        y += 36
        nf, nlh = style_font("tips")
        nlines = wrap(d, s.get("note", ""), nf, W - 2 * m - 80) if s.get("note") else []
        note_h = (28 + len(nlines) * nlh + 56 + 30) if nlines else 0
        tiers = s["tiers"]
        n = len(tiers)
        bottom = H - SPACE["footer-zone"] - note_h
        height = bottom - y
        th = height / n
        if th < 120:
            raise LayoutError(f"pyramid tiers only {th:.0f}px tall: shorten the title or note")
        fills = s.get("fills", ["sage-tint", "seri-sekolah-bg", "seri-mpasi-bg", "blush"])
        inks = s.get("inks", ["sage-ink", "seri-sekolah-ink", "seri-mpasi-ink", "terra-ink"])
        cx, half_base, half_top, gap = W / 2, (W - 2 * m) / 2, 110, 10
        lf, sf = font("display", 44), font("body700", 28)
        for i, (label, small) in enumerate(tiers):
            yb = bottom - i * th
            yt = yb - th + gap
            wb = half_base - (half_base - half_top) * i / n
            wt = half_base - (half_base - half_top) * (i + 1) / n
            d.polygon([(cx - wb, yb), (cx + wb, yb), (cx + wt, yt), (cx - wt, yt)], fill=self.c(fills[i % len(fills)]))
            ink = self.c(inks[i % len(inks)])
            maxw = 2 * wt - 40
            size = 44
            while d.textlength(label, font=font("display", size)) > maxw and size > 26:
                size -= 2
            lf = font("display", size)
            sl = wrap(d, small, sf, maxw) if small else []
            block = size + 8 + len(sl) * 36
            ty = (yt + yb) / 2 - block / 2
            d.text((cx, ty), label, font=lf, fill=ink, anchor="ma")
            ty += size + 8
            for line in sl:
                d.text((cx, ty), line, font=sf, fill=ink, anchor="ma")
                ty += 36
        if nlines:
            by0 = bottom + 30
            d.rounded_rectangle([m, by0, W - m, by0 + len(nlines) * nlh + 56], radius=RADIUS["radius-md"],
                                fill=self.c("sage-tint"), outline=self.c("sage"), width=3)
            ty = by0 + 28
            for line in nlines:
                d.text((m + 40, ty), line, font=nf, fill=self.c("ink"))
                ty += nlh

    def gallery(self):
        """Title plus a grid of our own images (stickers, worksheet pages): 'items' are paths from the repo root."""
        d, s, m = self.d, self.spec, self.m
        y = 200
        if s.get("kicker"):
            self.chip(m, 210, s["kicker"], "sage-ink", "on-accent", size=26)
            y = 262
        hf, hlh = style_font("slide-title")
        for line in wrap(d, s["title"], hf, W - 2 * m):
            d.text((m, y), line, font=hf, fill=self.c("ink"))
            y += hlh
        y += 30
        note_h, nlines = 0, []
        if s.get("note"):
            nf, nlh = style_font("tips")
            nlines = wrap(d, s["note"], nf, W - 2 * m - 80)
            note_h = 28 + len(nlines) * nlh + 56 + 28
        items = s["items"]
        cols = s.get("cols", 2 if len(items) <= 4 else 3)
        rows = -(-len(items) // cols)
        gap = 20
        room = H - SPACE["footer-zone"] - y - note_h
        cell = min((W - 2 * m - gap * (cols - 1)) // cols, (room - gap * (rows - 1)) // rows)
        if cell < 200:
            raise LayoutError(f"gallery cells only {cell}px: fewer items or a shorter title")
        gx = (W - (cols * cell + (cols - 1) * gap)) // 2
        y += max(0, (room - rows * cell - (rows - 1) * gap) // 3)
        for i, path in enumerate(items):
            im = Image.open(os.path.join(ROOT, path)).convert("RGBA").resize((cell, cell), Image.LANCZOS)
            cx, cy = gx + (i % cols) * (cell + gap), y + (i // cols) * (cell + gap)
            d.rounded_rectangle([cx, cy, cx + cell, cy + cell], radius=RADIUS["radius-md"], fill=self.c("surface-200"))
            self.img.paste(im, (cx, cy), im)
        if nlines:
            by0 = y + rows * cell + (rows - 1) * gap + 28
            d.rounded_rectangle([m, by0, W - m, by0 + len(nlines) * nlh + 56], radius=RADIUS["radius-md"],
                                fill=self.c("sage-tint"), outline=self.c("sage"), width=3)
            ty = by0 + 28
            for line in nlines:
                d.text((m + 40, ty), line, font=nf, fill=self.c("ink"))
                ty += nlh

    def render(self):
        self.chrome()
        getattr(self, self.spec["type"])()
        return self.img


def render_post(path, out_dir=None):
    post = json.load(open(path, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(path))[0]
    out_dir = out_dir or os.path.join(ROOT, "out", name)
    os.makedirs(out_dir, exist_ok=True)
    slides = post["slides"]
    imgs = []
    for i, spec in enumerate(slides):
        try:
            img = Slide(spec, post, i, len(slides)).render()
        except LayoutError as e:
            raise SystemExit(f"{name} slide {i + 1}: {e}")
        img.save(os.path.join(out_dir, f"slide-{i + 1}.png"))
        imgs.append(img)
    # contact sheet for quick review on a phone
    tw, th, g = 360, 480, 24
    sheet = Image.new("RGB", (len(imgs) * (tw + g) + g, th + 2 * g), (236, 228, 216))
    for i, im in enumerate(imgs):
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (g + i * (tw + g), g))
    sheet.save(os.path.join(out_dir, "contact-sheet.png"))
    return out_dir


if __name__ == "__main__":
    print(render_post(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
