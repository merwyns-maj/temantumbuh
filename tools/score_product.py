#!/usr/bin/env python3
"""Score affiliate product candidates out of 100. Rubric: .claude/skills/riset-afiliasi/SKILL.md

Usage: python tools/score_product.py data/products.csv [--post d23-alat-mpasi]
Columns used (empty cells score as worst case):
  id, platform, name, url, price, commission_pct, commission_cap, sold_30d, rating, reviews,
  store_type (mall|star|official|regular), registration (SNI/BPOM number or empty),
  age_min_months, post_age_min_months, gate_fail (any text = excluded), relevance (1-5), post
"""
import csv
import math
import sys


def num(v, default=None):
    try:
        return float(str(v).replace(".", "").replace(",", ".")) if "," in str(v) else float(v)
    except (TypeError, ValueError):
        return default


def score(r):
    if (r.get("gate_fail") or "").strip():
        return None, f"excluded: {r['gate_fail']}"
    price = num(r.get("price"), 0)
    pct = num(r.get("commission_pct"), 0)
    cap = num(r.get("commission_cap"))
    per_sale = price * pct / 100
    if cap:
        per_sale = min(per_sale, cap)
    # Rupiah per sale: 0 at Rp1k, full at Rp15k (log scale)
    rps = 0 if per_sale <= 1000 else min(1, math.log(per_sale / 1000) / math.log(15)) * 20
    sold = num(r.get("sold_30d"), 0)
    demand = 0 if sold <= 0 else min(1, math.log10(sold) / math.log10(3000)) * 20
    rating = num(r.get("rating"), 0)
    reviews = num(r.get("reviews"), 0)
    band = 6 if 30000 <= price <= 200000 else 3 if 15000 <= price <= 400000 else 0
    rate_pts = 5 if rating >= 4.9 else 4 if rating >= 4.8 else 2 if rating >= 4.6 else 0
    rev_pts = 2 if reviews >= 1000 else 1 if reviews >= 100 else 0
    store = (r.get("store_type") or "").lower()
    conv = band + rate_pts + rev_pts + (2 if store in ("mall", "official", "star") else 0)
    trust = (8 if store in ("mall", "official", "star") else 0) + (8 if (r.get("registration") or "").strip() else 0)
    a_min, p_min = num(r.get("age_min_months")), num(r.get("post_age_min_months"))
    trust += 4 if a_min is not None and p_min is not None and a_min <= p_min else 0
    rel = num(r.get("relevance"))
    relevance = 0 if rel is None else rel / 5 * 25
    total = relevance + rps + demand + conv + trust
    note = f"Rp{per_sale:,.0f}/sale".replace(",", ".")
    if rel is None:
        note += ", relevance not judged"
    if rating and rating < 4.6 or reviews and reviews < 100:
        return None, "excluded: rating under 4.6 or under 100 reviews"
    return total, note


def main(args):
    path = args[0]
    post = args[args.index("--post") + 1] if "--post" in args else None
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    out = []
    for r in rows:
        if post and r.get("post") != post:
            continue
        s, note = score(r)
        out.append((s if s is not None else -1, r, note))
    out.sort(key=lambda x: -x[0])
    for s, r, note in out:
        verdict = "EXCLUDED" if s < 0 else "USE" if s >= 75 else "BACKUP" if s >= 60 else "DROP"
        shown = "  -" if s < 0 else f"{s:3.0f}"
        print(f"{shown}  {verdict:8} {r.get('post', ''):22} {r.get('name', '')[:44]:44} {note}")


if __name__ == "__main__":
    main(sys.argv[1:])
