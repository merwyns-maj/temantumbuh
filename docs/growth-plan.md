# Growth plan: 22 Oct to 4 Nov 2026

Goal: more views, engagement and followers on TikTok (Instagram stays second).
Owner: Merwyn approves content. Claude runs the tests, the numbers and the schedule.

## 1. Where we are (TikTok, as of 21 Oct 22:00 WIB)

| Post | Series | Score | Views | Likes /1k | Shares /1k |
| --- | --- | --- | --- | --- | --- |
| d01 Stimulasi | pintar | 88 | 26,983 | 54 | 13.5 |
| d04 Mitos bayi | pintar | 96 | 4,612 | 33 | 3.7 |
| d02 Potong anggur | mpasi | 96 | 3,304 | 40 | 0.9 |
| d11 Siap SD | sekolah | 95 | 3,100 | 49 | 8.1 |
| d03 Mainan dapur | main | 86 | 1,342 | 37 | 1.5 |
| d07 Ayah, part 2 | ayah | 93 | 411 | 29 | 7.3 |
| d05 Keluhan suami | ayah | 91 | 362 | 41 | 5.5 |
| s01 Stiker WA | ayah | 93 | 279 | 50 | 7.2 |

- 8 posts, about 44,000 views, median 2,200 per post.
- Followers: 54 (17 Oct) to 106 (20 Oct), about 17 a day. That is roughly 2.4 followers per 1,000 views, which is low: people watch but do not follow.
- d31 (7 indra) was posted by hand on 21 Oct, so it is not in Metricool yet.
- Instagram is too small to read (single-digit reach on most posts, Stories at zero).

What the data says:
1. **The dad series is narrow, not bad.** Its share rate is fine (5 to 7 per 1k), but TikTok never pushes it past the first small audience. Most parenting viewers are moms, and these posts speak to dads.
2. **Practical 0 to 3 topics with a calming hook win.** d01, d04 and Siap SD all reassure ("kamu udah", "bukan salah Nenek", "nggak boleh ada tes calistung").
3. **Our score does not predict views yet.** Every post scored 86 to 96, so the score cannot tell them apart. Spearman between total score and views is 0.23 across 8 posts (noise). The hook criterion tracks views best (0.51). The "does its one job" criterion goes the wrong way (-0.39), because the dad posts got 5/5 on it and then flopped.
4. **We cannot see saves, watch time or traffic sources for photo posts** through Metricool. TikTok Studio shows them.

## 2. Constraint: Metricool free plan

20 published posts a month, reset on the 1st. October is used up, so **Merwyn posts by hand until 1 Nov**. Claude sends the slides and caption at 17:30 for a 19:00 post (and at 10:30 for a 12:00 post).
Even after the reset, 20 a month is under one TikTok post a day. Upgrading to Starter (about US$20 to 25 a month) is the decision to make by 1 Nov if we want daily or twice-daily posting.
Saving quota: no more Instagram Stories until they show reach.

## 3. Tests (one variable at a time)

With about 8 posts a week, only big differences are real. Rules:
- Compare **rates per 1,000 views** (likes, shares, comments, follows) and **views at 48 hours**, not lifetime views.
- Same slot and the same kind of topic on both sides.
- Call a winner only at **2x or more** difference, with at least 3 posts per side. Anything smaller is "no difference yet".

### Test A: short video vs carousel (22 Oct to 4 Nov)
- Video side: recut our best carousels into 15 to 25 second videos with `tools/recut.py`, plus the animated Tunas experiments. Posted at 12:00, TikTok only.
  1. Thu 22 Oct 12:00: d01 Stimulasi video
  2. Sat 24 Oct 09:00: e01 Susu bisa nari (animated)
  3. Tue 27 Oct 12:00: d04 Mitos bayi video
  4. Thu 29 Oct 12:00: d11 Siap SD video
- Carousel side: the 19:00 posts the same weeks.
- Extra for videos only: TikTok gives average watch time and full-watch rate. Target over 40% full-watch.
- Decision on 4 Nov: if videos get 2x the 48-hour views or follows per 1k, they get a daily slot.

### Test B: hooks (29 Oct to 4 Nov)
- For the two video posts that week, make two first frames (calming hook vs problem hook, e.g. "Kamu udah stimulasi anak" vs "Takut anakmu kurang stimulasi?").
- Run both as Instagram Trial Reels (shown to non-followers only, so there's no duplicate post on the feed). TikTok gets the winner a day later.
- Record the result in the hook anchors of the score rubric.

### Test C: follow CTA on series posts (from 26 Oct)
- Every other post in a series ends with "Follow buat Seri Anak Pintar bagian berikutnya". Compare followers gained per 1,000 views with posts that end with the usual save or send CTA.

## 4. Focus and content mix (proposed, from 22 Oct)

**Focus on one segment: parents of children aged 0 to 3, mostly moms.** It is where all our top posts sit. TikTok also learns faster who to show us to when every post speaks to the same person, and it is the best fit for affiliate products (newborn list, toys, MPASI tools).

- 60% Seri Anak Pintar (stimulation, development, myths)
- 25% Seri MPASI (safety, menus, GTM). No formula, bottles or teats (PP 28/2024).
- 15% Seri Main di Rumah for 1 to 3 (save posts, video-friendly experiments)
- Paused: Seri Ayah Baru (carousels) and Seri Siap Sekolah. Siap Sekolah comes back in January for the SPMB season.

Alternatives considered:
- MPASI only: big search demand, but more claim risk and a narrower age window (6 to 24 months).
- Siap Sekolah (3 to 6): fits the worksheet lane, but it is seasonal and only one post so far.
- **Dad series:** stop it as carousels. Bring it back as a short, funny video once Test A shows videos work. It is still useful as a send-to-partner post, so keep the sticker pack link in the bio.
- Turn good comment questions into **reply-with-video** answers (e.g. "d01 ini untuk umur berapa?"). They are cheap to make, TikTok shows them to people who saw the original post, and they reward the commenter.

## 5. Followers and engagement

- Profile (Merwyn does this on his phone):
  - Bio: "Ide main dan tips anak 0 sampai 5 tahun. Sumber IDAI dan WHO. Stiker WA gratis di bawah."
  - Pin d01, d04 and Siap SD.
- Reply to every comment within the first hour after posting. Claude drafts replies on request (batch is fine).
- End questions with numbered choices ("ketik nomornya"). This is the easiest comment to write.
- Post every day at the same time, so people learn when we show up.

## 6. Score calibration

- **28 Oct (planned):** about 12 posts will have 7 days of data. Run section 4 of `skor-konten`. Proposed changes, at most 5 points moved:
  - Add **Audience breadth** (who stops: all parents of 0 to 5 vs one narrow group).
  - Take the points from **Does its one job** (15 to 10). It rewarded the dad posts that did not get reach.
  - Tighten the anchors so a normal post scores around 70, not 90. Use d01 and d04 as the 5/5 hook examples.
- From then on, each week: fill the actual columns of `data/predictions.csv` from Metricool. Merwyn sends one TikTok Studio screenshot per week (saves and watch time) on Monday.

## 7. Targets for 4 Nov (vs today)

| Metric | Now | Target |
| --- | --- | --- |
| Median views per TikTok post (48h) | about 2,200 | 3,000 |
| Followers | 106 | 300 |
| Followers per 1,000 views | 2.4 | 4 |
| Shares per 1,000 views on send posts | 5.5 median | 6 |
| Score vs views (Spearman) | 0.23 | 0.5 |

## 8. Decisions (Merwyn, 21 Oct)

1. Focus on parents of 0 to 3: yes.
2. Short video at 12:00 from Thu 22 Oct: yes. The d01 video (20.6 s) was sent for review.
3. d12 "Kamus suami" stays on Fri 23 Oct as the last dad-series carousel.
4. Metricool Starter: try it for 1 month (monthly billing), then review against the 4 Nov results.
5. Bio and pins: TikTok pins are d01, d04 and d02 (all 0 to 3). The sticker link goes in the TikTok bio as text and in the Instagram link field.

## 9. Test D: two posts a day (2 to 15 Nov, agreed 29 Oct)

- 12:00 "Contekan Cepat": 3 to 4 illustrated slides, one practical tip to save (0 to 3 focus, source on the last slide, score 70+). If one is not good enough, that day has one post.
- 19:00 full carousel as now.
- Both via Tebar, TikTok Public, auto music. Merwyn approves the whole week in one batch on Saturday.
- Judge on 15 Nov: median views per slot, whether 19:00 posts drop after noon posts start, followers per week vs 27 Oct to 1 Nov. Keep two a day if the total rises and 19:00 holds.
- Needs Tebar Starter (Rp17,900) after the Pro trial ends around 9 Nov: Free allows 30 posts a month.

Topic plan, week of 2 Nov:
- 19:00: d21 kirim ke pengasuh, d22 jawaban sopan "kok kurus?", d27 buku per usia, d29 18 bulan belum ngomong (IDAI/KPSP), d23 alat MPASI kepake vs pajangan, d24 mainan 100 cara, d15 screen time (WHO).
- 12:00 Contekan: tanda bayi kenyang, porsi MPASI per usia, cek suhu air mandi, posisi tidur aman, gigi pertama, nenangin bayi nangis malam, demam: kapan ke dokter.

## 10. Review, 4 Nov (Tebar numbers, synced 4 Nov 08:39 WIB)

| Metric | Before (21 to 26 Oct) | Since 27 Oct | Target 4 Nov |
| --- | --- | --- | --- |
| Median views per post (lifetime) | 227 (7 posts) | 608 (10 posts) | 3,000 |
| Followers | 117 (21 Oct) | 168 (4 Nov) | 300 |
| New followers per day | 2.9 | 4.9 | |
| Followers per 1,000 views | 2.8 | 3.2 | 4 |

- Organic is rising: median views up about 2.7x since the illustrated v2 design and the new hooks. Targets for 4 Nov are missed (they assumed the launch-week pace).
- Best post since launch week: w2n gigi pertama (Contekan, 12:00), 5,588 views in under a day, 15.5x the account's usual. The first two noon Contekan posts both beat the 19:00 carousels of the same days (1,142 and 5,588 vs 562 and 556). Early, not yet a result: Test D is judged on 15 Nov.
- Promote: skipped for now, per the rule agreed 29 Oct (organic is rising). Revisit on 15 Nov with Test D.

## 11. Review, 16 Nov: Test D verdict (Tebar numbers, synced 16 Nov 07:31 WIB)

Views are lifetime views at the sync. The baseline posts are 15 to 20 days old, while Test D posts are between half a day and 14 days old, so newer posts are understated. Posts from 14 and 15 Nov are still climbing. The account-level daily views in Tebar lag by a few days (they do not include most of the 14 Nov hit yet), so per-post views are used below.

| Metric | Baseline: 27 Oct to 1 Nov, one post a day | Test D: 2 to 15 Nov, two a day |
| --- | --- | --- |
| Median views, 19:00 post | 610 (6 posts) | 621 (14 posts); week 1: 636, week 2: 415 |
| Median views, 12:00 post | n/a | 273 (14 posts); week 1: 830, week 2: 217 |
| Median views per day, both posts | 623 | 1,466 |
| New followers per week | +37 (26 Oct to 2 Nov) | +16 (2 to 9 Nov), +49 (9 to 16 Nov) |
| Followers | 130 (26 Oct) | 232 (16 Nov) |

- **Verdict: keep two a day, with a watch on noon.** Both rules agreed on 29 Oct are met: total views per day more than doubled, and the 19:00 slot held (621 vs 610; week 1 at similar ages was 636).
- **Noon faded in week 2.** In week 1 the noon post beat the 19:00 post on 4 of 7 days. In week 2 it won on only 1 of 7, and the noon median dropped from 830 to 217. Week 2's noon topics were narrower newborn issues (late teeth, kaki O, ruam popok, kepala peyang, cegukan, ASIP). Format and slot are still confounded: in the one swap (7 Nov), the short post at 19:00 got 2,199 and the long one at noon got 230. Week 4 (Test E: format swapped on Tue, Thu and Sat) separates them.
- **Hits, not volume, drive growth.** Three posts made 79% of Test D views: gelar dokter anak (73,300, 19:00 long), gigi pertama (23,238, 12:00 short) and kata pertama (10,981, 19:00 long). All three are reference posts with age or milestone ranges, or a decoder of something parents see but can't read. Without the hits, the median post did about 415 views.
- **Followers didn't scale with views.** Gelar dokter anak got 73,300 views and 25 follows (0.3 per 1,000 views). The hits reach non-followers who save and leave. Weekly follower gain averaged 32.5 vs 37 at baseline.
- **Promote: still skip.** Reach isn't the bottleneck (organic hits reached 73k); conversion is. Fix the profile and pinned posts first (pin the three hits, plus a bio line that names the series), then retest. Revisit on 30 Nov.
- **Persona panel, forward check** (results in data/panel/results_2026-11-16.txt). On the 16 posts judged before they went out, Spearman vs views was panel +0.44 and skor-konten +0.57. Within one slot it drops to panel +0.00 (19:00) and +0.38 (12:00), and skor-konten +0.15 and -0.35. So most of the signal is just "19:00 long beat 12:00 short this week". The panel ranked kata pertama 3rd and gelar 8th of 16. Neither the panel nor skor-konten spots a hit yet.
- **skor-konten change (proposed):** add a "topic type" item worth about 20 points: a reference post a parent will come back to (age or milestone ranges, decoding a label, a referral path) scores high; opinion or myth lists score low. Take the points from the hook-craft items, which showed no signal within a slot. Leave slot and format weights alone until Test E ends on 22 Nov.
