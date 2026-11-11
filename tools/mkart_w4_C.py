# Design v2 scenes for week 4, group C (series ibu, long format):
#   w4l-asi-naik (Tue 17 Nov 12:00) and w4l-mastitis (Thu 19 Nov 12:00).
# Run: python tools/mkart_w4_C.py [contact.png]
# Every name starts with "w4c-" so it never collides with other batches.
# Rules: Mama from people.py (hijab), baby always wrapped in a blanket, breastfeeding shown as a close hold only,
# no anatomy, no bottles, teats or pumps with bottles (PP 28/2024). Milk only as ASI bags.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *
import people as P

ICE = '#cfe6f5'; ICED = '#a9cde8'; LEAF = '#6f9e5b'; LEAFD = '#557f45'; RICE = '#fbf7ee'; WATER = '#d6eaf7'
MILK = '#f7ecd6'; FRD = '#c3d3e2'; GREY = '#c8c2b8'; PALE = '#fde7df'
NAMES = []


def save(name, h, body):
    svg(name, h, body); NAMES.append(name)


# ------------------------------------------------------------------ small kit
def rr(x, y, w, h, r, f, st=None, sw=0, op=1):
    s = f' stroke="{st}" stroke-width="{sw}"' if st else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"{s} opacity="{op}"/>'
def circ(cx, cy, r, f, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" opacity="{op}"/>'
def path(d, col, w=8, fill='none', op=1, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{ds}/>'
def check(cx, cy, r=30):
    return circ(cx, cy, r, SD) + path(f'M{cx-r*.45} {cy} L{cx-r*.12} {cy+r*.33} L{cx+r*.5} {cy-r*.33}', '#fff', r * .27)
def nope(cx, cy, r=30):
    k = r * .38
    return circ(cx, cy, r, TD) + path(f'M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}', '#fff', r * .27)
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def badge(cx, cy, label, col=SAGE, w=200, ink=CARD, size=36, h=64):
    return rr(cx - w / 2, cy - h / 2, w, h, h / 2, col) + text(cx, cy + size * .36, label, size, ink)
def snow(cx, cy, s, col=SKYD):
    out = ''
    for a in range(3):
        t = math.radians(a * 60)
        dx, dy = s * math.cos(t), s * math.sin(t)
        out += path(f'M{cx-dx} {cy-dy} L{cx+dx} {cy+dy}', col, s * .22)
    return out + circ(cx, cy, s * .2, col)
def clock(cx, cy, r, h=2, m=0, col=SUND):
    ha = math.radians(h * 30 - 90); ma = math.radians(m * 6 - 90)
    return (circ(cx, cy, r + 10, col) + circ(cx, cy, r, CARD) +
            ''.join(circ(cx + r * .78 * math.cos(math.radians(k * 30)), cy + r * .78 * math.sin(math.radians(k * 30)), r * .05, LINE) for k in range(12)) +
            path(f'M{cx} {cy} L{cx+r*.48*math.cos(ha)} {cy+r*.48*math.sin(ha)}', INK, r * .1) +
            path(f'M{cx} {cy} L{cx+r*.7*math.cos(ma)} {cy+r*.7*math.sin(ma)}', INK, r * .07) + circ(cx, cy, r * .07, TD))
def sunico(cx, cy, r):
    rays = ''.join(path(f'M{cx+r*1.35*math.cos(a)} {cy+r*1.35*math.sin(a)} L{cx+r*1.7*math.cos(a)} {cy+r*1.7*math.sin(a)}', SUN, r * .22) for a in [i * math.pi / 4 for i in range(8)])
    return rays + circ(cx, cy, r, SUN)
def moon(cx, cy, r, bg=CARD):
    return circ(cx, cy, r, SUND) + circ(cx + r * .45, cy - r * .3, r * .85, bg)
def bag(cx, cy, s=1, rot=0, lab=None):
    """ASI storage bag (same look as w3n-asip): tapered pouch, zip line, milk to two-thirds."""
    t = (f'<rect x="-34" y="-44" width="68" height="28" rx="6" fill="{SUN}" opacity="0.85"/>' + text(0, -22, lab, 22, INK)) if lab else \
        f'<rect x="-30" y="-40" width="60" height="18" rx="4" fill="{SUN}" opacity="0.8"/>'
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            f'<path d="M-44 -70 L44 -70 L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="{CARD}" stroke="{FRD}" stroke-width="4"/>'
            f'<path d="M-46 -6 L46 -6 L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="{MILK}"/>'
            f'<path d="M-44 -56 L44 -56" stroke="{SKYD}" stroke-width="5" stroke-linecap="round"/>' + t +
            f'<ellipse cx="-22" cy="26" rx="8" ry="18" fill="#fff" opacity="0.5"/></g>')
def leafy(cx, cy, s=1, rot=0):
    """A small sprig of katuk: a stem with paired oval leaves."""
    out = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">' + path('M0 60 L0 -70', LEAFD, 6)
    for i, y in enumerate(range(40, -80, -26)):
        out += f'<ellipse cx="-20" cy="{y}" rx="20" ry="10" fill="{LEAF if i % 2 else LEAFD}" transform="rotate(-25 -20 {y})"/>'
        out += f'<ellipse cx="20" cy="{y-8}" rx="20" ry="10" fill="{LEAFD if i % 2 else LEAF}" transform="rotate(25 20 {y-8})"/>'
    return out + '</g>'
def glass(x, y, w, h):
    return (f'<path d="M{x} {y} L{x+w} {y} L{x+w*.88} {y+h} L{x+w*.12} {y+h} Z" fill="{CARD}" stroke="{FRD}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{x+w*.04} {y+h*.25} L{x+w*.96} {y+h*.25} L{x+w*.88} {y+h-3} L{x+w*.12} {y+h-3} Z" fill="{WATER}"/>'
            + rr(x + w * .2, y + h * .35, w * .1, h * .45, w * .05, '#fff', op=.7))
def pillow(cx, cy, w, f=CARD):
    h = w * 0.55
    return f'<path d="M{cx-w/2} {cy-h/2} Q{cx} {cy-h/2+14} {cx+w/2} {cy-h/2} Q{cx+w/2-14} {cy} {cx+w/2} {cy+h/2} Q{cx} {cy+h/2-14} {cx-w/2} {cy+h/2} Q{cx-w/2+14} {cy} {cx-w/2} {cy-h/2} Z" fill="{f}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
def thermo(x, y, s=1, col=TERRA):
    return (f'<g transform="translate({x} {y}) scale({s})">' + rr(-18, -110, 36, 150, 18, CARD, FRD, 6) +
            rr(-8, -70, 16, 110, 8, col) + circ(0, 56, 30, col) + circ(-8, 48, 8, '#fff', .5) +
            ''.join(path(f'M18 {-90+i*26} L30 {-90+i*26}', FRD, 5) for i in range(4)) + '</g>')
def icepack(cx, cy, w, rot=0):
    """Ice pack wrapped in a cloth: blue gel pack, cloth fold over it, snowflake."""
    h = w * .62
    return (f'<g transform="rotate({rot} {cx} {cy})">' + rr(cx - w / 2, cy - h / 2, w, h, h * .3, ICE, ICED, 6) +
            f'<path d="M{cx-w/2-8} {cy-h*.05} L{cx+w/2+8} {cy-h*.05} L{cx+w/2+8} {cy+h/2+6} Q{cx} {cy+h/2+22} {cx-w/2-8} {cy+h/2+6} Z" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>'
            + path(f'M{cx-w*.35} {cy+h*.18} L{cx+w*.35} {cy+h*.18}', BLUSH, 7, op=.9) + path(f'M{cx-w*.35} {cy+h*.34} L{cx+w*.35} {cy+h*.34}', BLUSH, 7, op=.9)
            + snow(cx, cy - h * .2, h * .16) + '</g>')
def fist(cx, cy, s=1):
    sk, skd = P.SKIN, P.SKIND
    return (f'<g transform="translate({cx} {cy}) scale({s})">' + rr(-70, -10, 140, 140, 30, P.OUTFIT['mama'][1]) +
            rr(-80, -110, 160, 120, 46, sk) + ''.join(path(f'M{-40+i*36} -110 L{-40+i*36} -62', skd, 7) for i in range(3)) +
            rr(-92, -80, 44, 70, 22, skd) + '</g>')
def hand_open(cx, cy, s=1, rot=0):
    sk, skd = P.SKIN, P.SKIND
    fingers = ''.join(rr(-58 + i * 32, -150 + abs(i - 1.5) * 14, 26, 90, 13, sk) for i in range(4))
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">' + rr(-60, 20, 120, 120, 30, P.OUTFIT['mama'][1]) +
            fingers + rr(-66, -80, 132, 120, 44, sk) + f'<path d="M50 -10 Q100 -40 104 -84" stroke="{sk}" stroke-width="30" fill="none" stroke-linecap="round"/>' +
            path('M-30 -10 Q0 4 30 -10', skd, 6) + '</g>')
def clinic(cx, base, w):
    h = w * .62
    x = cx - w / 2
    return (rr(x, base - h, w, h, 16, CARD, LINE, 6) + f'<path d="M{x-20} {base-h+6} L{cx} {base-h-w*.3} L{x+w+20} {base-h+6} Z" fill="{SAGE}"/>' +
            rr(cx - w * .14, base - h * .52, w * .28, h * .52, 10, SKY) + rr(x + w * .1, base - h * .7, w * .2, h * .22, 8, ICE) + rr(x + w * .7, base - h * .7, w * .2, h * .22, 8, ICE) +
            rr(cx - 9, base - h - w * .2, 18, 56, 6, CARD) + rr(cx - 28, base - h - w * .2 + 19, 56, 18, 6, CARD))
def pills(cx, cy, w, rot=0):
    h = w * .6
    dots = ''.join(circ(cx - w * .3 + i * w * .3, cy - h * .2 + j * h * .4, h * .14, CARD) + circ(cx - w * .3 + i * w * .3, cy - h * .2 + j * h * .4, h * .1, BLUSH)
                   for i in range(3) for j in range(2))
    return f'<g transform="rotate({rot} {cx} {cy})">' + rr(cx - w / 2, cy - h / 2, w, h, 14, GREY) + dots + '</g>'
def arrows_out(cx, cy, r, col=TD):
    out = ''
    for a in [i * math.pi / 4 + math.pi / 8 for i in range(8)]:
        x0, y0, x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a), cx + (r + 44) * math.cos(a), cy + (r + 44) * math.sin(a)
        out += path(f'M{x0} {y0} L{x1} {y1}', col, 9)
        for d in (-0.5, 0.5):
            out += path(f'M{x1} {y1} L{x1-16*math.cos(a+d)} {y1-16*math.sin(a+d)}', col, 9)
    return out
def swap(cx, cy, r, col=SAGE):
    """Two curved arrows in a circle: switch sides."""
    return (path(f'M{cx-r} {cy} A{r} {r} 0 0 1 {cx+r*.9} {cy-r*.42}', col, 12) + path(f'M{cx+r*.9} {cy-r*.42} l-34 -4 M{cx+r*.9} {cy-r*.42} l4 -34', col, 12) +
            path(f'M{cx+r} {cy} A{r} {r} 0 0 1 {cx-r*.9} {cy+r*.42}', col, 12) + path(f'M{cx-r*.9} {cy+r*.42} l34 4 M{cx-r*.9} {cy+r*.42} l-4 34', col, 12))
def chip(cx, cy, label, col=SAGE, ink=CARD, size=30):
    w = len(label) * size * .58 + 44
    return badge(cx, cy, label, col, w, ink, size, size * 1.8)


# ------------------------------------------------------------------ Mama holding a wrapped baby
def baby_head(cx, cy, rb, expr='lembut'):
    h = P.person('adek', cx, cy, rb / 54, expr, 'none')
    return h[h.index('<ellipse'):]
def mama_baby(cx, cy, s, expr='lembut', baby='lembut', blanket=BLUSH, blanketd=TERRA, big_blanket=False):
    """Mama (hijab) holds a swaddled baby across her chest. Only faces show: the blanket covers the rest."""
    r = 62 * s; ty = cy + 0.95 * r
    col, cold = P.OUTFIT['mama']
    out = P.person('mama', cx, cy, s, expr, 'none')
    hx, hy, rb = cx - 0.82 * r, ty + 0.62 * r, 0.5 * r
    out += baby_head(hx, hy, rb, baby)
    # the bundle
    bx, by = cx + 0.12 * r, ty + 1.32 * r
    rx, ry = (1.62 * r, 0.86 * r) if big_blanket else (1.38 * r, 0.66 * r)
    out += f'<ellipse cx="{bx}" cy="{by}" rx="{rx}" ry="{ry}" fill="{blanket}" transform="rotate(-14 {bx} {by})"/>'
    # blanket hem tucked under the baby's chin
    out += (f'<path d="M{hx-rb*1.05} {hy+rb*0.55} Q{hx+rb*0.2} {hy+rb*1.25} {hx+rb*1.6} {hy+rb*0.35} L{hx+rb*1.9} {hy+rb*1.1} Q{hx} {hy+rb*1.9} {hx-rb*1.2} {hy+rb*1.2} Z" fill="{blanket}"/>'
            f'<path d="M{hx-rb*1.0} {hy+rb*0.62} Q{hx+rb*0.2} {hy+rb*1.3} {hx+rb*1.6} {hy+rb*0.42}" stroke="{blanketd}" stroke-width="{r*0.07}" fill="none" opacity="0.45" stroke-linecap="round"/>')
    out += path(f'M{bx-rx*0.1} {by+ry*0.1} Q{bx+rx*0.35} {by+ry*0.25} {bx+rx*0.7} {by-ry*0.2}', blanketd, r * 0.06, op=.35)
    # Mama's forearm in front, under the bundle, hand near the baby's head
    out += path(f'M{cx+1.22*r} {ty+0.5*r} Q{cx+1.45*r} {ty+2.0*r} {cx-0.25*r} {ty+1.92*r} Q{cx-0.9*r} {ty+1.85*r} {cx-1.25*r} {ty+1.3*r}', cold, r * 0.42)
    out += circ(cx - 1.3 * r, ty + 1.2 * r, r * 0.24, P.SKIN)
    return out


H, T = 520, 470
def mb_cy(s, top): return top - 3.0 * 62 * s   # head centre so the whole bundle sits above the table

# ================================================================== 1. w4l-asi-naik
# HERO: Mama holds the baby close; a bowl of katuk sits to the side, small
m = mb_cy(1.5, T)
b = (mama_baby(330, m, 1.5) + P.table(T, H) +
     heart(560, 110, 26) + heart(610, 170, 16, BLUSH) +
     shadow(730, T + 26, 110) + leafy(695, T - 70, .8, -18) + leafy(735, T - 76, .85, 4) + leafy(775, T - 66, .8, 22) +
     bowl(735, T - 20, 210, CARD, LINE) + chip(735, T + 24, 'katuk', LEAF, CARD, 28) + text(735, T - 150, '?', 70, SUND))
save('hero-w4c-asi-katuk', H, b)

# 1: supply follows demand. Mama + baby, a clock with 8-12x, sun and moon
m = mb_cy(1.36, T)
b = (mama_baby(260, m, 1.36) + P.table(T, H) +
     clock(660, 210, 110, 10, 10) + badge(660, 390, '8-12x sehari', SUN, 300, INK, 40) +
     sunico(520, 70, 24) + moon(800, 70, 28, '#fbf4ea'))
save('big-w4c-asi-sering', H, b)

# 2: latch, as a baby face: mouth wide open, lower lip turned out
def latch_face(cx, cy, rb):
    h = P.person('adek', cx, cy, rb / 54, 'senang', 'none')
    h = h[h.index('<ellipse'):]
    # cover the default mouth with skin, then draw the wide mouth
    my = cy + rb * 0.38
    h += f'<ellipse cx="{cx}" cy="{my+rb*0.05}" rx="{rb*0.32}" ry="{rb*0.22}" fill="{P.SKIN}"/>'
    h += f'<ellipse cx="{cx}" cy="{my+rb*0.12}" rx="{rb*0.3}" ry="{rb*0.26}" fill="#7a3b2c"/>'
    h += f'<path d="M{cx-rb*0.22} {my+rb*0.3} Q{cx} {my+rb*0.16} {cx+rb*0.22} {my+rb*0.3} Q{cx} {my+rb*0.4} {cx-rb*0.22} {my+rb*0.3} Z" fill="#f29a86"/>'
    h += f'<path d="M{cx-rb*0.3} {my+rb*0.3} Q{cx} {my+rb*0.56} {cx+rb*0.3} {my+rb*0.3}" stroke="#e9907a" stroke-width="{rb*0.07}" fill="none" stroke-linecap="round"/>'
    return h
b = (shadow(330, 470, 170) + rr(170, 330, 320, 150, 70, BLUSH) + latch_face(330, 230, 140) +
     path('M520 250 L600 190', SAGE, 7) + chip(700, 170, 'buka lebar', SAGE, CARD, 32) + check(830, 170, 26) +
     path('M470 320 L600 350', SAGE, 7) + chip(705, 350, 'bibir keluar', SAGE, CARD, 32) + check(840, 350, 26))
save('big-w4c-asi-pelekatan', 500, b)

# 3: skin to skin, under one blanket, hearts
m = mb_cy(1.3, T) - 20
b = (mama_baby(440, m, 1.3, 'senang', 'lembut', SKY, SKYD, big_blanket=True) + P.table(T, H) +
     heart(170, 170, 34) + heart(120, 250, 20, BLUSH) + heart(710, 150, 30, TERRA) + heart(770, 230, 18, SUN) +
     chip(440, T + 26, 'kulit ke kulit', SAGE, CARD, 32))
save('big-w4c-asi-skin', H, b)

# 4: two sides, switch: two ASI bags (kiri, kanan) and switch arrows
b = (floor(380, 480) + shadow(220, 440, 110) + shadow(660, 440, 110) +
     bag(220, 290, 1.4, -6, 'kiri') + bag(660, 290, 1.4, 6, 'kanan') + swap(440, 230, 90) + check(440, 400, 32))
save('big-w4c-asi-dua', 480, b)

# 5: Mama gets fed and rests: plate of rice with katuk, a glass of water, a pillow and moon
b = (floor(360, 470) + shadow(220, 430, 160) + rr(60, 300, 320, 70, 35, CARD, LINE, 6) +
     f'<ellipse cx="180" cy="300" rx="80" ry="44" fill="{RICE}" stroke="{LINE}" stroke-width="4"/>' +
     leafy(290, 270, .55, 60) + leafy(300, 300, .5, 80) + f'<ellipse cx="110" cy="320" rx="34" ry="22" fill="{SUN}"/><ellipse cx="110" cy="320" rx="14" ry="10" fill="{SUND}"/>' +
     shadow(480, 430, 60) + glass(430, 190, 100, 220) + badge(480, 130, '12-14 gelas', SKY, 230, INK, 30, 56) +
     shadow(720, 430, 140) + pillow(720, 330, 260, CARD) + moon(770, 140, 44, '#fbf4ea') +
     text(660, 200, 'z', 46, SKYD) + text(700, 160, 'z', 36, SKYD))
save('big-w4c-asi-ibu', 470, b)

# cheat icons (square-ish, read at 64-200 px)
save('big-w4c-ic-sering', 300, clock(150, 140, 100, 10, 10) + badge(150, 268, '8-12x', SUN, 170, INK, 40))
save('big-w4c-ic-latch', 300, latch_face(150, 130, 110))
mi = P.seat('mama', 1.0, 300)
save('big-w4c-ic-skin', 330, mama_baby(150, mb_cy(1.0, 300) - 10, 1.0, 'senang', 'lembut', SKY, SKYD, True))
save('big-w4c-ic-dua', 300, bag(80, 160, .95, -6, 'kiri') + bag(220, 160, .95, 6, 'kanan') + swap(150, 160, 40))
save('big-w4c-ic-konselor', 300, clinic(150, 280, 230) + heart(240, 60, 22))

# ================================================================== 2. w4l-mastitis
# HERO: Mama holds a cold pack, snowflakes. Off to the side: a fist (urut keras) crossed out
m = T - 1.5 * 62 * 2.08 - 90
b = (P.person('mama', 320, m, 1.5, 'lembut', 'pegang') + icepack(320, m + 1.5 * 62 * 2.0, 200, -4) + P.table(T, H) +
     snow(110, 110, 30) + snow(560, 90, 22) + snow(150, 260, 18) +
     circ(320 - 112, m + 1.5 * 62 * 2.0 + 10, 26, P.SKIN) + circ(320 + 112, m + 1.5 * 62 * 2.0 + 4, 26, P.SKIN) +
     fist(720, 330, .95) + chip(700, 110, 'urut keras', TD, CARD, 32) + nope(830, 110, 34))
save('hero-w4c-mas-dingin', H, b)

# 1: signs. Mama tired and feverish, thermometer, warm waves
m = T - 1.6 * 62 * 2.1
b = (P.person('mama', 260, m, 1.6, 'capek', 'tangan-dada') + P.table(T, H) +
     thermo(560, 300, 1.25) + path('M560 70 q14 -16 0 -32 q-14 -16 0 -32', TERRA, 8, op=.7) + path('M600 90 q14 -16 0 -32 q-14 -16 0 -32', TERRA, 8, op=.5) +
     chip(750, 150, 'demam', TD, CARD, 34) + chip(750, 250, 'menggigil', SKYD, CARD, 34) + chip(750, 350, 'pegal', SUND, INK, 34))
save('big-w4c-mas-tanda', H, b)

# 2: keep feeding as usual: Mama holds the baby, check and heart
m = mb_cy(1.44, T)
b = (mama_baby(360, m, 1.44, 'lembut', 'lembut') + P.table(T, H) + check(700, 180, 44) + heart(130, 160, 30) + heart(720, 300, 20, BLUSH) +
     chip(700, 90, 'ASI aman', SAGE, CARD, 32))
save('big-w4c-mas-susui', H, b)

# 3: no hard kneading (fist, nope) / light stroke on the skin (open hand, soft sweep, check)
b = (floor(400, 500) + shadow(220, 470, 120) + fist(220, 330, 1.05) + path('M140 150 l-20 -24 M220 140 l0 -30 M300 150 l20 -24', TD, 9) +
     nope(330, 120, 36) + chip(220, 450, 'keras', TD, CARD, 32) +
     shadow(640, 470, 120) + hand_open(640, 330, 1.0, 8) +
     path('M520 150 Q600 110 680 140 Q750 165 800 130', SAGE, 9, dash='4 18') + path('M540 200 Q620 165 700 190', SAGE, 7, op=.6, dash='4 18') +
     check(800, 230, 34) + chip(640, 450, 'lembut', SAGE, CARD, 32))
save('big-w4c-mas-pijat', 500, b)

# 4: no pumping to empty: a pile of bags (nope) / just enough, one bag (check)
pile = ''.join(bag(x, y, .62, r) for x, y, r in ((120, 330, -8), (200, 340, 6), (280, 330, -4), (160, 240, 5), (240, 245, -7), (200, 160, 3)))
b = (floor(400, 500) + shadow(200, 440, 150) + pile + nope(330, 120, 36) + chip(200, 460, 'sampai kosong', TD, CARD, 30) +
     shadow(640, 440, 90) + bag(640, 310, 1.1, 4) + check(760, 190, 36) + chip(640, 460, 'secukupnya', SAGE, CARD, 30))
save('big-w4c-mas-pompa', 500, b)

# 5: cold pack, every hour if wanted / pain relief: ask the doctor
b = (floor(380, 480) + shadow(220, 440, 150) + icepack(220, 320, 250, -6) + snow(100, 150, 26) + snow(340, 120, 20) +
     clock(470, 160, 62, 1, 0) + badge(470, 270, 'tiap jam', SUN, 190, INK, 30, 56) +
     shadow(720, 440, 100) + pills(720, 360, 170, 8) + chip(720, 250, 'tanya dokter', SAGE, CARD, 28))
save('big-w4c-mas-kompres', 480, b)

# cheat icons for "ke dokter kalau"
save('big-w4c-ic-demam', 300, thermo(110, 170, 1.0) + badge(210, 250, '24 jam', TD, 160, CARD, 34) + path('M200 60 q12 -14 0 -28 q-12 -14 0 -28', TERRA, 7, op=.7))
save('big-w4c-ic-jam', 300, clock(150, 130, 100, 12, 0) + badge(150, 262, '12-24 jam', SUN, 210, INK, 34))
save('big-w4c-ic-meluas', 300, circ(150, 150, 120, PALE) + circ(150, 150, 74, BLUSH) + circ(150, 150, 38, TERRA, .7) + arrows_out(150, 150, 70))
save('big-w4c-ic-benjol', 300, circ(150, 150, 120, PALE) + circ(150, 150, 70, BLUSH) +
     f'<path d="M150 98 Q192 150 186 174 Q178 206 150 206 Q122 206 114 174 Q108 150 150 98 Z" fill="{SUN}"/>' + circ(138, 170, 10, '#fff', .6))

autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=360))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 5; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (360 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 360, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
