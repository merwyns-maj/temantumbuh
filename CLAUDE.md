# TemanTumbuh: instructions for Claude sessions

You are producing content for TemanTumbuh, a faceless Indonesian parenting channel on TikTok. The owner is Merwyn; he reviews every post before it goes out.

## Rules that never bend

1. **Voice:** follow `.claude/skills/suara-temantumbuh/SKILL.md`. Spoken Indonesian (kamu, nggak, udah), no em or en dashes, no AI openers, no "Bunda" alone. `tools/lint_copy.py` must report zero errors.
2. **Score gate:** follow `.claude/skills/skor-konten/SKILL.md`. Nothing under 70 reaches Merwyn; rewrite it first.
3. **One job per post:** `"job"` is save, send or comment, and the CTA pill must match it.
4. **Safety and claims:**
   - Health, development and MPASI content follows IDAI, Kemenkes or WHO, carries a `source` line on the last slide, and keeps the disclaimer.
   - No promises ("bikin pintar", "pasti", "dijamin").
   - Never promote formula or other breast-milk substitutes (PP 28/2024).
   - Affiliate posts disclose in the caption (#iklan or "link afiliasi").
5. **Tone:** no mom-shaming, no husband-bashing, no mertua wars. In humour, the dad laughs at himself and the mom is the hero. Old beliefs are corrected kindly ("bukan salah Nenek").
6. **Originality:** never copy or repost other creators' slides, videos or text. Ideas from the swipe file are rewritten in our voice with our own sources. No real faces, no character IP, and no photorealistic AI people (TikTok requires an AI label for those).
7. **Design:** colours, type and spacing come from `design/tokens.json` through `tools/render.py`. Do not hand-draw slides.

## Workflow

See `docs/pipeline.md`. In short: draft spec → lint → render → score (machine half + judged half in `data/judged.json`) → review sheet to Merwyn → on approval, move to scheduling.

## Verify, don't recall

Before stating a fact about the world on a slide (a regulation, a guideline, a statistic), look it up and name the source. When unsure, soften the claim or leave it out.
