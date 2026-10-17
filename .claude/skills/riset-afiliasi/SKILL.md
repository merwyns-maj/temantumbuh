---
name: riset-afiliasi
description: Find, check and score affiliate products (TikTok Shop, Shopee) to attach to TemanTumbuh posts, so every product earns its place in the post and the commission is worth it. Use when a post is affiliate-eligible, when refilling data/products.csv, or when Merwyn asks what to sell.
---

# Riset afiliasi

A product goes into a post only when it is **the tool the tip already needs**. A soft book belongs in "Buku pertama bayi per usia", and a food cutter belongs in "Potong makanan anti-tersedak". If you have to change the post to fit the product, it is the wrong product.

Keep affiliate posts to about **20% of the calendar** (research, 17 Oct 2026). Trust comes first; 70% of Indonesian mums buy through links from people they trust.

## 1. Where the data comes from

| Source | What it gives | How to reach it |
| --- | --- | --- |
| TikTok Shop affiliate marketplace (Creator Center) | Commission %, price, sold count, rating, seller | Only inside the TikTok app once the account is an affiliate (about 1,000 followers). Use Merwyn's export or screenshots, or the built-in browser if he is signed in |
| Shopee Affiliate (affiliate.shopee.co.id) | Commission % per product or category, extra-commission campaigns, the per-order commission cap | Built-in browser with Merwyn signed in, or his export |
| Shopee and TikTok Shop product pages | Price, sold count, rating, review count, store type (Mall or Star), SNI or BPOM number | Public pages via WebFetch, when reachable |
| Kalodata, FastMoss and similar (paid, optional) | TikTok Shop trending products and sales history | Only if Merwyn subscribes |

Never invent sold counts or commission rates. If a number cannot be seen, leave the cell empty; the score treats it as the worst case.

## 2. Hard gates (fail any one and the product is out)

1. **No breast-milk substitutes**: formula, follow-on or growing-up milk, bottles and teats promoted for formula (PP 28/2024).
2. **No health claims we cannot back**: ASI boosters, supplements and vitamins stay out for now. When they come in later, they need a BPOM number and no efficacy claims.
3. **Toys need SNI** (mandatory for children's toys in Indonesia). Food, food contact items and cosmetics need BPOM or the right registration.
4. **Age-safe**: nothing with small parts for under-3s, and no products for a younger age than the maker states.
5. **Rating 4.6 or higher, with at least 100 reviews.**
6. **Not a dropship listing of a branded item at a suspicious price** (likely fake).

## 3. Score out of 100

`python tools/score_product.py data/products.csv` computes the parts in **bold**. You fill in `relevance` (1 to 5) and check the gates.

| Criterion | Max | How it is scored |
| --- | --- | --- |
| Relevance to the post | 25 | Judged 1 to 5. 5 = the post's tip literally needs it. 3 = it fits the series but not this post. 1 = forced |
| **Rupiah per sale** | 20 | price × commission %, after any per-order cap. Full points at Rp15,000 or more per sale, scaled down to 0 at Rp1,000 |
| **Demand** | 20 | Sold in the last 30 days. Full points at 3,000+, scaled on a log curve. Empty = 0 |
| **Likely to convert** | 15 | Price band (Rp30k to Rp200k is best for impulse buys), rating, review count, Mall or Star store |
| **Trust** | 20 | Official, Mall or Star store (8), SNI or BPOM registration present (8), the maker's age matches the post's age (4) |

The margin question: as an affiliate we don't earn the seller's margin, only the commission, so "Rupiah per sale" is our margin. A seller with a high margin can afford a high commission, which is why commission % is the number to chase. Real margin matters only for our own products (the Momo worksheets), which are scored separately.

**Thresholds:** 75 and up can go in a post. 60 to 74 is a backup. Under 60 is dropped.

## 4. Matching products to posts

1. Find the calendar days marked `"affiliate"`, plus any post where a tip names a buyable tool.
2. For each, shortlist 3 to 5 candidates that pass the gates, score them, and keep the top 1 to 2. Never more than 3 products in one post.
3. Record the choice in the post spec as `"products": ["<id>", ...]` and add `"affiliate": true`. The linter then requires a disclosure in the caption (#iklan or "link afiliasi").
4. The product shows up as a tool inside the tip, never as the hook. "Jangan checkout dulu" posts list what *not* to buy too; that honesty is what makes the rest trusted.

## 5. Weekly refresh

- Re-check price, commission and stock for every product in posts from the last 30 days. Commission campaigns end and links break.
- Add 10 to 20 new candidates per series from what is trending in Mom and Baby and Toys.
- After affiliate posts go live, add clicks, orders and commission earned to `data/products.csv`. Then compare the score with real earnings per 1,000 views, as with the content score.
