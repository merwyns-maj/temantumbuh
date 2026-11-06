# Scenes for w3e-s01-jangan-nangis (first story-format post). Run: python tools/mkart_story1.py [contact-sheet.png]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

def heart(x, y, s, col=TERRA):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 8 C-14 -8 -30 6 0 30 C30 6 14 -8 0 8 Z" fill="{col}"/>'
def phone(x, y, rot=0):
    return (f'<g transform="rotate({rot} {x+28} {y+50})"><rect x="{x}" y="{y}" width="56" height="100" rx="12" fill="{INK}"/><rect x="{x+6}" y="{y+10}" width="44" height="74" rx="6" fill="{SKY}"/>'
            f'<rect x="{x+12}" y="{y+20}" width="32" height="8" rx="4" fill="{CARD}"/><rect x="{x+12}" y="{y+34}" width="24" height="8" rx="4" fill="{CARD}"/></g>'
            f'<circle cx="{x+60}" cy="{y-4}" r="15" fill="{TERRA}"/>' + text(x+60, y+3, '9', 20, CARD))
def held_biscuits(kind, cx, cy, s, bs=0.8):
    r = head_r(kind, s); hy = cy + 0.95 * r + 1.13 * r
    return biscuit(cx - r * 0.42, hy - 18, bs, -18, 'l') + biscuit(cx + r * 0.42, hy - 14, bs, 14, 'r')
def crumbs(pts): return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BOXD}"/>' for x, y, r in pts)
H, T = 520, 440

# HERO: Adek crying with a broken biscuit, Ayah says the line
a = seat('adek', 1.5, T, True); y = seat('ayah', 1.38, T)
b = (person('ayah', 650, y, 1.38, 'capek', 'tangan-dada') + person('adek', 235, a, 1.5, 'nangis', 'pegang') +
     held_biscuits('adek', 235, a, 1.5) + table(T, H) + crumbs([(230, T + 30, 4), (262, T + 40, 3), (290, T + 26, 3)]) +
     bubble(400, 0, 440, ['Udah, jangan nangis.', 'Cuma biskuit.'], 'br', size=36))
svg('hero-s01-jangan-nangis', H, b)

# 1: relief. Ayah tired, phone buzzing
y = seat('ayah', 1.56, T); a = seat('adek', 0.94, T)
b = (person('adek', 120, a, 0.94, 'nangis', 'none') + person('ayah', 430, y, 1.56, 'capek', 'none') + table(T, H) +
     phone(650, T - 120, 12) + f'<path d="M708 {T-140} l14 -14 M722 {T-122} l18 -6 M636 {T-132} l-12 -14" stroke="{TERRA}" stroke-width="6" stroke-linecap="round"/>' +
     bubble(560, 10, 260, ['Capek...'], 'bl', size=38, think=True))
svg('big-s01-capek', H, b)

# 2: what the child hears
a = seat('adek', 1.88, T, True)
b = (person('adek', 400, a, 1.88, 'sedih', 'pegang') + held_biscuits('adek', 400, a, 1.88, 1.0) + table(T, H) +
     bubble(500, 0, 370, ['"Perasaanku', 'salah."'], 'bl', size=46, think=True))
svg('big-s01-perasaanku-salah', H, b)

# 3: name the feeling, at eye level
m = seat('mama', 1.44, T); a = seat('adek', 1.38, T, True)
b = (person('mama', 270, m, 1.44, 'lembut', 'none') + person('adek', 610, a, 1.38, 'sedih', 'pegang') + held_biscuits('adek', 610, a, 1.38, 0.7) +
     table(T, H) + bubble(20, 0, 540, ['"Kamu sedih ya,', 'biskuitnya patah."'], 'br', size=38))
svg('big-s01-sebut-perasaan', H, b)

# 4: stay close (hug)
m = seat('mama', 1.44, T); a = seat('adek', 1.38, T)
b = (person('adek', 520, a, 1.38, 'lembut', 'none') + person('mama', 320, m, 1.44, 'lembut', 'peluk') + table(T, H) +
     heart(650, 150, 1.4) + heart(715, 215, 0.9, SUN) + heart(190, 150, 1.0, BLUSH) +
     bubble(520, 0, 340, ['"Mama di sini."'], 'bl', size=38))
svg('big-s01-temenin', H, b)

# 5: once calm, find a way together (Ayah redeems himself)
y = seat('ayah', 1.44, T, True); a = seat('adek', 1.38, T)
b = (person('ayah', 280, y, 1.44, 'senang', 'pegang') + held_biscuits('ayah', 280, y, 1.44, 0.75) + person('adek', 630, a, 1.38, 'senang', 'none') + table(T, H) +
     f'<path d="M712 {T-190} l10 -24 l10 24 l24 10 l-24 10 l-10 24 l-10 -24 l-24 -10 Z" fill="{SUN}"/>' +
     bubble(10, 0, 590, ['"Satu buat kamu,', 'satu buat Ayah?"'], 'br', size=38))
svg('big-s01-cari-jalan', H, b)

names = ['hero-s01-jangan-nangis', 'big-s01-capek', 'big-s01-perasaanku-salah', 'big-s01-sebut-perasaan', 'big-s01-temenin', 'big-s01-cari-jalan']
autocrop(names)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in names]
    h = max(i.size[1] for i in ims); sheet = Image.new('RGB', (440 * 3, h * 2), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % 3) * 440, (k // 3) * h), im)
    sheet.save(sys.argv[1])
print('ok')
