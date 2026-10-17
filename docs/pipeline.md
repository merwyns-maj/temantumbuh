# Pipeline

How a TemanTumbuh post goes from idea to TikTok, and what runs on a schedule.

## Daily run (morning, Asia/Jakarta)

A scheduled cloud session opens this repo and:

1. Reads `posts/calendar.json` and picks the next post whose status is not yet `approved`. If the spec doesn't exist, it writes it from the calendar title, the series, the job and the research.
2. Runs `python tools/lint_copy.py` until there are zero errors.
3. Runs `python tools/render.py`, fixing copy whenever the renderer reports an overflow.
4. Scores the post: `python tools/score_post.py` for the machine half, plus the judged half written to `data/judged.json` following `.claude/skills/skor-konten/SKILL.md`. Anything under 70 is rewritten and scored again.
5. Builds the review sheet with `python tools/review_sheet.py out/review-<slug>.pdf posts/<slug>.json`, sends it to Merwyn with a push notification, and waits for his reply.
6. **On "approve":** sets the status to `approved` in the calendar, commits the spec, and hands the slides to scheduling (below). **On a change request:** edits, re-renders, re-scores and sends again.

Posting time: 19:00 WIB by default. Weekend posts go at 09:00, and the 12:00 slot gets tested now and then.

## Scheduling and publishing

- **Value posts:** scheduled through the Metricool connector once it is connected and linked to the TikTok account.
- **Affiliate posts:** uploaded as drafts. Merwyn adds the product link in the TikTok app and posts them himself; no API can attach the yellow basket.
- **Until Metricool is connected:** Merwyn posts manually from the rendered PNGs.

## Weekly runs

**Swipe file (research).** Collects 10 to 20 high-performing Indonesian parenting posts from what is reachable: news coverage, Threads, Instagram, search results, and any TikTok links Merwyn saves. Each entry records the link, hook, format, visible engagement and why it worked, in `research/swipe/YYYY-WW.md`. It produces ideas only. Nothing is reposted, and every idea is rewritten in our voice with our own sources.

**Product research (from week 3, or once the account nears 1,000 followers).** Follows `.claude/skills/riset-afiliasi/SKILL.md`. For every affiliate-eligible post in the next two weeks, it:
1. Shortlists 3 to 5 products from TikTok Shop and Shopee and checks the hard gates: no formula, SNI or BPOM present, age-safe, rating 4.6+.
2. Scores them with `python tools/score_product.py data/products.csv --post <slug>` (relevance, Rupiah per sale, demand, likely to convert, trust).
3. Attaches the top 1 or 2 to the post spec with `"products"` and `"affiliate": true`.

It also re-checks commission and stock on live affiliate posts. It needs Merwyn signed in to the TikTok Shop and Shopee affiliate dashboards (built-in browser), or an export from him; it never invents numbers.

**Calibration.** Once at least 10 posts have 7 days of data, pull views, likes, comments, shares and saves from Metricool or TikTok Analytics into `data/predictions.csv`. Then compare each post's predicted score with the real rate for its job and adjust the rubric, following section 4 of the `skor-konten` skill.

**Calendar refill.** Keep at least 10 days of specs ready ahead. Take ideas from the backlog, the swipe file and calendar moments (Hari Ayah 12 Nov, Hari Ibu 22 Des, the start of the school year, rainy season).

## Fact-checking

Facts verified on 17 Oct 2026:

- SD admission may not use a calistung test (Permendikdasmen No. 3 Tahun 2025 on SPMB; restated by Kemendikdasmen in May 2026).
- Eggs are a good protein but a weak source of absorbable iron. The protein post compares spinach with meat, liver and fish for iron.
