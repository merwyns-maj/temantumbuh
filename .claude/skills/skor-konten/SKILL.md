---
name: skor-konten
description: Score every TemanTumbuh post out of 100 before it goes to Merwyn for review, rewrite anything under 70, and log the prediction so it can be checked against real TikTok numbers later. Use after the copy passes the linter and before rendering for review.
---

# Skor konten

A post is only as good as the one job it does. Every post declares **one** job in its spec (`"job"`):

- **send**: the viewer forwards it or tags someone (pasangan, grup WA keluarga, nenek atau pengasuh, grup WA sekolah)
- **save**: the viewer saves it to use later (checklist, per-usia guide, menu, phrases)
- **comment**: the viewer answers in the comments (shared-struggle questions, A-or-B dilemmas)

The weights below come from `research/parenting-content-research.md` (17 Oct 2026). They are a starting point. Section 4 says how to re-weight them from real results.

## 1. Two halves, 100 points

`python tools/score_post.py posts/<slug>.json` prints the **machine half (40 points)**: things a script can check. You add the **judged half (60 points)** in `data/judged.json` after reading the rendered slides like a parent scrolling at 9 pm.

### Machine half (40), computed by the script

| Check | Points |
| --- | --- |
| A job is declared, and the CTA pill matches it (send: KIRIM or TAG; save: SIMPAN; comment: a question on the last slide or in the pill) | 8 |
| The CTA names who to send it to (pasangan, suami, grup WA, nenek, pengasuh, teman yang lagi hamil...) for a send post | 4 |
| 6 to 9 slides | 4 |
| Hook: 4 lines or fewer, each 15 characters or fewer | 4 |
| Linter: zero errors (6), zero warnings (2) | 8 |
| Health or development post (pintar, mpasi, or anything with a disclaimer) carries a source line | 4 |
| Caption ends with a question and has 3 to 5 hashtags including the series tag | 4 |
| Specific details: digits, times, prices or named everyday objects appear in at least half the point slides | 4 |

### Judged half (60), by you

Score each, using the anchors. Be strict: a 3 out of 5 is a normal post.

| Criterion | Max | 5 looks like | 1 looks like |
| --- | --- | --- | --- |
| **Hook stops the thumb** | 20 | A flat statement that tells the parent something they did not expect, with concrete words: reassurance ("Kamu udah stimulasi anak tiap hari", 31k views), a new rule ("Masuk SD nggak ada tes calistung", 3.3k), gentle myth-busting ("Bukan salah Nenek. Ilmunya aja yang udah update", 4.7k), named objects ("Anggur, sosis, kelengkeng. Potongnya jangan bulat", 3.4k) | Topic label or a bare question ("Anakmu GTM lagi?", 212; "Tummy time nggak harus sambil nangis", 273) |
| **Does its one job** | 10 | You can name the exact person it gets sent to, or why it gets saved, or the comment people will write | It is fine but nobody would forward it |
| **Relief, not guilt** | 10 | Leaves parents calmer or laughing ("bukan salah kamu", "ternyata normal") | Lists everything they are doing wrong |
| **Trust and safety** | 10 | Claims are soft and sourced; no formula promotion; nobody is shamed; humour makes the dad the joke and the mom the hero | A promise ("bikin pintar"), a jab at mertua, a complaining husband |
| **Fresh** | 10 | A calendar or news peg, or an angle not already everywhere | Saturated topic told the usual way (tanda siap MPASI as a plain list) |

Multiply each judged criterion score (1 to 5) by its max divided by 5.

### Thresholds

- **90 and up**: priority slot (Monday or Friday prime time).
- **70 to 89**: goes to review.
- **Under 70**: rewrite before Merwyn sees it. Fix the lowest criterion first; usually it is the hook or the job.

## 2. What to put in data/judged.json

```json
{"d02-potong-makanan": {"hook": 5, "job": 5, "relief": 3, "trust": 5, "fresh": 4,
  "note": "News peg handled gently; strongest forward-to-caregiver post."}}
```

The note is one line on the weakest point. It is shown under the contact sheet in the review.

## 3. Log the prediction

`python tools/score_post.py posts/*.json --log` appends one row per post to `data/predictions.csv` (slug, date, series, job, machine, judged, total). After posting, the weekly job fills the actual columns from Metricool or TikTok Analytics: views, likes, comments, shares, saves, and the rates per 1,000 views.

## 4. Calibrate every week

After at least 10 posts have 7 days of data (96% of reach happens in the first 10 days):

1. For each job, compare the predicted total with the matching real rate: send posts with shares per 1,000 views, save posts with saves per 1,000 views, comment posts with comments per 1,000 views.
2. Look for criteria that do not track reality. If posts with hook 5 do no better than hook 3, the hook anchors are wrong, not the audience: rewrite the anchors with real examples from our own top posts.
3. Move at most 5 points between criteria per week, so one viral fluke does not wreck the rubric.
4. Write what changed and why at the bottom of this file, with the date.

## 5. Calibration log

- 2026-10-17: initial weights from the research report. No real data yet.
- 2026-10-28: first calibration, 13 TikTok posts (lifetime views from Tebar). Spearman with views: total score 0.36, hook 0.43, fresh 0.28, relief 0.07, job -0.11, trust -0.13. Moved 5 points from job (15 to 10) to hook (15 to 20) and rewrote the hook anchors with our own top and bottom posts. Caveat: the account's daily views fell from 25k (17 Oct) to under 1k (22 Oct onward) for every post, so post date is a confounder; the dad series sits in the bottom group whatever its hook. Not yet changed: audience breadth (re-check next week with the 0 to 3 focus posts).
