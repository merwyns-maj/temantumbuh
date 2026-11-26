# Scenes for week-5 group C: w5s-hp-tanpa-teriak and w5s-tontonan-tier (Fri 27 Nov).
# Every name starts with "w5c-". Flat palette, no real faces, no show characters or logos (screens show plain shapes only).
# Run: python tools/mkart_w5_C.py [contact.png]
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

NAMES = []
MINT = '#e3eee6'; SCREEN = '#2f3b45'; GLOW = '#9fd3f0'; ZAP = '#f3c45f'; PURPLE = '#9b7ac9'; SOFA = '#c98b6b'; SOFAD = '#a86f53'


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
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def note(cx, cy, s=1, col=TERRA):
    return circ(cx, cy, 12 * s, col) + rr(cx + 8 * s, cy - 50 * s, 6 * s, 50 * s, 3, col) + rr(cx + 8 * s, cy - 50 * s, 26 * s, 10 * s, 4, col)

def tablet(cx, cy, w, inner=None, rot=0):
    h = w * 0.7
    g = rr(cx - w / 2, cy - h / 2, w, h, 18, INK) + rr(cx - w / 2 + 12, cy - h / 2 + 12, w - 24, h - 24, 10, GLOW)
    if inner: g += inner
    return f'<g transform="rotate({rot} {cx} {cy})">{g}</g>'
def tv(cx, by, w, inner=''):
    h = w * 0.62
    return (rr(cx - w / 2, by - h - 30, w, h, 20, INK) + rr(cx - w / 2 + 16, by - h - 14, w - 32, h - 32, 12, SCREEN) + inner +
            rr(cx - 14, by - 30, 28, 22, 4, LINE) + rr(cx - w * 0.22, by - 10, w * 0.44, 12, 6, LINE))
def clock(cx, cy, r, hand=40):
    return circ(cx, cy, r, CARD) + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="6"/>' + path(f'M{cx} {cy} L{cx} {cy-r*0.7} M{cx} {cy} L{cx+r*0.5} {cy+r*0.1}', INK, 6)
def chest(kind, cx, cy, s):
    r = head_r(kind, s); return cx, cy + 0.95 * r + 1.1 * r


# ===================================================== w5s-hp-tanpa-teriak
H, T = 480, 420
m = seat('mama', 1.25, T, True); k = seat('kakak', 1.25, T)
b = (person('mama', 230, m, 1.25, 'lembut', 'pegang') + person('kakak', 620, k, 1.25, 'kaget', 'pegang', flip=True) +
     table(T, H, col=MINT, edge=SAGE) + tablet(470, T - 60, 170, rr(420, T - 92, 100, 16, 8, CARD) + circ(470, T - 52, 16, TERRA)) +
     clock(780, 90, 46) + spark(60, 60, 16))
save('hero-w5c-hp', H, b)

H, T = 440, 400
m = seat('mama', 1.15, T, True); k = seat('kakak', 1.15, T)
b = (person('mama', 220, m, 1.15, 'senang', 'pegang') + person('kakak', 640, k, 1.15, 'senang', 'none', flip=True) + table(T, H, col=MINT, edge=SAGE) +
     bubble(330, 0, 320, ['"1 episode,', 'habis itu udahan"'], 'bl', size=34))
save('big-w5c-janji', H, b)

H = 320
b = tablet(360, 170, 360, rr(240, 120, 240, 22, 11, CARD) + rr(240, 160, 180, 22, 11, CARD, op=.7) + check(360, 220, 30)) + clock(680, 150, 70)
save('big-w5c-selesai', H, b)

H, T = 440, 400
k = seat('kakak', 1.25, T)
kx, ky = chest('kakak', 300, k, 1.25)
can = (f'<path d="M520 {T-150} L640 {T-150} L630 {T-40} L530 {T-40} Z" fill="{SKY}"/>' + path(f'M640 {T-130} L720 {T-180}', SKYD, 16) +
       path(f'M520 {T-150} q-30 30 0 70', SKYD, 12) + ''.join(path(f'M{728+i*14} {T-170+i*6} l10 26', SKY, 6) for i in range(3)) +
       f'<path d="M760 {T} q-10 -70 20 -110 q10 50 -10 110 Z" fill="{SAGE}"/><path d="M790 {T} q20 -60 50 -80 q-10 50 -30 80 Z" fill="{SAGE}"/>' + rr(740, T - 20, 110, 40, 10, BOX))
b = person('kakak', 300, k, 1.25, 'hore', 'pegang') + can + table(T, H, col=MINT, edge=SAGE)
save('big-w5c-ganti', H, b)

H, T = 440, 400
k = seat('kakak', 1.3, T)
b = (person('kakak', 300, k, 1.3, 'ngomel', 'pegang') + tablet(300, T - 40, 150) + table(T, H, col=MINT, edge=SAGE) +
     bubble(480, 30, 300, ['"2 menit lagi', 'ya, Nak"'], 'bl', size=34) + clock(740, 250, 50) +
     path('M180 120 l-40 -20 M190 90 l-30 -30 M420 120 l40 -20', TD, 8))
save('big-w5c-dua-menit', H, b)

# ===================================================== w5s-tontonan-tier
H = 460
inner = (''.join(rr(210 + i * 120, 140 + (i % 2) * 40, 90, 90, 14, c) for i, c in enumerate([TERRA, ZAP, PURPLE, SKY])) +
         path('M200 260 L280 200 L340 280 L420 190 L480 270 L560 200 L640 260', ZAP, 10))
b = tv(440, 440, 520, inner)
for i, (t, c) in enumerate([('S', SAGE), ('A', SKY), ('B', SUN), ('C', TERRA)]):
    b += rr(20, 60 + i * 90, 70, 70, 14, c) + text(55, 108 + i * 90, t, 44, '#fff')
save('hero-w5c-tontonan', H, b)

H = 340
inner_fast = (''.join(rr(230 + i * 70, 100 + (i % 3) * 30, 60, 60, 10, c, rot=i * 20) for i, c in enumerate([TERRA, ZAP, PURPLE, SKY, TERRA, ZAP])) +
              path('M240 220 L300 160 L340 230 L400 150 L450 220 L520 160 L600 230', ZAP, 9))
save('big-w5c-cepat', H, tv(420, 330, 460, inner_fast) + path('M700 80 L740 40 L730 90 L780 60', ZAP, 10) + path('M120 90 L80 50 L90 100 L40 70', ZAP, 10))
inner_slow = (circ(320, 150, 40, SUN) + f'<path d="M210 260 Q330 170 450 230 Q540 180 630 260 Z" fill="{SAGE}"/>' + rr(500, 190, 30, 50, 6, BOX) + f'<path d="M490 195 L515 165 L540 195 Z" fill="{TERRA}"/>')
save('big-w5c-pelan', H, tv(420, 330, 460, inner_slow) + spark(740, 90, 18) + spark(110, 80, 12, TERRA))

H, T = 460, 420
m = seat('mama', 1.15, T, True); k = seat('kakak', 1.05, T)
b = (rr(80, T - 140, 520, 140, 40, SOFA) + rr(60, T - 210, 560, 90, 40, SOFAD) +
     person('mama', 220, m, 1.15, 'senang', 'peluk') + person('kakak', 440, k, 1.05, 'senang', 'none') + rr(60, T - 20, 560, 30, 10, SOFAD) +
     tv(760, T, 220, f'<path d="M680 {T-120} Q760 {T-160} 840 {T-120} L840 {T-60} L680 {T-60} Z" fill="{SAGE}"/>') + bubble(250, 0, 270, ['"Dia lagi', 'ngapain?"'], 'bl', size=32))
save('big-w5c-bareng', H, b)

H, T = 440, 400
k = seat('kakak', 1.25, T)
b = person('kakak', 330, k, 1.25, 'hore', 'hore') + note(560, 160, 1.2) + note(640, 100, 1, SKY) + note(150, 130, 1, SAGE) + table(T, H, col=MINT, edge=SAGE) + spark(700, 220, 18)
save('big-w5c-lagu', H, b)

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
