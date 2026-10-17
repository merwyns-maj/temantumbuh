# TemanTumbuh

Content factory for **TemanTumbuh**, a faceless Indonesian parenting channel on TikTok (photo carousels, 1080 × 1440) for parents of children from newborn to SD. Five series: Seri Anak Pintar, Seri MPASI, Seri Main di Rumah, Seri Siap Sekolah, Seri Ayah Baru.

Every post is a JSON spec. The tools turn it into slides that follow the design system, check the copy, score it, and build a review sheet.

## Quick start

```bash
pip install -r requirements.txt
python tools/lint_copy.py posts/d02-potong-makanan.json      # voice + compliance check
python tools/render.py posts/d02-potong-makanan.json         # slides -> out/d02-potong-makanan/
python tools/score_post.py posts/d*.json                     # score out of 100
python tools/review_sheet.py out/review.pdf posts/d*.json    # one page per post, for review on a phone
```

## Folders

| Path | What |
| --- | --- |
| `posts/` | One JSON spec per post, plus `calendar.json` (30 days, series rhythm, backlog) |
| `backlog/` | Drafts parked for a later day |
| `design/` | `tokens.json` from the TemanTumbuh Design System, logo and series icons (SVG) |
| `fonts/` | Fredoka 600 and Nunito 600/700/800 (SIL Open Font License) |
| `tools/` | `render.py`, `lint_copy.py`, `score_post.py`, `review_sheet.py` |
| `.claude/skills/` | `suara-temantumbuh` (voice and humanify rules), `skor-konten` (post score), `riset-afiliasi` (product research and score) |
| `data/` | `judged.json` (judged half of the score), `predictions.csv` (prediction log, actual metrics added after posting), `products.csv` (affiliate candidates; the three rows marked [contoh] are examples) |
| `research/` | Content research that the rubric and calendar are built on |
| `docs/pipeline.md` | How the daily and weekly runs work |
| `out/` | Rendered slides and review PDFs (not committed) |

## A post spec, in short

```json
{
  "series": "mpasi",            // pintar | mpasi | main | sekolah | ayah
  "job": "send",                // send | save | comment: the one thing this post must get people to do
  "usia": "BAYI DAN BALITA",    // age chip on the hook slide (optional)
  "caption": "... ending with a question? #mpasi #SeriMPASI",
  "slides": [
    {"type": "hook", "kicker": "...", "lines": ["...", "..."], "accent": 1, "sub": "...", "theme": "dark"},
    {"type": "point", "title": "...", "body": "...", "tips": "...", "usia": "6-12 BULAN"},
    {"type": "point", "label": "KATA ORANG DULU", "title": "\"...\"", "tips_label": "KATA DOKTER ANAK SEKARANG", "tips": "..."},
    {"type": "punch", "word": "NGANTUK", "punch": "...", "zzz": true},
    {"type": "cta", "headline": "...", "accent": "...", "pill": "KIRIM KE ...", "sub2": "...",
     "source": "Sumber: ...", "disclaimer": true}
  ]
}
```

The renderer refuses to draw a slide whose text would overflow or collide, and says which words to cut.
