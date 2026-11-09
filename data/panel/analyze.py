"""Compare persona-panel ratings and our skor-konten total against real views (Spearman rank correlation).
Usage: python data/panel/analyze.py PANEL_OUT_DIR [actuals.json]"""
import csv, glob, json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out_dir = sys.argv[1]
act = json.load(open(sys.argv[2] if len(sys.argv) > 2 else f'{ROOT}/data/panel/actuals_2026-11-09.json'))
key = json.load(open(f'{ROOT}/data/panel/key.json'))
score = {r['slug']: float(r['total']) for r in csv.DictReader(open(f'{ROOT}/data/predictions.csv')) if r['total']}
score['d25-ternyata-normal-v2'] = score.get('d25-ternyata-normal-v2', score.get('d25-ternyata-normal'))

def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def spearman(a, b):
    ra, rb = rank(a), rank(b); n = len(a); ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb)); den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float('nan')

panel = {}
for f in sorted(glob.glob(f'{out_dir}/*.json')):
    name = os.path.basename(f)[:-5]
    panel[name] = {r['code']: r for r in json.load(open(f))}
names = list(panel)
by_slug = {v['slug']: c for c, v in key.items()}
def feat(slug, field, who=None):
    c = by_slug[slug]; rows = [panel[n][c] for n in (who or names) if c in panel[n]]
    return sum(r[field] for r in rows) / len(rows)
def composite(slug, who=None):
    return feat(slug, 'stop', who) * (1 + (feat(slug, 'save', who) + feat(slug, 'send', who)) / 20)

def report(slugs, label):
    v = [act[s]['views'] for s in slugs]
    rows = [('our score (skor-konten total)', [score[s] for s in slugs])]
    for fld in ('stop', 'swipe', 'save', 'send', 'comment'):
        rows.append((f'panel mean {fld}', [feat(s, fld) for s in slugs]))
    rows.append(('panel composite (stop x save/send)', [composite(s) for s in slugs]))
    for n in names:
        rows.append((f'  persona {n}: stop', [feat(s, 'stop', [n]) for s in slugs]))
    print(f'\n{label} (n={len(slugs)}), Spearman vs views')
    for name, xs in rows: print(f'  {name:38s} {spearman(xs, v):+.2f}')
    return rows, v

bt = [s for s, k in ((key[c]['slug'], key[c]) for c in key) if k['set'] == 'backtest' and s in act]
print('personas:', ', '.join(names))
report(bt, 'BACKTEST all')
report([s for s in bt if s != 'd01-udah-stimulasi'], 'BACKTEST without d01 (account launch boost)')
report([s for s in bt if s.startswith('w2')], 'BACKTEST week 2 only (same design, same cadence)')
print('\nTop 8 by panel composite vs views:')
for s in sorted(bt, key=lambda s: -composite(s))[:8]: print(f'  {s:28s} comp {composite(s):5.2f}  score {score[s]:3.0f}  views {act[s]["views"]}')
fw = [key[c]['slug'] for c in key if key[c]['set'] == 'forward']
print('\nFORWARD set, panel prediction (rank by composite):')
for i, s in enumerate(sorted(fw, key=lambda s: -composite(s)), 1): print(f'  {i:2d}. {s:28s} comp {composite(s):5.2f}  stop {feat(s,"stop"):.1f}  score {score.get(s, 0):3.0f}')
