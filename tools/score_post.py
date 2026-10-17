#!/usr/bin/env python3
"""Score TemanTumbuh posts: machine half (40) plus judged half (60) from data/judged.json.

Usage:
  python tools/score_post.py posts/d02-potong-makanan.json
  python tools/score_post.py posts/d*.json --log      # also append to data/predictions.csv
Rubric: .claude/skills/skor-konten/SKILL.md
"""
import csv
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from lint_copy import lint, ERROR  # noqa: E402

SERIES_TAG = {"pintar": "#SeriAnakPintar", "mpasi": "#SeriMPASI", "main": "#SeriMainDiRumah",
              "sekolah": "#SeriSiapSekolah", "ayah": "#SeriAyahBaru", "ibu": "#SeriIbu"}
RECIPIENTS = r"pasangan|suami|istri|grup wa|nenek|kakek|pengasuh|teman|keluarga|ayah|yang nyuapin|yang jagain|guru|dm"
JUDGED_MAX = {"hook": 15, "job": 15, "relief": 10, "trust": 10, "fresh": 10}
EVERYDAY = r"\b(sendok|wadah|gelas|selimut|kardus|kertas|popok|telur|hati ayam|lele|anggur|sosis|lakban|timer|kursi|handuk|jepit|sedotan|playdough|kelengkeng|apel|wortel|botol|celana|kotak bekal|tv|hp|lampu|cermin|buku|gurita|bedong|baby walker|digendong|tamu|air minum|charger|grup wa|foto|teh|kucing|motor|lagu|mandi|koran|taplak|jam \d)\b"


def machine(spec):
    slides = spec.get("slides", [])
    cta = next((s for s in reversed(slides) if s.get("type") == "cta"), {})
    pill = cta.get("pill", "").upper()
    job = spec.get("job")
    notes, pts = [], 0

    job_ok = (job == "send" and re.search(r"KIRIM|TAG", pill)) or \
             (job == "save" and "SIMPAN" in pill) or \
             (job == "comment" and ("?" in " ".join(str(v) for v in cta.values()) or "KOMEN" in pill))
    if job_ok:
        pts += 8
    else:
        notes.append(f"CTA pill '{pill}' does not match job '{job}'")

    if job == "send":
        cta_text = " ".join(str(cta.get(k, "")) for k in ("pill", "sub2", "sub")).lower()
        if re.search(RECIPIENTS, cta_text):
            pts += 4
        else:
            notes.append("send post does not name who to send it to")
    else:
        pts += 4

    if 6 <= len(slides) <= 9:
        pts += 4
    else:
        notes.append(f"{len(slides)} slides; aim for 6 to 9")

    hook = slides[0] if slides else {}
    lines = hook.get("lines", [])
    if lines and len(lines) <= 4 and all(len(l) <= 15 for l in lines):
        pts += 4
    else:
        notes.append("hook over 4 lines or a line over 15 characters")

    issues = lint(spec)
    errs = [i for i in issues if i[0] == ERROR]
    if not errs:
        pts += 6
        if len(issues) == 0:
            pts += 2
        else:
            notes.append(f"{len(issues)} linter warning(s)")
    else:
        notes.append(f"{len(errs)} linter error(s)")

    needs_source = spec.get("series") in ("pintar", "mpasi") or any(s.get("disclaimer") for s in slides)
    if not needs_source or any(s.get("source") for s in slides):
        pts += 4
    else:
        notes.append("health or development post without a source line")

    cap = spec.get("caption", "")
    tags = re.findall(r"#\w+", cap)
    tag_ok = 3 <= len(tags) <= 5 and SERIES_TAG.get(spec.get("series"), "#") in tags
    if "?" in cap.split("#")[0] and tag_ok:
        pts += 4
    else:
        notes.append("caption needs a question and 3 to 5 hashtags incl. the series tag")

    points = [s for s in slides if s.get("type") in ("point", "punch")]
    specific = 0
    for s in points:
        text = " ".join(str(s.get(k, "")) for k in ("title", "body", "tips", "punch", "word"))
        if re.search(r"\d", text) or re.search(EVERYDAY, text, flags=re.IGNORECASE):
            specific += 1
    if points and specific >= len(points) / 2:
        pts += 4
    else:
        notes.append(f"only {specific}/{len(points)} point slides have concrete details")
    return pts, notes


def judged(slug, table):
    j = table.get(slug)
    if not j:
        return None, "not judged yet"
    total = sum(round(JUDGED_MAX[k] * j[k] / 5, 1) for k in JUDGED_MAX)
    return total, j.get("note", "")


def main(args):
    log = "--log" in args
    paths = [a for a in args if a != "--log"]
    jpath = os.path.join(ROOT, "data", "judged.json")
    table = json.load(open(jpath, encoding="utf-8")) if os.path.exists(jpath) else {}
    rows = []
    for p in paths:
        spec = json.load(open(p, encoding="utf-8"))
        slug = os.path.splitext(os.path.basename(p))[0]
        m, notes = machine(spec)
        jd, jnote = judged(slug, table)
        total = m + jd if jd is not None else None
        verdict = "-" if total is None else ("PRIORITY" if total >= 90 else "REVIEW" if total >= 70 else "REWRITE")
        print(f"{slug:28} machine {m:2}/40  judged {('%.0f' % jd) if jd is not None else ' -'}/60  "
              f"total {('%.0f' % total) if total is not None else ' -':>3}  {verdict}")
        for n in notes:
            print(f"    - {n}")
        if jnote:
            print(f"    > {jnote}")
        rows.append([slug, datetime.date.today().isoformat(), spec.get("series"), spec.get("job"), m,
                     "" if jd is None else round(jd), "" if total is None else round(total)])
    if log:
        out = os.path.join(ROOT, "data", "predictions.csv")
        new = not os.path.exists(out)
        with open(out, "a", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["slug", "scored_on", "series", "job", "machine", "judged", "total",
                            "posted_on", "views", "likes", "comments", "shares", "saves",
                            "shares_per_1k", "saves_per_1k", "comments_per_1k"])
            for r in rows:
                w.writerow(r + [""] * 9)
        print(f"logged {len(rows)} row(s) to {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
