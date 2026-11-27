#!/usr/bin/env python3
"""Turn rendered carousel slides + a voiceover into a 9:16 voiced video (MP4 with audio).

Usage: python tools/voice_reel.py <reel.json> <out.mp4> [--frames t1,t2,...]

reel.json:
  slides_dir   folder with slide-1.png ... (from tools/render.py, 1080x1440)
  voice        mp3 voiceover
  sting        optional mp3 played after the voice (series signature)
  segments     [{"slide": 1, "start": 0.0}, ...]  slide shown from start until the next one
  captions     [{"t": 0.0, "text": "..."}, ...]   burned-in caption from t until the next one
  end_hold     seconds the last slide stays after the voice (covers the sting), default 3
Layout: slide scaled to 0.82 and centred high, gentle zoom, 0.25 s crossfade between slides;
captions in a dark pill above the bottom safe line (y 1500), left of the right button rail.
--frames writes PNG stills at those times instead of encoding (for checking).
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import color, font, wrap  # noqa: E402

W, H, FPS = 1080, 1920, 30
SCALE = 0.82
FADE = 0.25
BG = color("surface-100", "light")
INK = color("ink", "light")
TERRA = color("terra", "light")


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


class Reel:
    def __init__(self, cfg, base):
        self.cfg = cfg
        d = os.path.join(base, cfg["slides_dir"]) if not os.path.isabs(cfg["slides_dir"]) else cfg["slides_dir"]
        self.slides = {}
        for s in cfg["segments"]:
            n = s["slide"]
            if n not in self.slides:
                im = Image.open(os.path.join(d, f"slide-{n}.png")).convert("RGB")
                self.slides[n] = im
        self.voice_len = dur(cfg["voice"])
        self.total = self.voice_len + cfg.get("end_hold", 3.0)
        self.segs = cfg["segments"]
        self.caps = cfg["captions"]
        self.cap_font = font("body800", 54)
        self.cache = {}

    def seg_at(self, t):
        idx = 0
        for i, s in enumerate(self.segs):
            if t >= s["start"]:
                idx = i
        return idx

    def slide_frame(self, idx, t):
        s = self.segs[idx]
        end = self.segs[idx + 1]["start"] if idx + 1 < len(self.segs) else self.total
        p = (t - s["start"]) / max(0.1, end - s["start"])
        z = SCALE * (1.0 + 0.035 * p)
        im = self.slides[s["slide"]]
        w, h = int(im.width * z), int(im.height * z)
        key = (s["slide"], w)
        if key not in self.cache:
            self.cache[key] = im.resize((w, h), Image.LANCZOS)
        return self.cache[key]

    def frame(self, t):
        canvas = Image.new("RGB", (W, H), BG)
        idx = self.seg_at(t)
        cur = self.slide_frame(idx, t)
        cx, top = 490, 190  # centre a bit left of the right button rail
        canvas.paste(cur, (int(cx - cur.width / 2), top))
        start = self.segs[idx]["start"]
        if idx > 0 and t - start < FADE:
            prev = self.slide_frame(idx - 1, t)
            a = 1 - (t - start) / FADE
            layer = canvas.copy()
            layer.paste(prev, (int(cx - prev.width / 2), top))
            canvas = Image.blend(canvas, layer, a)
        self.caption(canvas, t)
        return canvas

    def caption(self, canvas, t):
        if t > self.voice_len + 0.1:
            return
        text = None
        for c in self.caps:
            if t >= c["t"]:
                text = c["text"]
        if not text:
            return
        d = ImageDraw.Draw(canvas)
        lines = wrap(d, text, self.cap_font, 780)
        lh = 66
        bh = lh * len(lines) + 36
        y0 = 1490 - bh
        x0, x1 = 70, 910
        d.rounded_rectangle((x0, y0, x1, y0 + bh), radius=34, fill=INK)
        for i, ln in enumerate(lines):
            tw = d.textlength(ln, font=self.cap_font)
            d.text(((x0 + x1 - tw) / 2, y0 + 14 + i * lh), ln, font=self.cap_font, fill=(255, 255, 255))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cfg_path, out = args[0], args[1]
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    base = os.getcwd()
    r = Reel(cfg, base)
    if "--frames" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]
        os.makedirs(out, exist_ok=True)
        for t in ts:
            r.frame(t).save(os.path.join(out, f"f{t:05.2f}.png"))
        print("frames", len(ts))
        return
    tmp = out[:-4] + ".part.mp4"
    n = int(r.total * FPS)
    audio = ["-i", cfg["voice"]]
    filt = "[1:a]apad[a]"
    if cfg.get("sting"):
        audio += ["-i", cfg["sting"]]
        delay = int((r.voice_len + 0.2) * 1000)
        filt = f"[2:a]adelay={delay}|{delay},volume=0.8[s];[1:a][s]amix=inputs=2:duration=longest:normalize=0[a]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-"] + audio + ["-filter_complex", filt, "-map", "0:v", "-map", "[a]", "-t", f"{r.total:.2f}",
           "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(r.frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit("ffmpeg failed")
    os.replace(tmp, out)
    print("ok", out, f"{r.total:.1f}s")


if __name__ == "__main__":
    main()
