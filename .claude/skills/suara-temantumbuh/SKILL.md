---
name: suara-temantumbuh
description: Write, rewrite and check every piece of TemanTumbuh copy (carousel slides, hooks, captions, CTAs) so it sounds like a real Indonesian parent talking, not AI and not a textbook. Use before any copy is rendered or sent for review.
---

# Suara TemanTumbuh

The test for every line: **would a parent say this out loud in a WhatsApp voice note to another parent?** If not, rewrite it. Readers forgive a plain sentence. They scroll past a polished one that smells like AI.

## 1. Who is talking

A friend who is also a parent and happens to have read the research. Register: *santai tapi sopan*, the way people write in a school parents' group. Not *anak Jaksel* slang, not EYD textbook, not a brand press release.

- Address the reader as **kamu**. Never *Anda*.
- For parents as a group: **Ayah Bunda** or **orang tua**. Never *Bunda* alone: the brand is neutral and dads read it too.
- *Si kecil* at most once per post. It is the most overused phrase in Indonesian parenting content.

## 2. Use the spoken forms

| Instead of | Write |
| --- | --- |
| tidak | nggak |
| sudah | udah |
| saja | aja |
| sangat / sekali | banget (after the word) |
| bagaimana | gimana |
| membuat | bikin |
| memberi / memberikan | kasih |
| mengerti / memahami | ngerti / paham |
| seperti | kayak |
| hanya | cuma |
| sedang | lagi |
| menanggapi | nanggepin |
| melihat | lihat |
| untuk (people, purpose) | buat |

Particles (*kok, sih, deh, lho, kan, ya, dong*) add warmth. **At most one per slide**, or it reads forced.

Health facts may sit one notch more standard (*nyarankan* is fine, *merekomendasikan* is stiff), but never textbook.

## 3. Banned: the AI tells

The linter (`tools/lint_copy.py`) fails a post that contains any of these.

**Punctuation**
- Em dash `—` and en dash `–`, anywhere in copy. Use a full stop, a comma or a colon. A hyphen only inside words (*bolak-balik*, *hitam-putih*).
- Semicolons.
- More than one `!` per post. More than one `...` per post (keep it for comic timing).

**Openers**
*Di era digital ini · Dalam dunia parenting · Tahukah kamu · Pernahkah kamu · Mari kita · Yuk simak · Simak penjelasan berikut · Berikut adalah · Siapa yang di sini*

**Structures**
*Tidak hanya X, tetapi juga Y · Bukan sekadar X, melainkan Y · X adalah kunci · X adalah fondasi · Penting untuk · Pastikan untuk · Hal ini · Dengan demikian · Oleh karena itu · Selain itu · Perlu diingat · Pada dasarnya · Yang mana · di mana* (as a relative pronoun)

**Words**
*esensial · krusial · optimal · holistik · signifikan · maksimal · memaksimalkan potensi · tumbuh kembang optimal · momen berharga · perjalanan parenting · luar biasa · ajaib · rahasia · game changer · worth it · literally*

**Translation-ese**
*Ini adalah · melakukan* + noun (*melakukan pengecekan* → *cek*) · passive *dapat dilakukan* · *memiliki* (→ *punya*)

**Shapes that give AI away**
- Every list has exactly three items. Use two, four, five. Vary.
- Every sentence the same length. Mix a long one with a three-word one.
- Rhetorical set-ups: *Bayangkan...*, a question answered by the next sentence, *Jawabannya:*.
- Every slide built the same way. Keep the template, vary the rhythm inside it.

## 4. Write like a person

- **One specific detail beats a general claim.** *Jam 2 pagi.* *Sendok dan wadah plastik.* *Lima menit sebelum tidur.* Not *aktivitas sederhana sehari-hari*.
- **Fragments are fine.** *Iya, masih yang tadi.*
- **Start with the situation, then the point.** *Pas dia ngoceh, jeda sebentar.* Not *Penting untuk memberikan jeda.*
- **Admit real life.** *Nggak harus sempurna kok. Berantakan dikit nggak apa-apa.*
- **Code-mix only where parents really do:** newborn, MPASI, screen time, soft book, tantrum, toddler, sleep schedule. Never English just to sound cool.
- **Digits on slides** (*5 menit*, *2 tahun*).

## 5. Claims

Say where it comes from, casually: *riset nemuin*, *kata IDAI*, *WHO nyaranin*. Never *dijamin, pasti, 100%, bikin pintar, bikin gemuk, langsung*. MPASI and health lines follow IDAI and WHO. When unsure, soften: *bisa bantu*, *cenderung*.

## 6. Casing on slides

Hooks UPPERCASE. Titles sentence case, never Title Case. Series tags uppercase. No emoji on slides; at most two in a caption.

## 7. Before and after

| AI-sounding | TemanTumbuh |
| --- | --- |
| Tidak perlu sempurna. Cukup hadir, kontak mata, dan peluk — konsistensi kecil yang membentuk rasa aman. | Nggak harus sempurna kok. Hadir, kontak mata, peluk. Yang penting konsisten. |
| Riset perkembangan anak menemukan bahwa yang paling membentuk otak adalah percakapan dua arah. | Riset nemuin, yang ngaruh banget ke otak bayi itu obrolan dua arah. Dia ngoceh, kamu jawab. |
| Penting untuk memastikan anak mendapatkan waktu tidur yang cukup. | Pas tidur, otak anak nyimpen semua yang dia pelajari hari itu. |
| Yuk simak 5 tips berikut untuk memaksimalkan tumbuh kembang si kecil! | 5 kebiasaan receh yang ngaruh banget ke otak anak. |
| Sediakan berbagai benda yang aman untuk dieksplorasi oleh anak. | Kasih benda aman buat diulik: sendok, wadah plastik, kain. |

## 8. The workflow

1. Draft the post as a JSON spec (the renderer's input).
2. Run `python tools/lint_copy.py <spec>.json`. Zero errors before anything else.
3. Read every slide aloud. Rewrite anything you would not say.
4. Check the share test: who will they send this to?
5. Only then render.
