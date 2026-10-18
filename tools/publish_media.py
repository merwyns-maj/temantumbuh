#!/usr/bin/env python3
"""Copy a rendered post's slides into the public media repo and push, then print their raw URLs.

Usage: python tools/publish_media.py <slug> <YYYY-MM-DD> [--media ../temantumbuh-media]
Renders first if out/<slug>/ is missing. Slides go to posts/<date>-<slug>/slide-N.jpg (JPEG, quality 92).
Only approved posts belong in the media repo: it is public.
"""
import glob
import os
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/merwyns-maj/temantumbuh-media/main/"


def main(args):
    slug, date = args[0], args[1]
    media = args[args.index("--media") + 1] if "--media" in args else os.path.join(os.path.dirname(ROOT), "temantumbuh-media")
    out = os.path.join(ROOT, "out", slug)
    if not glob.glob(os.path.join(out, "slide-*.png")):
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "render.py"), os.path.join(ROOT, "posts", slug + ".json")], check=True)
    rel = f"posts/{date}-{slug}"
    dest = os.path.join(media, rel)
    os.makedirs(dest, exist_ok=True)
    slides = sorted(glob.glob(os.path.join(out, "slide-*.png")), key=lambda p: int(p.rsplit("-", 1)[1].split(".")[0]))
    for old in glob.glob(os.path.join(dest, "slide-*.jpg")):
        os.remove(old)
    urls = []
    for i, p in enumerate(slides, 1):
        name = f"slide-{i}.jpg"
        Image.open(p).convert("RGB").save(os.path.join(dest, name), quality=92)
        urls.append(RAW + rel + "/" + name)
    git = ["git", "-C", media]
    subprocess.run(git + ["add", rel], check=True)
    if subprocess.run(git + ["diff", "--cached", "--quiet"]).returncode:
        subprocess.run(git + ["-c", "user.name=Merwyn", "-c", "user.email=merwyn.sebastian@gmail.com", "commit", "-qm", f"Slides: {date} {slug}"], check=True)
        subprocess.run(git + ["push", "-q", "origin", "main"], check=True)
    for u in urls:
        print(u)


if __name__ == "__main__":
    main(sys.argv[1:])
