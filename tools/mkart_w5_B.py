# Scenes for week-5 group B: w5s-makan-busui and w5s-sains-dapur (Wed 25 Nov).
# Every name starts with "w5b-". Flat palette, no real faces, no bottle/teat/pacifier (PP 28/2024).
# Run: python tools/mkart_w5_B.py [contact.png]
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

NAMES = []
CHILI = '#d9503b'; CHILID = '#a8372a'; LEAF = '#6fbf5a'; ICE = '#d8eef8'; COFFEE = '#6b4632'; CABBAGE = '#b9dc9a'; CABD = '#8fbf7a'
WATER = '#bfe0f2'; WATERD = '#8fc4ea'; PURPLE = '#9b7ac9'; FIZZ = '#fff7d6'


def save(name, h, body): svg(name, h, body); NAMES.append(name)
def rr(x, y, w, h, r, f, op=1, rot=0):
    t = f' transform="rotate({rot} {x+w/2} {y+h/2})"' if rot else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" opacity="{op}"{t}/>'
def circ(cx, cy, r, f, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" opacity="{op}"/>'
def path(d, col, w=8, fill='none', op=1):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'
def spark(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'
def check(cx, cy, r=34):
    return circ(cx, cy, r, SAGE) + path(f'M{cx-r*.42} {cy} L{cx-r*.1} {cy+r*.32} L{cx+r*.45} {cy-r*.3}', '#fff', r * .24)
def shadow(cx, cy, rx): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.14}" fill="#000" opacity="0.07"/>'
def steam(x, y, n=3, gap=40): return path(' '.join(f'M{x+i*gap} {y} q14 -20 0 -40' for i in range(n)), LINE, 8)

def chili(cx, cy, s=1, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx-70*s} {cy-10*s} Q{cx} {cy-40*s} {cx+70*s} {cy+30*s} Q{cx+10*s} {cy+20*s} {cx-70*s} {cy+12*s} Z" fill="{CHILI}"/>'
            f'<path d="M{cx-40*s} {cy-14*s} Q{cx} {cy-28*s} {cx+40*s} {cy+4*s}" stroke="#fff" stroke-width="{6*s}" fill="none" opacity="0.35" stroke-linecap="round"/>'
            f'<path d="M{cx-70*s} {cy} q-20 -6 -26 -26" stroke="{LEAF}" stroke-width="{10*s}" fill="none" stroke-linecap="round"/></g>')
def glass(cx, by, w, h, fill=WATER, ice=True):
    b = (f'<path d="M{cx-w/2} {by-h} L{cx+w/2} {by-h} L{cx+w*0.4} {by} L{cx-w*0.4} {by} Z" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>'
         f'<path d="M{cx-w*0.46} {by-h*0.8} L{cx+w*0.46} {by-h*0.8} L{cx+w*0.4} {by-4} L{cx-w*0.4} {by-4} Z" fill="{fill}"/>')
    if ice: b += rr(cx - w * 0.3, by - h * 0.72, w * 0.26, w * 0.26, 8, ICE, rot=-12) + rr(cx + 0.02 * w, by - h * 0.6, w * 0.26, w * 0.26, 8, ICE, rot=14)
    return b
def mug(cx, by, w, col=TERRA):
    h = w * 0.9
    return (rr(cx - w / 2, by - h, w, h, 18, col) + path(f'M{cx+w/2} {by-h*0.75} q{w*0.35} 0 {w*0.35} {h*0.3} q0 {h*0.3} -{w*0.35} {h*0.3}', col, w * 0.1) +
            rr(cx - w * 0.4, by - h + 8, w * 0.8, 18, 9, COFFEE))
def cabbage(cx, cy, r):
    return circ(cx, cy, r, CABBAGE) + path(f'M{cx} {cy-r*0.9} Q{cx-r*0.3} {cy} {cx} {cy+r*0.9} M{cx-r*0.7} {cy-r*0.4} Q{cx-r*0.2} {cy} {cx-r*0.5} {cy+r*0.6} M{cx+r*0.7} {cy-r*0.4} Q{cx+r*0.2} {cy} {cx+r*0.5} {cy+r*0.6}', CABD, 7)
def peanut(cx, cy, s=1, rot=0):
    return f'<g transform="rotate({rot} {cx} {cy})">' + circ(cx - 14 * s, cy, 16 * s, '#d9ad78') + circ(cx + 14 * s, cy, 14 * s, '#d9ad78') + '</g>'
def basin(cx, by, w):
    h = w * 0.34
    return (f'<path d="M{cx-w/2} {by-h} L{cx+w/2} {by-h} L{cx+w*0.42} {by} L{cx-w*0.42} {by} Z" fill="{SKYD}"/>' +
            f'<ellipse cx="{cx}" cy="{by-h}" rx="{w/2}" ry="{h*0.22}" fill="{WATER}"/>' + rr(cx - w / 2 - 6, by - h - 10, w + 12, 14, 7, SKY))
def tray(cx, by, w): return rr(cx - w / 2, by - 22, w, 22, 10, BOX) + rr(cx - w / 2 + 10, by - 22, w - 20, 8, 4, BOXD, op=.5)
def bottle_plain(cx, by, s=1, col=SAGE):
    # a plain plastic soda-style bottle used as a "volcano" (not a baby bottle: no teat, wide cap)
    return (rr(cx - 34 * s, by - 150 * s, 68 * s, 150 * s, 20 * s, col, op=.85) + rr(cx - 20 * s, by - 186 * s, 40 * s, 40 * s, 10 * s, col) +
            rr(cx - 24 * s, by - 196 * s, 48 * s, 16 * s, 6 * s, BOXD))


# ============================================================ hero: makan busui
H, T = 460, 390
m = seat('mama', 1.3, T, True)
b = (person('mama', 260, m, 1.3, 'senang', 'pegang') + table(T, H, col=CARD, edge=LINE) +
     bowl(470, T - 70, 170, TERRA, TD) + bits([(436, T - 76, 14, '#f0e2b6'), (470, T - 84, 14, '#f0e2b6'), (504, T - 76, 13, LEAF)]) + steam(440, T - 120, 3, 30) +
     chili(640, T - 40, 0.75, -10) + glass(790, T - 6, 90, 150) + spark(720, 80, 18) + spark(560, 60, 12, TERRA))
save('hero-w5b-busui', H, b)

H = 300
save('big-w5b-cabai', H, chili(330, 120, 1.5, -20) + chili(400, 220, 1.3, 15) + check(560, 70))
save('big-w5b-es', H, glass(260, 280, 150, 230) + glass(440, 280, 130, 200, fill='#f6d6a8') + check(570, 80))
save('big-w5b-kol', H, cabbage(220, 160, 110) + peanut(440, 210, 1.6, -20) + peanut(520, 160, 1.4, 25) + peanut(470, 110, 1.3, 5) + check(600, 60))
save('big-w5b-kopi', H, mug(240, 270, 150) + mug(450, 270, 150, SAGE) + steam(215, 120, 2, 40) + steam(425, 120, 2, 40))
save('big-w5b-alkohol', H, f'<path d="M300 60 L420 60 L380 170 L340 170 Z" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>' + rr(355, 170, 10, 80, 5, LINE) + rr(310, 245, 100, 14, 7, LINE) +
     circ(600, 160, 90, TD) + path('M540 100 L660 220 M660 100 L540 220', '#fff', 22))

# ============================================================ hero: sains dapur
H, T = 460, 390
b = (table(T, H, col=MINT if False else '#e3eee6', edge=SAGE) + tunas('riset', 170, 200, 120, T - 190) +
     bottle_plain(470, T, 1.15) + path(f'M470 {T-226} q-40 -40 -80 -30 M470 {T-226} q40 -50 90 -36 M470 {T-226} q0 -60 10 -90', '#fff', 16) +
     circ(395, T - 270, 22, FIZZ) + circ(555, T - 268, 26, FIZZ) + circ(480, T - 320, 20, FIZZ) +
     basin(700, T, 220) + circ(660, T - 84, 16, TERRA) + rr(720, T - 92, 40, 18, 8, SUN) + spark(820, 90, 20) + spark(600, 60, 14, TERRA))
save('hero-w5b-sains', H, b)

H = 300
b = (basin(330, 280, 380) + circ(260, 196, 22, TERRA) + rr(330, 186, 60, 22, 10, SUN) + f'<ellipse cx="420" cy="200" rx="34" ry="12" fill="{BOX}"/>' +
     path('M260 230 L260 262 M250 252 L260 264 L270 252', SKYD, 6))
save('big-w5b-terapung', H, b)
b = tray(440, 290, 420) + ''.join(rr(270 + i * 120, 150 + (i % 2) * 20, 100, 110, 20, c, op=.85) + circ(300 + i * 120, 180 + (i % 2) * 20, 14, '#fff', .6) for i, c in enumerate([SKY, TERRA, PURPLE])) + ''.join(f'<ellipse cx="{320+i*120}" cy="270" rx="52" ry="10" fill="{c}" opacity="0.5"/>' for i, c in enumerate([SKY, TERRA, PURPLE]))
save('big-w5b-es-warna', H, b)
b = glass(300, 280, 110, 200, fill=SKY, ice=False) + glass(430, 280, 110, 200, fill=SUN, ice=False) + path('M500 180 L530 180 M518 168 L532 180 L518 192', MUTED, 7) + glass(590, 280, 110, 200, fill=SAGE, ice=False)
save('big-w5b-warna', H, b)
b = (tray(440, 290, 520) + bottle_plain(440, 268, 1.0, TERRA) + path('M440 74 q-40 -30 -80 -10 M440 74 q40 -36 80 -14', FIZZ, 18) +
     circ(370, 60, 18, FIZZ) + circ(520, 56, 20, FIZZ) + f'<ellipse cx="440" cy="250" rx="140" ry="18" fill="{FIZZ}"/>')
save('big-w5b-gunung', H, b)
b = (glass(290, 280, 100, 190, fill=CHILI, ice=False) + glass(440, 280, 100, 190, fill=CARD, ice=False) + glass(590, 280, 100, 190, fill=SKY, ice=False) +
     path('M290 120 Q365 30 440 140', '#f0e8dc', 24) + path('M440 140 Q515 30 590 120', '#f0e8dc', 24) +
     path('M290 120 Q325 70 360 64', CHILI, 10, op=.6) + path('M590 120 Q555 70 520 64', SKY, 10, op=.6) + f'<ellipse cx="440" cy="258" rx="40" ry="10" fill="{PURPLE}" opacity="0.6"/>')
save('big-w5b-tisu', H, b)

autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k_, im in enumerate(ims): sheet.paste(im, ((k_ % cols) * 440, (k_ // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
