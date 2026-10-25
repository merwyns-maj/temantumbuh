#!/usr/bin/env python3
"""Turn an approved carousel spec into a short 9:16 motion video (MP4, no audio).

Usage: python tools/recut.py posts/<slug>.json [out.mp4] [--point-secs 1.8]

Scenes, built from the spec (no new copy):
  hook   lines pop in one by one, the accent line in terra, Tunas bounces in, the sub fades up
  point  one per point slide: numbered disc + title slide up (the tips box is left for the carousel)
  cta    headline + accent, Tunas, the pill, source and disclaimer
Everything stays inside TikTok's safe zone: x 80..900 (the right rail has the buttons),
y 220..1500 (the bottom has the caption). Music is added in TikTok when posting.
"""
import math
import os
import subprocess
import sys
import json

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import DISCLAIMER, SERIES, color, font, style_font, svg_image, wrap  # noqa: E402

W, H, FPS = 1080, 1920, 30
LEFT, RIGHT, TOP, BOTTOM = 80, 900, 220, 1500


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def back_out(t, s=1.7):
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1


def paste_alpha(base, im, xy, alpha):
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy()
        a = im.split()[3].point(lambda v: int(v * alpha))
        im.putalpha(a)
    base.alpha_composite(im, (int(xy[0]), int(xy[1])))


def text_layer(lines, f, lh, fills, width=W, align="left"):
    h = lh * len(lines) + 20
    im = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (line, col) in enumerate(zip(lines, fills)):
        x = 0 if align == "left" else (width - d.textlength(line, font=f)) / 2
        d.text((x, i * lh), line, font=f, fill=col + (255,))
    return im


class Recut:
    def __init__(self, spec, point_secs=1.8):
        self.spec = spec
        self.series = spec["series"]
        self.c = lambda n: color(n, "light")
        self.point_secs = point_secs
        self.scenes = []
        for s in spec["slides"]:
            if s["type"] == "hook":
                self.scenes.append(("hook", s, 3.2))
            elif s["type"] in ("point", "punch"):
                self.scenes.append(("point", s, point_secs))
            elif s["type"] == "cta":
                self.scenes.append(("cta", s, 3.4))
        self.total = sum(d for _, _, d in self.scenes)
        self.cache = {}

    # ---------- shared chrome
    def base(self):
        im = Image.new("RGBA", (W, H), self.c("surface-100") + (255,))
        d = ImageDraw.Draw(im)
        blob = self.c("surface-200")
        d.ellipse([-260, -200, 300, 300], fill=blob)
        d.ellipse([760, 1560, 1360, 2160], fill=blob)
        logo = svg_image("tt-primary.svg", 64)
        im.alpha_composite(logo, (LEFT - 4, 120))
        f, _ = style_font("wordmark")
        x = LEFT + 76
        for part, col in (("T", "sage-deep"), ("eman", "ink"), ("T", "terra-deep"), ("umbuh", "ink")):
            d.text((x, 152), part, font=f, fill=self.c(col), anchor="lm")
            x += d.textlength(part, font=f)
        return im

    def progress(self, im, t):
        d = ImageDraw.Draw(im)
        y = 1560
        d.rounded_rectangle([LEFT, y, RIGHT, y + 8], radius=4, fill=self.c("dot-inactive"))
        d.rounded_rectangle([LEFT, y, LEFT + (RIGHT - LEFT) * min(1, t / self.total), y + 8], radius=4, fill=self.c("terra"))
        cf, _ = style_font("caption")
        d.text((LEFT, y + 30), self.spec.get("handle", "@temantumbuhid"), font=cf, fill=self.c("ink-muted"))

    def mascot(self, pose, w, h):
        key = ("m", pose, w, h)
        if key not in self.cache:
            self.cache[key] = svg_image(f"tunas/tunas-{pose}.svg", w, h)
        return self.cache[key]

    # ---------- scenes
    def hook(self, im, s, t):
        d = ImageDraw.Draw(im)
        hf = font("display", 118)
        lh = 134
        y0 = 600
        # kicker chip
        kf = font("body800", 30)
        a = ease_out(t / 0.3)
        if a > 0:
            kw = d.textlength(s["kicker"], font=kf) + 48
            chip = Image.new("RGBA", (int(kw), 62), (0, 0, 0, 0))
            cd = ImageDraw.Draw(chip)
            cd.rounded_rectangle([0, 0, kw - 1, 61], radius=31, fill=self.c("sage-ink") + (255,))
            cd.text((24, 13), s["kicker"], font=kf, fill=self.c("on-accent"))
            paste_alpha(im, chip, (LEFT, 500 + 20 * (1 - a)), a)
        for i, line in enumerate(s["lines"]):
            start = 0.25 + i * 0.28
            p = ease_out((t - start) / 0.35)
            if p <= 0:
                continue
            col = self.c("accent-text") if i == s.get("accent") else self.c("ink")
            key = ("hl", i)
            if key not in self.cache:
                size = 118
                while d.textlength(line, font=font("display", size)) > RIGHT - LEFT:
                    size -= 4
                self.cache[key] = text_layer([line], font("display", size), lh, [col])
            paste_alpha(im, self.cache[key], (LEFT - 40 * (1 - p), y0 + i * lh), p)
        n = len(s["lines"])
        bar_t = ease_out((t - 0.25 - n * 0.28) / 0.3)
        if bar_t > 0:
            y = y0 + n * lh + 24
            d.rounded_rectangle([LEFT, y, LEFT + 260 * bar_t, y + 10], radius=5, fill=self.c("terra"))
        sub_t = ease_out((t - 0.45 - n * 0.28) / 0.4)
        if sub_t > 0 and s.get("sub"):
            sf, slh = style_font("sub")
            lines = wrap(d, s["sub"], sf, RIGHT - LEFT)
            layer = text_layer(lines, sf, slh, [self.c("ink-muted")] * len(lines))
            paste_alpha(im, layer, (LEFT, y0 + n * lh + 70 + 20 * (1 - sub_t)), sub_t)
        if s.get("mascot"):
            p = back_out((t - 0.9) / 0.5)
            if (t - 0.9) > 0:
                w, h = 240, 280
                sc = max(0.01, p)
                m = self.mascot(s["mascot"], w, h).resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
                bob = 6 * math.sin((t - 0.9) * 4) if t > 1.4 else 0
                im.alpha_composite(m, (int(RIGHT - w / 2 - m.width / 2 + 10), int(250 + h - m.height + bob)))  # sits above the headline

    def point(self, im, s, t, num):
        d = ImageDraw.Draw(im)
        # disc pops
        p = back_out(t / 0.35)
        r = 120 * max(0.01, p)
        cx, cy = LEFT + 120, 680
        ser = s.get("series", self.series)  # a point can carry its own series colour (e.g. the intro video)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=self.c(f"seri-{ser}-bg"))
        if p > 0.6:
            d.text((cx, cy + 6), f"{num:02d}", font=font("display", int(130 * min(1, p))), fill=self.c(f"seri-{ser}-ink"), anchor="mm")
        # title slides up
        q = ease_out((t - 0.15) / 0.4)
        if q > 0:
            key = ("pt", num)
            if key not in self.cache:
                f = font("display", 92)
                lines = wrap(d, s.get("title") or s.get("word"), f, RIGHT - LEFT)
                self.cache[key] = text_layer(lines, f, 108, [self.c("ink")] * len(lines))
            layer = self.cache[key]
            paste_alpha(im, layer, (LEFT, 880 + 40 * (1 - q)), q)
            bar = ease_out((t - 0.45) / 0.3)
            if bar > 0:
                y = 880 + layer.height + 10
                d.rounded_rectangle([LEFT, y, LEFT + 220 * bar, y + 10], radius=5, fill=self.c("sage"))
            if s.get("mascot"):  # optional Tunas pose per point, top right
                mp = back_out((t - 0.3) / 0.5)
                if t > 0.3:
                    w, h = 220, 257
                    sc = max(0.01, mp)
                    m = self.mascot(s["mascot"], w, h).resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
                    bob = 6 * math.sin((t - 0.3) * 4) if t > 0.8 else 0
                    im.alpha_composite(m, (int(RIGHT - w / 2 - m.width / 2), int(560 + h - m.height + bob)))
            ln = ease_out((t - 0.6) / 0.4)
            if ln > 0 and s.get("line"):  # optional one-line explainer under the title
                key = ("ln", num)
                if key not in self.cache:
                    sf, slh = style_font("sub")
                    lines = wrap(d, s["line"], sf, RIGHT - LEFT)
                    self.cache[key] = text_layer(lines, sf, slh, [self.c("ink-muted")] * len(lines))
                paste_alpha(im, self.cache[key], (LEFT, 880 + layer.height + 50 + 20 * (1 - ln)), ln)

    def cta(self, im, s, t):
        d = ImageDraw.Draw(im)
        if s.get("mascot"):
            p = back_out(t / 0.5)
            w, h = 260, 303
            m = self.mascot(s["mascot"], w, h)
            sc = max(0.01, p)
            m2 = m.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
            im.alpha_composite(m2, (int((LEFT + RIGHT) / 2 - m2.width / 2), int(380 + h - m2.height)))
        hf = font("display", 76)
        q = ease_out((t - 0.3) / 0.4)
        if "cta" not in self.cache:
                head = wrap(d, s["headline"], hf, RIGHT - LEFT)
                acc = wrap(d, s["accent"], hf, RIGHT - LEFT)
                self.cache["cta"] = text_layer(head + acc, hf, 92, [self.c("ink")] * len(head) + [self.c("accent-text")] * len(acc),
                                               width=RIGHT - LEFT, align="center")
        text_y = 730
        pill_y = text_y + self.cache["cta"].height + 40
        if q > 0:
            paste_alpha(im, self.cache["cta"], (LEFT, text_y + 30 * (1 - q)), q)
        pt = back_out((t - 0.8) / 0.4)
        if t > 0.8:
            pf = font("display", 44)
            pw = d.textlength(s["pill"], font=pf) + 110
            ph = 110
            pill = Image.new("RGBA", (int(pw), ph), (0, 0, 0, 0))
            pd = ImageDraw.Draw(pill)
            pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=55, fill=self.c("terra-deep") + (255,))
            pd.text((pw / 2, ph / 2 + 2), s["pill"], font=pf, fill=self.c("on-accent"), anchor="mm")
            sc = max(0.01, pt)
            pill = pill.resize((max(1, int(pill.width * sc)), max(1, int(ph * sc))), Image.LANCZOS)
            im.alpha_composite(pill, (int((LEFT + RIGHT) / 2 - pill.width / 2), int(pill_y + (ph - pill.height) / 2)))
        f2 = ease_out((t - 1.2) / 0.4)
        if f2 > 0:
            lines, fills, fonts = [], [], []
            if s.get("source"):
                lines.append(s["source"])
            if s.get("disclaimer"):
                lines += wrap(d, DISCLAIMER, font("body600", 28), RIGHT - LEFT)
            layer = Image.new("RGBA", (RIGHT - LEFT, 44 * len(lines) + 10), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            for i, line in enumerate(lines):
                f = font("body800", 28) if (s.get("source") and i == 0) else font("body600", 28)
                col = self.c("sage-ink") if (s.get("source") and i == 0) else self.c("ink-muted")
                ld.text(((RIGHT - LEFT) / 2, i * 44), line, font=f, fill=col + (255,), anchor="ma")
            paste_alpha(im, layer, (LEFT, pill_y + 150), f2)

    def frame(self, t):
        im = self.base()
        acc, num = 0.0, 0
        for kind, s, dur in self.scenes:
            if kind == "point":
                num += 1
            if t < acc + dur or (kind, s, dur) == self.scenes[-1]:
                lt = t - acc
                if kind == "hook":
                    self.hook(im, s, lt)
                elif kind == "point":
                    self.point(im, s, lt, num)
                else:
                    self.cta(im, s, lt)
                break
            acc += dur
        self.progress(im, t)
        return im.convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    secs = 1.8
    if "--point-secs" in sys.argv:
        secs = float(sys.argv[sys.argv.index("--point-secs") + 1])
    spec_path = args[0]
    slug = os.path.splitext(os.path.basename(spec_path))[0]
    out = args[1] if len(args) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", f"{slug}.mp4")
    rc = Recut(json.load(open(spec_path, encoding="utf-8")), secs)
    n = int(rc.total * FPS)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(rc.frame(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print(out, f"{rc.total:.1f}s", n, "frames")


if __name__ == "__main__":
    main()
