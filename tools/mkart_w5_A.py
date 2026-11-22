# Scenes for week-5 group A: w5s-ww-isi (Mon 23), w5s-menu-mpasi-1 and w5s-rebutan-mainan (Tue 24).
# Every name starts with "w5a-" so it never collides with other batches.
# Family from tools/people.py. Flat palette, no real faces. No bottle, teat or pacifier anywhere (PP 28/2024).
# Toys: big and safe-looking (no small parts near the baby). Run: python tools/mkart_w5_A.py [contact.png]
import sys, os, io, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

NAMES = []
MINT = '#e3eee6'; LIVER = '#8a4a3c'; MEAT = '#b5573f'; YOLK = '#f3c45f'; CHICK = '#f0d2a8'; CHICKD = '#d9ad78'; GREEN = '#8fbf7a'


def save(name, h, body):
    svg(name, h, body); NAMES.append(name)


def rr(x, y, w, h, r, f, op=1, rot=0):
    t = f' transform="rotate({rot} {x+w/2} {y+h/2})"' if rot else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" opacity="{op}"{t}/>'
def circ(cx, cy, r, f, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" opacity="{op}"/>'
def path(d, col, w=8, fill='none', op=1):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def spark(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'
def block(x, y, s, f, fd, rot=0):
    return f'<g transform="rotate({rot} {x+s/2} {y+s/2})">' + rr(x, y, s, s, 10, f) + rr(x, y + s * .72, s, s * .28, 8, fd, op=.6) + circ(x + s / 2, y + s * .4, s * .16, '#fff', .45) + '</g>'
def limb(pts, col, w):
    d = f'M{pts[0][0]} {pts[0][1]}' + (f' Q{pts[1][0]} {pts[1][1]} {pts[2][0]} {pts[2][1]}' if len(pts) == 3 else ''.join(f' L{x} {y}' for x, y in pts[1:]))
    return path(d, col, w)
def hand(x, y, r): return circ(x, y, r, SKIN)
def carpet(x, y, w, h):
    return rr(x, y, w, h, 20, MINT) + ''.join(rr(x + 30, y + 14 + i * 22, w - 60, 6, 3, SAGE, op=.35) for i in range(max(1, int((h - 20) / 22))))
def chest(kind, cx, cy, s):
    r = head_r(kind, s); return cx, cy + 0.95 * r + 1.1 * r


def car(cx, cy, w, col=SKY, cold=SKYD):
    """Big chunky toy car, side view, centred at cx, wheels resting on cy + w*0.32."""
    h = w * 0.34
    return (rr(cx - w / 2, cy - h / 2, w, h, h * 0.35, col) + rr(cx - w * 0.22, cy - h * 1.05, w * 0.46, h * 0.7, h * 0.3, col) +
            rr(cx - w * 0.15, cy - h * 0.92, w * 0.14, h * 0.42, 6, CARD) + rr(cx + w * 0.03, cy - h * 0.92, w * 0.14, h * 0.42, 6, CARD) +
            rr(cx - w / 2, cy + h * 0.12, w, h * 0.38, h * 0.2, cold, op=.55) +
            ''.join(circ(cx + k * w * 0.3, cy + h * 0.5, w * 0.13, INK) + circ(cx + k * w * 0.3, cy + h * 0.5, w * 0.05, LINE) for k in (-1, 1)))
def ball(cx, cy, r):
    return circ(cx, cy, r, TERRA) + path(f'M{cx-r} {cy} Q{cx} {cy-r*0.5} {cx+r} {cy}', CARD, r * 0.18) + circ(cx - r * 0.35, cy - r * 0.4, r * 0.18, '#fff', .45)
def book(x, y, w, col=BLUSH):
    h = w * 0.62
    return (rr(x, y, w, h, 10, col) + rr(x + w / 2 - 4, y, 8, h, 3, TD, op=.5) +
            circ(x + w * 0.28, y + h * 0.42, h * 0.16, SUN) + rr(x + w * 0.6, y + h * 0.3, w * 0.28, h * 0.12, 4, CARD) + rr(x + w * 0.6, y + h * 0.52, w * 0.22, h * 0.12, 4, CARD))
def hourglass(cx, cy, s):
    w, h = 60 * s, 110 * s
    return (rr(cx - w * 0.7, cy - h / 2 - 12 * s, w * 1.4, 14 * s, 6, BOXD) + rr(cx - w * 0.7, cy + h / 2 - 2 * s, w * 1.4, 14 * s, 6, BOXD) +
            f'<path d="M{cx-w/2} {cy-h/2} L{cx+w/2} {cy-h/2} L{cx+w*0.08} {cy} L{cx+w/2} {cy+h/2} L{cx-w/2} {cy+h/2} L{cx-w*0.08} {cy} Z" fill="{CARD}" stroke="{LINE}" stroke-width="{4*s}"/>'
            f'<path d="M{cx-w*0.3} {cy-h*0.28} L{cx+w*0.3} {cy-h*0.28} L{cx} {cy-h*0.02} Z" fill="{SUN}"/>'
            f'<path d="M{cx-w*0.42} {cy+h*0.47} L{cx+w*0.42} {cy+h*0.47} Q{cx} {cy+h*0.2} {cx-w*0.42} {cy+h*0.47} Z" fill="{SUN}"/>')
def nope(cx, cy, r=34):
    k = r * .4
    return circ(cx, cy, r, TD) + path(f'M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}', '#fff', r * .26)


# ================================================================== w5s-ww-isi
H, T = 460, 380
m = seat('mama', 1.25, T, True)
b = (rr(560, 20, 170, 130, 18, BOX) + rr(572, 32, 146, 106, 10, SKY) + circ(612, 70, 22, SUN) + rr(642, 32, 10, 106, 0, BOX) +
     person('mama', 250, m, 1.25, 'senang', 'pegang') + table(T, H, col=MINT, edge=SAGE) +
     f'<ellipse cx="600" cy="{T+18}" rx="80" ry="12" fill="#000" opacity="0.07"/>' + tunas('hore', 160, 190, 520, T - 170) +
     block(700, T - 70, 70, SUN, SUND, -8) + block(730, T - 140, 60, SAGE, SD, 10) + ball(790, T - 6, 34) + book(330, T - 8, 120))
save('hero-w5a-ww-isi', H, b)

# ================================================================== w5s-menu-mpasi-1
H = 440
DAYS = (('SEN', YOLK), ('SEL', SKY), ('RAB', LIVER), ('KAM', MEAT), ('JUM', SKY), ('SAB', CHICK), ('MIN', YOLK))
b = rr(20, 20, 620, 300, 26, CARD) + rr(20, 20, 620, 70, 26, SAGE) + rr(20, 60, 620, 30, 0, SAGE) + text(330, 68, 'LAUK HEWANI TIAP HARI', 30, '#fff')
for i, (d, col) in enumerate(DAYS):
    x = 60 + i * 82
    b += text(x + 22, 140, d, 24, MUTED)
    if col == YOLK:   # egg: white with a yolk
        b += f'<ellipse cx="{x+22}" cy="210" rx="30" ry="24" fill="#fff" stroke="{LINE}" stroke-width="3"/>' + circ(x + 22, 210, 12, YOLK)
    elif col == SKY:  # fish
        b += f'<ellipse cx="{x+16}" cy="210" rx="26" ry="14" fill="{SKY}"/><path d="M{x+38} 210 L{x+54} 196 L{x+54} 224 Z" fill="{SKYD}"/>' + circ(x + 4, 206, 3.5, INK)
    elif col == CHICK:  # drumstick
        b += f'<ellipse cx="{x+28}" cy="204" rx="24" ry="20" fill="{CHICK}"/><rect x="{x-2}" y="214" width="26" height="9" rx="4" fill="{CARD}" transform="rotate(30 {x+10} 218)"/><circle cx="{x+2}" cy="226" r="7" fill="{CARD}"/>'
    else:             # liver / meat pieces
        b += circ(x + 10, 214, 14, col) + circ(x + 32, 204, 13, col) + circ(x + 28, 226, 11, col)
    b += rr(x - 4, 258, 52, 10, 5, LINE)
b += (f'<ellipse cx="760" cy="330" rx="90" ry="14" fill="#000" opacity="0.07"/>' + bowl(760, 230, 200, TERRA, TD) +
      bits([(715, 226, 15, YOLK), (750, 216, 14, GREEN), (790, 226, 15, MEAT), (765, 232, 12, SKY)]) +
      path('M720 160 q14 -20 0 -40 M760 160 q14 -20 0 -40 M800 160 q14 -20 0 -40', LINE, 8))
save('hero-w5a-menu', H, b)

# chicken: raw drumstick -> cooked, chopped into the bowl (same layout as the art-lauk-* strips)
H = 300
b = (f'<ellipse cx="140" cy="140" rx="90" ry="70" fill="{CHICK}"/><ellipse cx="160" cy="120" rx="40" ry="24" fill="#fff" opacity="0.35"/>'
     f'<rect x="20" y="170" width="90" height="28" rx="12" fill="{CARD}" transform="rotate(30 60 184)"/><circle cx="30" cy="214" r="22" fill="{CARD}"/><circle cx="56" cy="226" r="18" fill="{CARD}"/>'
     + path('M330 150 L440 150 M410 124 L442 150 L410 176', MUTED, 12) +
     path('M580 60 q14 -20 0 -40 M620 60 q14 -20 0 -40 M660 60 q14 -20 0 -40', LINE, 8) + bowl(620, 130, 230, SKY, SKYD) +
     bits([(570, 126, 14, CHICK), (600, 118, 13, CHICKD), (640, 126, 14, CHICK), (670, 118, 12, CHICKD), (620, 112, 12, CHICK)]))
save('big-w5a-ayam', H, b)

# ================================================================== w5s-rebutan-mainan
H, T = 520, 440
k = seat('kakak', 1.3, T); a = seat('adek', 1.34, T)
kx, ky = chest('kakak', 210, k, 1.3); ax, ay = chest('adek', 670, a, 1.34)
cy = ky - 40
pull = (limb([(kx + 50, ky - 30), (kx + 110, cy - 10), (330, cy)], TD, 42) + hand(330, cy, 24) +
        limb([(ax - 50, ay - 30), (ax - 110, cy - 10), (550, cy)], SUND, 42) + hand(550, cy, 24))
b = (person('kakak', 210, k, 1.3, 'ngomel', 'none') + person('adek', 670, a, 1.34, 'ngomel', 'none', flip=True) + car(440, cy, 260) + pull +
     path(f'M300 {cy-120} l-40 -20 M310 {cy-150} l-30 -30 M580 {cy-120} l40 -20 M570 {cy-150} l30 -30', TD, 8) +
     table(T, H, col=MINT, edge=SAGE) + bubble(20, 0, 260, ['"Punyaku!"'], 'br', size=40) + bubble(600, 0, 260, ['"Punyaku!"'], 'bl', size=40))
save('hero-w5a-rebutan', H, b)

# 1 stop: Mama holds the car up out of reach, calm; both kids look surprised
m = seat('mama', 1.2, T, True); mx, my = chest('mama', 440, m, 1.2)
b = (person('kakak', 150, seat('kakak', 1.05, T), 1.05, 'kaget', 'none') + person('adek', 730, seat('adek', 1.08, T), 1.08, 'kaget', 'none', flip=True) +
     person('mama', 440, m, 1.2, 'lembut', 'pegang') + car(440, my - 34, 190) + table(T, H, col=MINT, edge=SAGE))
save('big-w5a-stop', H, b)

# 2 name the feeling: Mama hugs Adek, who is sad; heart
m = seat('mama', 1.3, T, True); a = seat('adek', 1.3, T)
b = (person('mama', 290, m, 1.3, 'lembut', 'peluk') + person('adek', 560, a, 1.3, 'sedih', 'none') + heart(700, 120, 36) + spark(760, 70, 16) + table(T, H, col=MINT, edge=SAGE))
save('big-w5a-sebut', H, b)

# 3 turns: Kakak plays the car, Adek waits with a ball, hourglass in between
k = seat('kakak', 1.22, T); a = seat('adek', 1.26, T)
b = (person('kakak', 180, k, 1.22, 'senang', 'pegang') + person('adek', 700, a, 1.26, 'senang', 'pegang', flip=True) +
     table(T, H, col=MINT, edge=SAGE) + car(250, T - 30, 170) + ball(640, T - 40, 42) + hourglass(440, T - 120, 1.25))
save('big-w5a-timer', H, b)


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
