# Handoff: Tunas YouTube kids channel

From the TemanTumbuh session, 16 Nov 2026. Drop this into the new project as its starting brief.

## 1. Goal

A second revenue stream next to the TemanTumbuh TikTok channel: a **YouTube channel of short, slow-paced animated social stories** for Indonesian children aged 2 to 5, watched together with a parent.

- **The job of each episode:** walk a child calmly through something they find hard. Examples: imunisasi, minum obat, tidur lebih awal, sikat gigi, potong rambut, ke dokter gigi, hari pertama sekolah.
- **The tone:** slow, honest, warm, with few words and long holds. Music and pictures carry the feeling, not narration.
- **Why it works:** parents search for this at the moment of need ("anak takut disuntik"). Social stories are an established approach for preparing children, and slow pacing suits YouTube Kids and parents who avoid hyper-stimulating cartoons.
- **The link to TemanTumbuh:** same mascot, same voice rules, same safety rules. TikTok can later carry cut-downs of each episode.

## 2. Format

- **Length:** 40 s pilot tests so far. The target is 2 to 4 minutes per episode, plus Shorts cut from it.
- **Language:** Indonesian, spoken register ("nggak", "udah"), short sentences a toddler can follow.
- **Voice:** an **AI Indonesian child voice** (Merwyn's choice). The plan is ElevenLabs, which Merwyn signs up for himself; never paste keys into chat. The current tests use a robotic espeak-ng placeholder.
- **Subtitles:** burnt in, large, in the Fredoka font. *To fix: add a soft backing so subtitles read on light floors.*
- **YouTube setting:** "made for kids" = yes (COPPA). That means no personalised ads and no comments, which lowers the revenue per view. Plan revenue around volume, Shorts and a later product (printables or books), not ads alone.

## 3. Story template (social story)

Every episode follows the same arc, so children learn the pattern:

1. **Setup:** what's going to happen today, said plainly ("Hari ini, Tunas mau imunisasi.").
2. **Feeling:** name the worry and allow it ("Tunas agak deg-degan. Nggak apa-apa.").
3. **Support:** a grown-up is there (Mama holds his hand).
4. **The moment:** honest about what it feels like ("Rasanya sakit sebentar. Boleh nangis."). Use a beat of silence, then the moment itself.
5. **Why it helps:** one simple, sourced reason ("Imunisasi bantu badan Tunas melawan kuman.").
6. **Ending:** warmth and pride ("Tunas hebat!"), a hug, and a slow pull back.

## 4. Characters

All are TemanTumbuh originals. Use no character IP and no real or photoreal faces.

| Character | Look | Role |
|---|---|---|
| **Tunas** (main) | A round peach seed-child (#f6c9a5) with a two-leaf green sprout on top (#6fbf5a) and big simple eyes. Has four expressions: senang, cemas, meringis, lega. Blinks. Can wear a plaster. | The child. Small and a bit nervous, but he gets through it. |
| **Mama** | Tall and simple, in a terracotta hijab (#e07856) and a sage green dress (#7fb08f). | The hero: calm and present. She holds his hand and hugs him. |
| **Bidan** | A light blue hijab (#8fc4ea), a pink dress (#ef93a8) and a white name tag. Holds cotton. | The kind health worker. Never scary, and the needle is never shown. |
| **Kuman** (germs) | Small purple blobs (#5e4a96 / #8a74c6), cute rather than scary. | The thing the body learns to beat. |

- **Palette:** peach, terracotta, leaf green, sage, sky blue, pink, warm cream paper, ink outlines.
- **Where the art lives:** the character drawing code is in `experiments/popup-imunisasi/chars.js` (makeTunas, makeAdult('mama'|'bidan'), germ).
- **Possible later additions:** Papa (he laughs at himself in humour; never the butt of a joke against Mama), a sibling, and Nenek (corrected kindly, "bukan salah Nenek").

## 5. Rules carried over from TemanTumbuh

- Health content must follow IDAI, Kemenkes or WHO, with the source named in the description. No promises ("pasti", "dijamin").
- **No red cross symbol** on clinics; use a leaf-heart sign. The protected emblem falls under UU 1/2018.
- No needle close-ups, no scary doctors, no mom-shaming, no husband-bashing.
- Never promote formula, bottles, teats or pacifiers (PP 28/2024).
- No other creators' characters, songs or phrases.

## 6. Three animation styles tested

All three tell the same 40 s imunisasi story, so they can be compared directly.

| | Puppet | Crayon picture book | Paper pop-up book |
|---|---|---|---|
| File | `experiments/kartun/tunas-test.mp4` | `experiments/crayon-imunisasi/preview-720p.mp4` | `experiments/popup-imunisasi/preview-720p.mp4` |
| Look | Flat cut-outs, simple | Hand-drawn crayon; the world draws itself ahead of Tunas | 3D pop-up book on a desk, with real paper shadows and page turns |
| Feel | Plain | Warm, handmade | Most premium and distinctive |
| Render time | Seconds | Minutes | About 2.3 h in the cloud (no GPU); much faster on a Mac |
| Cost per new episode | Lowest | Low | Highest: new sets, props and poses each time |

**Decision pending:** Merwyn hasn't picked a style yet. The pop-up is the strongest look, and the crayon is the easiest to scale.

## 7. Tools and pipeline

- **Engine:** Lemo-Opuscar (github.com/lemomo-ai/lemo-opuscar).
  - Its code is MIT. Its STYLE.md files are CC BY-NC and are used as direction only, never copied.
  - It renders a web page frame by frame into video (`core/render/video.mjs`), then muxes the sound (`core/render/mux.sh`).
- **Sound:** synthesised in each project's `mix.py`: plucked strings, music box, glockenspiel, woodblock and paper foley. No samples are used, so there are no licence issues.
- **Each project folder holds:** `TREATMENT.md` (the story, shot list, beat sheet and sound plan), the scene JS, `mix.py`, `CREDITS` and `voices/`.
- **Repo:** everything is in the temantumbuh repo under `experiments/`. Full-size mp4s are gitignored; only the 720p previews are committed.
- **Render on Merwyn's Mac** for real episodes, using `LEMO_ANGLE=metal`. Cloud rendering at about 10 s per frame is too slow for a series.

## 8. Next steps

1. Merwyn picks a style: puppet, crayon or pop-up.
2. Merwyn sets up ElevenLabs and chooses an Indonesian child voice. Then re-voice the imunisasi pilot.
3. Fix subtitle readability, then lock the pilot.
4. Write a list of 10 episode topics and their sources (IDAI/Kemenkes for the health ones).
5. Set up the YouTube channel: name, made-for-kids setting, banner using Tunas.
6. Produce episode 1 at full length (2 to 4 min), plus 2 or 3 Shorts cut from it.

## 9. Working tip for the new project

Start fresh sessions per episode and keep this file as the brief. The old session got expensive (about $619 at API rates) mostly because every step re-read a very long history.
