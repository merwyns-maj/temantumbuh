#!/usr/bin/env python3
"""Animated 'Eksperimen 1 Menit' with Tunas as the host: 9:16 MP4, no audio.

Usage: python tools/animate_experiment.py [out.mp4]

Episode 1, Susu warna-warni. The milk plate is seen from above; the colour drops are a small
particle simulation (they sit still, then rush outward and swirl when the soap touches).
Copy comes from experiments/e01-susu-warna.json (already linted). Safe zone: x 80..900, y 220..1500.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recut import FPS, H, LEFT, RIGHT, W, back_out, ease_out, paste_alpha, text_layer  # noqa: E402
from render import color, font, style_font, svg_image, wrap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = lambda n: color(n, "light")  # noqa: E731
PLATE_C = (540, 860)
PLATE_R = 330
MILK_R = 285
DYES = [(224, 69, 58), (243, 190, 64), (59, 125, 216), (63, 174, 106)]
SCENES = [("judul", 2.6), ("bahan", 3.2), ("tuang", 2.6), ("tetes", 3.0), ("sabun", 2.4),
          ("kabur", 4.6), ("kenapa", 4.2), ("air", 4.4), ("tutup", 3.4)]
TOTAL = sum(d for _, d in SCENES)


class Particles:
    """Colour drops: 4 blobs that sit still until the soap touches, then rush out and swirl."""

    def __init__(self, n_per=170, seed=7, spread=1.0):
        rng = np.random.default_rng(seed)
        centers = [(-55, -50), (55, -50), (55, 55), (-55, 55)]
        pts, cols, born = [], [], []
        for i, (cx, cy) in enumerate(centers):
            r = np.sqrt(rng.random(n_per)) * 34 * spread
            a = rng.random(n_per) * 2 * math.pi
            pts.append(np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1))
            cols += [i] * n_per
            born += [i] * n_per
        self.p0 = np.concatenate(pts)
        self.col = np.array(cols)
        self.drop = np.array(born)
        self.rng = rng

    def simulate(self, seconds, soap=True):
        """Precompute positions per frame after the soap touches."""
        p = self.p0.copy()
        v = np.zeros_like(p)
        frames = []
        dt = 1 / FPS
        tang = self.rng.choice([-1, 1], size=len(p)) * (0.6 + self.rng.random(len(p)))
        gain = (0.25 + self.rng.random(len(p)) ** 1.5)[:, None]
        for k in range(int(seconds * FPS)):
            t = k * dt
            if soap:
                r = np.linalg.norm(p, axis=1, keepdims=True) + 1e-3
                d = p / r
                perp = np.stack([-d[:, 1], d[:, 0]], 1)
                push = 620 * gain * math.exp(-t / 0.8) / (r / 70 + 1)
                swirl = 230 * math.exp(-t / 3.0) * tang[:, None] * (r / (r + 80))
                v += (push * d + swirl * perp) * dt
                v *= 0.90
                p += v * dt
                r = np.linalg.norm(p, axis=1, keepdims=True)
                over = r[:, 0] > MILK_R - 14
                p[over] = p[over] / r[over] * (MILK_R - 14)
            frames.append(p.copy())
        return frames


class Episode:
    def __init__(self):
        self.cache = {}
        self.parts = Particles()
        self.sim = self.parts.simulate(dict(SCENES)["kabur"] + dict(SCENES)["kenapa"] + 0.5)
        self.water = Particles(n_per=120, seed=3, spread=0.8)

    # ---------- pieces
    def tunas(self, pose, w=250):
        key = ("t", pose, w)
        if key not in self.cache:
            self.cache[key] = svg_image(f"tunas/tunas-{pose}.svg", w, int(w * 140 / 120))
        return self.cache[key]

    def base(self):
        im = Image.new("RGBA", (W, H), C("surface-100") + (255,))
        d = ImageDraw.Draw(im)
        d.ellipse([-260, -200, 300, 300], fill=C("surface-200"))
        d.ellipse([760, 1560, 1360, 2160], fill=C("surface-200"))
        logo = svg_image("tt-primary.svg", 64)
        im.alpha_composite(logo, (LEFT - 4, 120))
        f, _ = style_font("wordmark")
        x = LEFT + 76
        for part, col in (("T", "sage-deep"), ("eman", "ink"), ("T", "terra-deep"), ("umbuh", "ink")):
            d.text((x, 152), part, font=f, fill=C(col), anchor="lm")
            x += d.textlength(part, font=f)
        tag = "EKSPERIMEN 1 MENIT"
        tf = font("body800", 24)
        tw = d.textlength(tag, font=tf) + 36
        d.rounded_rectangle([RIGHT - tw, 128, RIGHT, 176], radius=24, fill=C("seri-main-bg"))
        d.text((RIGHT - tw / 2, 152), tag, font=tf, fill=C("seri-main-ink"), anchor="mm")
        return im

    def progress(self, im, t):
        d = ImageDraw.Draw(im)
        y = 1560
        d.rounded_rectangle([LEFT, y, RIGHT, y + 8], radius=4, fill=C("dot-inactive"))
        d.rounded_rectangle([LEFT, y, LEFT + (RIGHT - LEFT) * min(1, t / TOTAL), y + 8], radius=4, fill=C("terra"))
        cf, _ = style_font("caption")
        d.text((LEFT, y + 30), "@temantumbuhid", font=cf, fill=C("ink-muted"))

    def headline(self, im, text, t, y=250, size=78, col="ink"):
        p = ease_out(t / 0.35)
        if p <= 0:
            return 0
        key = ("h", text, size, col)
        if key not in self.cache:
            f = font("display", size)
            d = ImageDraw.Draw(im)
            lines = wrap(d, text, f, RIGHT - LEFT)
            self.cache[key] = text_layer(lines, f, int(size * 1.18), [C(col)] * len(lines))
        layer = self.cache[key]
        paste_alpha(im, layer, (LEFT, y + 30 * (1 - p)), p)
        return layer.height

    def caption(self, im, text, t, y=1250, width=560, size=40, col="ink"):
        p = ease_out(t / 0.35)
        if p <= 0:
            return
        key = ("c", text, width, size, col)
        if key not in self.cache:
            f = font("body700", size)
            d = ImageDraw.Draw(im)
            lines = wrap(d, text, f, width - 60)
            lh = int(size * 1.35)
            box = Image.new("RGBA", (width, lh * len(lines) + 56), (0, 0, 0, 0))
            bd = ImageDraw.Draw(box)
            box = Image.new("RGBA", (width + 40, lh * len(lines) + 56), (0, 0, 0, 0))
            bd = ImageDraw.Draw(box)
            hb = box.height
            bd.polygon([(width - 6, hb * 0.45), (width + 36, hb * 0.62), (width - 6, hb * 0.75)], fill=C("surface-card") + (255,),
                       outline=C("line") + (255,))
            bd.rounded_rectangle([0, 0, width - 1, hb - 1], radius=28, fill=C("surface-card") + (255,),
                                 outline=C("line") + (255,), width=3)
            for i, line in enumerate(lines):
                bd.text((30, 28 + i * lh), line, font=f, fill=C(col) + (255,))
            self.cache[key] = box
        paste_alpha(im, self.cache[key], (LEFT, y + 20 * (1 - p)), p)

    def host(self, im, pose, t, x=650, y=1210, w=250):
        p = back_out(t / 0.45)
        if t <= 0:
            return
        m = self.tunas(pose, w)
        sc = max(0.01, p)
        m2 = m.resize((max(1, int(m.width * sc)), max(1, int(m.height * sc))), Image.LANCZOS)
        bob = 5 * math.sin(t * 3.2) if t > 0.5 else 0
        im.alpha_composite(m2, (int(x + (m.width - m2.width) / 2), int(y + m.height - m2.height + bob)))

    def plate(self, im, milk=1.0, liquid=None):
        d = ImageDraw.Draw(im)
        cx, cy = PLATE_C
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([cx - PLATE_R, cy - PLATE_R + 18, cx + PLATE_R, cy + PLATE_R + 18], fill=(120, 95, 70, 60))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        d.ellipse([cx - PLATE_R, cy - PLATE_R, cx + PLATE_R, cy + PLATE_R], fill=(255, 255, 255), outline=C("line"), width=4)
        d.ellipse([cx - PLATE_R + 34, cy - PLATE_R + 34, cx + PLATE_R - 34, cy + PLATE_R - 34], outline=(238, 232, 224), width=3)
        if milk > 0:
            r = MILK_R * milk
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=liquid or (253, 249, 240))

    def ink(self, im, pts, cols, alpha=1.0, visible=None):
        layer = Image.new("RGBA", (2 * PLATE_R, 2 * PLATE_R), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for (x, y), ci, vis in zip(pts, cols, visible if visible is not None else [1] * len(pts)):
            if vis <= 0:
                continue
            rr = 9 * vis
            r, g, b = DYES[ci]
            d.ellipse([PLATE_R + x - rr, PLATE_R + y - rr, PLATE_R + x + rr, PLATE_R + y + rr], fill=(r, g, b, int(170 * alpha)))
        layer = layer.filter(ImageFilter.GaussianBlur(4))
        mask = Image.new("L", layer.size, 0)
        ImageDraw.Draw(mask).ellipse([PLATE_R - MILK_R, PLATE_R - MILK_R, PLATE_R + MILK_R, PLATE_R + MILK_R], fill=255)
        a = Image.composite(layer.split()[3], Image.new("L", layer.size, 0), mask)
        layer.putalpha(a)
        im.alpha_composite(layer, (PLATE_C[0] - PLATE_R, PLATE_C[1] - PLATE_R))

    def cotton_bud(self, im, k):
        """Bud held by Tunas (standing top right of the plate); k 0 = up in his hand, 1 = tip on the centre."""
        d = ImageDraw.Draw(im)
        hand = (790, 560)
        tip = (PLATE_C[0] + (hand[0] - PLATE_C[0]) * 0.55 * (1 - k), PLATE_C[1] + (hand[1] - PLATE_C[1]) * 0.55 * (1 - k))
        dx, dy = tip[0] - hand[0], tip[1] - hand[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        start = (tip[0] - ux * 300, tip[1] - uy * 300)
        d.line([start, tip], fill=(242, 242, 242), width=12)
        d.ellipse([start[0] - 15, start[1] - 15, start[0] + 15, start[1] + 15], fill=(255, 255, 255), outline=(200, 200, 200), width=2)
        d.ellipse([tip[0] - 16, tip[1] - 16, tip[0] + 16, tip[1] + 16], fill=(255, 255, 255), outline=(200, 200, 200), width=2)
        d.ellipse([tip[0] - 9, tip[1] - 9, tip[0] + 9, tip[1] + 9], fill=(130, 200, 150))

    def icons(self, im, t):
        d = ImageDraw.Draw(im)
        items = []
        # susu UHT
        items.append(("Susu UHT\nfull cream", lambda x, y: (d.rounded_rectangle([x + 40, y + 10, x + 120, y + 150], radius=10, fill=(255, 255, 255), outline=C("ink"), width=4),
                                                           d.rectangle([x + 42, y + 12, x + 118, y + 52], fill=(59, 125, 216)),
                                                           d.text((x + 80, y + 100), "UHT", font=font("body800", 24), fill=C("ink"), anchor="mm"))))
        items.append(("Pewarna\nmakanan", lambda x, y: [(d.rounded_rectangle([x + 12 + i * 36, y + 60, x + 42 + i * 36, y + 150], radius=8, fill=DYES[i]),
                                                          d.polygon([(x + 18 + i * 36, y + 60), (x + 36 + i * 36, y + 60), (x + 27 + i * 36, y + 30)], fill=DYES[i]))
                                                         for i in range(4)]))
        items.append(("Sabun cuci\npiring", lambda x, y: (d.rounded_rectangle([x + 45, y + 45, x + 115, y + 150], radius=16, fill=(126, 196, 150), outline=C("sage-ink"), width=4),
                                                          d.rectangle([x + 70, y + 20, x + 90, y + 45], fill=C("sage-ink")),
                                                          d.rectangle([x + 70, y + 20, x + 112, y + 30], fill=C("sage-ink")))))
        items.append(("Cotton bud", lambda x, y: (d.line([x + 30, y + 130, x + 130, y + 40], fill=(235, 235, 235), width=10),
                                                  d.ellipse([x + 16, y + 118, x + 44, y + 146], fill=(255, 255, 255), outline=(200, 200, 200), width=2),
                                                  d.ellipse([x + 116, y + 26, x + 144, y + 54], fill=(255, 255, 255), outline=(200, 200, 200), width=2))))
        items.append(("Piring\nputih", lambda x, y: (d.ellipse([x + 15, y + 25, x + 145, y + 155], fill=(255, 255, 255), outline=C("line"), width=4),
                                                     d.ellipse([x + 35, y + 45, x + 125, y + 135], outline=(238, 232, 224), width=3))))
        cell_w, cell_h = 270, 270
        for i, (label, draw) in enumerate(items):
            p = back_out((t - 0.2 - i * 0.22) / 0.4)
            if t - 0.2 - i * 0.22 <= 0:
                continue
            col, row = i % 3, i // 3
            x = LEFT + col * cell_w + (0 if row == 0 else cell_w / 2)
            y = 470 + row * 330
            card = Image.new("RGBA", (240, 300), (0, 0, 0, 0))
            cd = ImageDraw.Draw(card)
            cd.rounded_rectangle([0, 0, 239, 299], radius=28, fill=C("surface-card") + (255,), outline=C("line") + (255,), width=3)
            im_card = card
            sc = max(0.01, p)
            # draw icon directly on main image inside the card area after pasting card
            c2 = im_card.resize((max(1, int(240 * sc)), max(1, int(300 * sc))), Image.LANCZOS)
            im.alpha_composite(c2, (int(x + (240 - c2.width) / 2), int(y + (300 - c2.height) / 2)))
            if p > 0.8:
                draw(x + 40, y + 20)
                for j, line in enumerate(label.split("\n")):
                    d.text((x + 120, y + 214 + j * 34), line, font=font("body700", 28), fill=C("ink"), anchor="mm")

    # ---------- scenes
    def scene(self, im, name, t):
        if name == "judul":
            self.headline(im, "Susu bisa nari?", t, y=300, size=110)
            self.plate(im)
            self.ink(im, self.parts.p0, self.parts.col, alpha=ease_out((t - 0.4) / 0.6))
            self.host(im, "mikir", t - 0.6)
            self.caption(im, "Yuk cari tahu bareng Tunas. Cuma 5 menit, bahannya dari dapur.", t - 1.0)
        elif name == "bahan":
            self.headline(im, "Siapin dulu", t)
            self.icons(im, t)
            self.host(im, "riset", t - 0.1)
            self.caption(im, "Susu harus full cream. Yang rendah lemak hampir nggak bereaksi.", t - 1.4)
        elif name == "tuang":
            self.headline(im, "1. Tuang susu tipis-tipis ke piring", t)
            self.plate(im, milk=ease_out((t - 0.3) / 1.4))
            self.host(im, "halo", t)
        elif name == "tetes":
            self.headline(im, "2. Teteskan 3 sampai 4 warna di tengah", t)
            self.plate(im)
            vis = np.clip((t - 0.3 - self.parts.drop * 0.45) / 0.3, 0, 1)
            self.ink(im, self.parts.p0, self.parts.col, visible=vis)
            self.host(im, "hore", t)
        elif name == "sabun":
            self.headline(im, "3. Celup cotton bud ke sabun, tempel di tengah", t)
            self.plate(im)
            self.ink(im, self.parts.p0, self.parts.col)
            self.host(im, "halo", t, x=720, y=420, w=200)
            self.cotton_bud(im, ease_out((t - 0.4) / 1.2))
            self.caption(im, "Tunas tempel pelan-pelan. Jangan diaduk, ya.", t - 0.6, y=1250, width=760)
        elif name == "kabur":
            self.headline(im, "Warnanya kabur!", t, size=110, col="accent-text")
            self.plate(im)
            k = min(len(self.sim) - 1, int(t * FPS))
            self.ink(im, self.sim[k], self.parts.col)
            self.host(im, "kaget", 1, x=720, y=420, w=200)
            self.cotton_bud(im, 1 - ease_out((t - 0.6) / 0.8))
            self.host(im, "hore", t - 1.2, x=600, y=1210, w=280)
        elif name == "kenapa":
            self.headline(im, "Kenapa bisa?", t)
            self.plate(im)
            k = min(len(self.sim) - 1, int((dict(SCENES)["kabur"] + t) * FPS))
            self.ink(im, self.sim[k], self.parts.col)
            self.host(im, "riset", t)
            self.caption(im, "Sabun bikin permukaan susu kendor dan narik-narik lemaknya. Warnanya ikut kebawa.", t - 0.3)
        elif name == "air":
            self.headline(im, "Kalau pakai air putih, bakal sama nggak?", t)
            self.plate(im, liquid=(232, 242, 251))
            self.ink(im, self.water.p0, self.water.col, alpha=0.9)
            self.host(im, "mikir", t, x=720, y=420, w=200)
            if t > 1.4:
                self.cotton_bud(im, ease_out((t - 1.4) / 0.8))
            self.caption(im, "Air nggak ada lemaknya, jadi warnanya diam aja.", t - 2.6, width=760)
        elif name == "tutup":
            self.headline(im, "Simpan buat main weekend", t, y=300, size=86)
            self.host(im, "hore", t, x=(W - 300) // 2, y=520, w=300)
            pf = font("display", 44)
            q = back_out((t - 0.6) / 0.4)
            if t > 0.6:
                d = ImageDraw.Draw(im)
                pw = d.textlength("SIMPAN", font=pf) + 120
                pill = Image.new("RGBA", (int(pw), 110), (0, 0, 0, 0))
                pd = ImageDraw.Draw(pill)
                pd.rounded_rectangle([0, 0, pw - 1, 109], radius=55, fill=C("terra-deep") + (255,))
                pd.text((pw / 2, 57), "SIMPAN", font=pf, fill=C("on-accent"), anchor="mm")
                sc = max(0.01, q)
                pill = pill.resize((max(1, int(pill.width * sc)), max(1, int(110 * sc))), Image.LANCZOS)
                im.alpha_composite(pill, (int(W / 2 - pill.width / 2), int(940 + (110 - pill.height) / 2)))
            self.caption(im, "Ditemenin orang dewasa. Susunya jangan diminum, ya.", t - 1.0, y=1110, width=820, size=36)
            f2 = ease_out((t - 1.4) / 0.4)
            if f2 > 0:
                layer = text_layer(["Sumber: Science Notes, Magic Milk Experiment"], font("body800", 26), 40, [C("sage-ink")],
                                   width=RIGHT - LEFT, align="center")
                paste_alpha(im, layer, (LEFT, 1290), f2)

    def frame(self, t):
        im = self.base()
        acc = 0.0
        for name, dur in SCENES:
            if t < acc + dur or name == SCENES[-1][0]:
                self.scene(im, name, t - acc)
                break
            acc += dur
        self.progress(im, t)
        return im.convert("RGB")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out", "e01-susu-warna-animasi.mp4")
    ep = Episode()
    n = int(TOTAL * FPS)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(ep.frame(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print(out, f"{TOTAL:.1f}s", n, "frames")


if __name__ == "__main__":
    main()
