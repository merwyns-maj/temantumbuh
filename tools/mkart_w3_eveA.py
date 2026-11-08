# Design v2 scenes for the w3 evening batch eveA (9 to 11 Nov):
#   w3e-adhd, w3e-newborn-skip, w3e-mitos-2.  Run: python tools/mkart_w3_eveA.py [contact.png]
# Every name starts with "w3a-" so it never collides with other batches.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *
import people as P

GREY = '#c8c2b8'; GREYL = '#e2ddd5'; DARK = '#3b3f4a'; MINT = '#e3eee6'; SEPIA = '#efe2cf'
BANANA = '#f5d76e'; BANANAD = '#d9b23c'; BROWN = '#9a5b3a'; BROWND = '#7a4429'
NAMES = []


def save(name, h, body):
    svg(name, h, body); NAMES.append(name)


# ------------------------------------------------------------------ small kit
def rr(x, y, w, h, r, f, st=None, sw=0, op=1):
    s = f' stroke="{st}" stroke-width="{sw}"' if st else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"{s} opacity="{op}"/>'
def circ(cx, cy, r, f, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" opacity="{op}"/>'
def line(x1, y1, x2, y2, col, w=8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}/>'
def path(d, col, w=8, fill='none', dash=None, op=1):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{ds} opacity="{op}"/>'
def check(cx, cy, r=30):
    return circ(cx, cy, r, SD) + path(f'M{cx-r*.45} {cy} L{cx-r*.12} {cy+r*.33} L{cx+r*.5} {cy-r*.33}', '#fff', r * .27)
def nope(cx, cy, r=30):
    k = r * .38
    return circ(cx, cy, r, TD) + path(f'M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}', '#fff', r * .27)
def spark(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def ball(cx, cy, r, f=TERRA, s=SUN):
    return (circ(cx, cy, r, f) + f'<path d="M{cx-r} {cy} Q{cx} {cy-r*.55} {cx+r} {cy}" stroke="{s}" stroke-width="{r*.22}" fill="none"/>' +
            circ(cx - r * .35, cy - r * .4, r * .18, '#fff', .45))
def block(x, y, s, f, fd, rot=0):
    return f'<g transform="rotate({rot} {x+s/2} {y+s/2})">' + rr(x, y, s, s, 10, f) + rr(x, y + s * .72, s, s * .28, 8, fd, op=.6) + circ(x + s / 2, y + s * .4, s * .16, '#fff', .45) + '</g>'
def book(x, y, w, h, f, fd, rot=0, lab=None):
    t = text(x + w * .58, y + h * .56, lab, h * .2, '#fff') if lab else rr(x + w * .3, y + h * .2, w * .5, h * .14, 6, '#fff', op=.55)
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">' + rr(x, y, w, h, 12, f) + rr(x, y, w * .16, h, 10, fd) + t + '</g>')
def cushion(x, y, w, h, f, fd):
    return rr(x, y, w, h, h * .45, f) + rr(x, y + h * .62, w, h * .38, h * .3, fd, op=.5) + circ(x + w / 2, y + h * .45, 6, fd)
def steth(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})">' + path('M0 0 Q-10 90 50 110 Q110 120 120 40', INK, 12) + path('M120 40 L130 0 M120 40 L108 2', INK, 10) +
            path('M50 110 Q60 170 110 175', INK, 12) + circ(122, 178, 28, GREY) + circ(122, 178, 16, GREYL) + circ(0, 0, 8, MUTED) + circ(130, 0, 8, MUTED) + '</g>')
def tv(x, y, w, h, screen=DARK):
    return (line(x + w * .3, y + h, x + w * .2, y + h + 50, INK, 10) + line(x + w * .7, y + h, x + w * .8, y + h + 50, INK, 10) +
            rr(x, y, w, h, 22, INK) + rr(x + 16, y + 16, w - 32, h - 32, 12, screen))
def clock(cx, cy, r, wedge=True):
    b = circ(cx, cy, r + 12, INK) + circ(cx, cy, r, CARD)
    if wedge:  # one hour out of twelve
        b += f'<path d="M{cx} {cy} L{cx} {cy-r} A{r} {r} 0 0 1 {cx+r*0.5} {cy-r*0.866} Z" fill="{SUN}"/>'
    return b + line(cx, cy, cx, cy - r * .72, INK, 8) + line(cx, cy, cx + r * .5, cy - r * .1, INK, 8) + circ(cx, cy, 7, TD)
def calendar(x, y, w, big, small=None):
    h = w * 0.9
    s = rr(x, y, w, h, 18, CARD, LINE, 6) + rr(x, y, w, h * 0.26, 18, TERRA) + rr(x, y + h * 0.16, w, h * 0.1, 0, TERRA)
    s += rr(x + w * 0.25, y - 14, 14, 34, 7, INK) + rr(x + w * 0.7, y - 14, 14, 34, 7, INK)
    s += text(x + w / 2, y + h * (0.66 if small else 0.8), big, w * 0.36, INK)
    if small:
        s += text(x + w / 2, y + h * 0.88, small, w * 0.15, MUTED)
    return s
def rug(cx, cy, rx, ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{MINT}"/><ellipse cx="{cx}" cy="{cy}" rx="{rx-22}" ry="{ry-12}" fill="none" stroke="{SAGE}" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round"/>'
def pillow(cx, cy, w, f='#fff'):
    h = w * 0.55
    return f'<path d="M{cx-w/2} {cy-h/2} Q{cx} {cy-h/2+14} {cx+w/2} {cy-h/2} Q{cx+w/2-14} {cy} {cx+w/2} {cy+h/2} Q{cx} {cy+h/2-14} {cx-w/2} {cy+h/2} Q{cx-w/2+14} {cy} {cx-w/2} {cy-h/2} Z" fill="{f}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
def shirt(cx, cy, w, f):
    h = w * 0.85
    return (f'<path d="M{cx-w*0.22} {cy-h/2} Q{cx} {cy-h*0.36} {cx+w*0.22} {cy-h/2} L{cx+w/2} {cy-h*0.3} L{cx+w*0.38} {cy-h*0.08} L{cx+w*0.28} {cy-h*0.14} '
            f'L{cx+w*0.28} {cy+h/2} L{cx-w*0.28} {cy+h/2} L{cx-w*0.28} {cy-h*0.14} L{cx-w*0.38} {cy-h*0.08} L{cx-w/2} {cy-h*0.3} Z" fill="{f}" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>')
def breath(x, y, col=SKY):
    return (f'<path d="M{x} {y} q30 -16 56 0 q26 16 56 0" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x+20} {y+30} q26 -14 50 0 q22 14 46 0" stroke="{col}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.7"/>')
def crib(x, y, w, h):
    mat = y + h * 0.56
    back = rr(x, y - 16, 24, h + 16, 10, BOXD) + rr(x + w - 24, y - 16, 24, h + 16, 10, BOXD)
    for sx in range(int(x + 50), int(x + w - 40), 44):
        back += rr(sx, y + 10, 12, mat - y - 10, 6, BOX)
    back += rr(x, y, w, 22, 11, BOX)
    back += rr(x + 18, mat, w - 36, 34, 12, CARD, LINE, 5)
    front = rr(x, mat + 32, w, 22, 11, BOXD)
    return back, front, mat
def jar(x, y, w, h, lab='madu'):
    return (rr(x + w * .12, y, w * .76, h * .16, 12, BOXD) + rr(x, y + h * .14, w, h * .86, 34, SUN) +
            rr(x + w * .62, y + h * .2, w * .26, h * .74, 22, SUND, op=.55) + rr(x + w * .14, y + h * .42, w * .72, h * .3, 14, CARD) +
            text(x + w / 2, y + h * .63, lab, w * .2, SUND))
def cake(cx, base, w, n):
    h = w * .55
    return (rr(cx - w / 2, base - h, w, h, 18, BLUSH) + rr(cx - w / 2, base - h, w, h * .3, 18, CARD) +
            ''.join(circ(cx - w / 2 + 24 + i * (w - 48) / 4, base - h * .7, 8, CARD) for i in range(5)) +
            rr(cx - w / 2 - 14, base - 12, w + 28, 16, 8, GREYL) +
            rr(cx - 12, base - h - 60, 24, 62, 8, SKY) + f'<path d="M{cx} {base-h-100} Q{cx+16} {base-h-76} {cx} {base-h-62} Q{cx-16} {base-h-76} {cx} {base-h-100} Z" fill="{SUN}"/>' +
            text(cx + 60, base - h - 30, n, 64, TD))
def banana(cx, cy, s, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx-s} {cy-s*.2} Q{cx} {cy+s*.9} {cx+s} {cy-s*.3} Q{cx} {cy+s*.35} {cx-s} {cy-s*.2} Z" fill="{BANANA}"/>'
            f'<path d="M{cx-s*.2} {cy+s*.32} Q{cx+s*.5} {cy+s*.25} {cx+s} {cy-s*.3}" stroke="{BANANAD}" stroke-width="{s*.08}" fill="none"/>'
            f'<rect x="{cx+s*.92}" y="{cy-s*.42}" width="{s*.16}" height="{s*.2}" rx="4" fill="{BROWND}" transform="rotate(-30 {cx+s} {cy-s*.3})"/></g>')
def bottle(x, y, w, h, f, cap, lab=None, labcol=CARD):
    return (rr(x + w * .3, y, w * .4, h * .16, 6, cap) + rr(x + w * .22, y + h * .12, w * .56, h * .1, 6, f) +
            rr(x, y + h * .2, w, h * .8, w * .22, f) + rr(x + w * .62, y + h * .26, w * .22, h * .66, w * .1, '#000', op=.08) +
            (rr(x + w * .14, y + h * .48, w * .72, h * .3, 8, labcol) + (text(x + w / 2, y + h * .69, lab, w * .26, f) if lab else '')))
def powder(x, y, w, h, rot=0):
    holes = ''.join(circ(x + w * (.32 + .18 * i), y + h * .06, 4, GREY) for i in range(3))
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">' + rr(x + w * .1, y, w * .8, h * .12, 14, GREYL) + holes +
            rr(x, y + h * .1, w, h * .9, w * .3, CARD, LINE, 5) + rr(x + w * .15, y + h * .45, w * .7, h * .25, 10, SKY) +
            circ(x + w * .5, y + h * .575, h * .07, CARD) + '</g>')
def cloud(cx, cy, s, col='#fff', op=.95):
    return ''.join(circ(cx + dx * s, cy + dy * s, r * s, col, op) for dx, dy, r in ((0, 0, 30), (-34, 8, 22), (32, 10, 24), (-12, -18, 20), (18, -16, 18))) + \
        ''.join(circ(cx + dx * s, cy + dy * s, 4 * s, GREY, .8) for dx, dy in ((-50, -30), (54, -26), (-20, -46), (40, 40), (-56, 30)))
def gurita(cx, cy, w):
    h = w * .32
    ties = ''.join(rr(cx + w / 2 - 6, cy - h / 2 + 8 + i * h * .3, 70, 16, 8, BLUSH) for i in range(3)) + \
        ''.join(rr(cx - w / 2 - 64, cy - h / 2 + 8 + i * h * .3, 70, 16, 8, BLUSH) for i in range(3))
    return ties + rr(cx - w / 2, cy - h / 2, w, h, 18, CARD, LINE, 6) + path(f'M{cx-w/2+20} {cy} L{cx+w/2-20} {cy}', LINE, 5, dash='2 14')
def cord_belly(cx, cy, s):
    """Flat icon: a baby tummy seen from the front, the cord stump and clamp left open, nothing on it."""
    sk = '#f3cba5'; skd = '#e2ad83'
    return (rr(cx - 150 * s, cy - 120 * s, 300 * s, 240 * s, 120 * s, sk) + rr(cx + 40 * s, cy - 110 * s, 100 * s, 220 * s, 60 * s, skd, op=.25) +
            path(f'M{cx} {cy+10*s} q22 -26 8 -60', '#b98f6a', 18 * s) + rr(cx - 20 * s, cy - 70 * s, 50 * s, 20 * s, 8 * s, SKY) +
            circ(cx - 70 * s, cy - 20 * s, 10 * s, skd, .5) + circ(cx + 70 * s, cy - 20 * s, 10 * s, skd, .5))
def diaper_fold(cx, top, w):
    """Diaper seen from the front with its waistband folded down, sitting below the tummy icon."""
    h = w * .55
    return (f'<path d="M{cx-w/2} {top} L{cx+w/2} {top} L{cx+w*.42} {top+h*.6} Q{cx} {top+h*1.05} {cx-w*.42} {top+h*.6} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>' +
            rr(cx - w / 2 - 6, top - 16, w + 12, 30, 14, GREYL) + path(f'M{cx-w*.3} {top+30} Q{cx} {top+48} {cx+w*.3} {top+30}', LINE, 5))
def walker(cx, base, s=1):
    w = 220 * s
    return (f'<ellipse cx="{cx}" cy="{base-14*s}" rx="{w*.55}" ry="{24*s}" fill="{SKYD}"/>' +
            ''.join(circ(cx + k * w * .45, base - 4 * s, 14 * s, INK) for k in (-1, 1)) + circ(cx, base + 2 * s, 14 * s, INK) +
            path(f'M{cx-w*.5} {base-24*s} L{cx-w*.36} {base-150*s} M{cx+w*.5} {base-24*s} L{cx+w*.36} {base-150*s}', SKY, 18 * s) +
            f'<ellipse cx="{cx}" cy="{base-150*s}" rx="{w*.5}" ry="{30*s}" fill="{SUN}"/>' +
            f'<ellipse cx="{cx}" cy="{base-156*s}" rx="{w*.26}" ry="{14*s}" fill="{FLOOR}"/>' +
            circ(cx - w * .36, base - 158 * s, 10 * s, TERRA) + circ(cx + w * .36, base - 158 * s, 10 * s, SAGE))
def towel(cx, cy, w):
    h = w * .42
    return (rr(cx - w / 2, cy - h / 2, w, h, 16, SKY) + rr(cx - w / 2, cy - h / 2 + h * .55, w, h * .45, 14, SKYD, op=.6) +
            path(f'M{cx-w/2+16} {cy-h/2+16} L{cx+w/2-16} {cy-h/2+16}', '#fff', 5, dash='2 14', op=.8))
def hand(cx, cy, s):
    sk = '#f3cba5'; nail = '#fbe7dc'
    f = ''
    for i, (dx, L, rot) in enumerate(((-36, 60, -14), (-12, 74, -4), (12, 76, 4), (36, 66, 12))):
        f += f'<g transform="rotate({rot} {cx+dx*s} {cy-30*s})">' + rr(cx + (dx - 11) * s, cy - (30 + L) * s, 22 * s, (L + 10) * s, 11 * s, sk) + \
             rr(cx + (dx - 7) * s, cy - (28 + L) * s, 14 * s, 14 * s, 6 * s, nail, '#e2ad83', 2) + '</g>'
    thumb = f'<g transform="rotate(-50 {cx-46*s} {cy+10*s})">' + rr(cx - 58 * s, cy - 40 * s, 24 * s, 60 * s, 12 * s, sk) + '</g>'
    return thumb + f + rr(cx - 52 * s, cy - 40 * s, 104 * s, 90 * s, 38 * s, sk)
def clipper(x, y, s, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">' + rr(x, y, 150 * s, 30 * s, 14 * s, GREY) + rr(x, y - 22 * s, 140 * s, 24 * s, 12 * s, GREYL) +
            rr(x + 10 * s, y + 4 * s, 24 * s, 22 * s, 6 * s, SKYD) + circ(x + 120 * s, y + 4 * s, 10 * s, MUTED) + '</g>')
def moon_window(x, y, w, h):
    return (rr(x - 12, y - 12, w + 24, h + 24, 18, BOX) + rr(x, y, w, h, 10, SKYD) +
            circ(x + w * .66, y + h * .4, h * .2, SUN) + circ(x + w * .74, y + h * .33, h * .18, SKYD) +
            ''.join(circ(x + w * a, y + h * b, 5, '#fff', .85) for a, b in ((.2, .25), (.3, .7), (.85, .8))) +
            rr(x + w / 2 - 6, y, 12, h, 0, BOX) + rr(x, y + h / 2 - 6, w, 12, 0, BOX))
def card(x, y, w, h, inner, f=CARD):
    return rr(x + 4, y + 8, w, h, 24, '#000', op=.06) + rr(x, y, w, h, 24, f, LINE, 4) + inner
def arrow(x1, y, x2, col=MUTED):
    return line(x1, y, x2 - 10, y, col, 8) + f'<path d="M{x2} {y} L{x2-22} {y-16} L{x2-22} {y+16} Z" fill="{col}"/>'
def refresh(cx, cy, r, col=SD):
    return (circ(cx, cy, r, CARD, ) + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="4"/>' +
            path(f'M{cx+r*.5} {cy-r*.35} A{r*.55} {r*.55} 0 1 0 {cx+r*.55} {cy+r*.2}', col, r * .16) +
            f'<path d="M{cx+r*.62} {cy-r*.68} L{cx+r*.62} {cy-r*.22} L{cx+r*.18} {cy-r*.3} Z" fill="{col}"/>')
def motion(x, y, n=3, col=MUTED, left=True):
    k = -1 if left else 1
    return ''.join(line(x, y + i * 26, x + k * (60 - i * 12), y + i * 26, col, 7) for i in range(n))


# ================================================================== 1. w3e-adhd (1-3 tahun)
# HERO: Tunas mid-jump off a cushion pile, toys everywhere, motion lines
b = (floor(320, 420) + cushion(60, 270, 200, 60, BLUSH, TERRA) + cushion(80, 222, 160, 54, SKY, SKYD) +
     path('M170 200 Q260 40 380 120', MUTED, 6, dash='3 16') +
     shadow(470, 395, 70, 10) + tunas('hore', 170, 198, 385, 40) + motion(372, 120, 3) +
     spark(620, 70, 22) + spark(330, 40, 14, TERRA) +
     ball(660, 350, 40) + block(720, 260, 60, SUN, SUND, 14) + block(590, 300, 48, SAGE, SD, -10) +
     book(770, 330, 84, 60, SKY, SKYD, -12) + block(280, 340, 44, SUN, SUND, 20))
save('hero-w3a-adhd', 420, b)

# BIG: active and quick to switch toys: a loop from tower to ball to book
b = (floor(380, 500) + rug(440, 430, 380, 56) +
     block(80, 330, 60, SKY, SKYD) + block(86, 272, 54, SUN, SUND, 6) + block(140, 350, 44, TERRA, TD, -12) +
     ball(760, 380, 46, SAGE, SUN) + book(600, 395, 100, 66, BLUSH, TERRA, -8) +
     path('M170 300 Q260 120 420 170 Q600 230 700 300 Q760 200 640 160', MUTED, 6, dash='3 16') +
     shadow(420, 455, 90) + tunas('hore', 160, 186, 340, 260) + motion(330, 320, 3) +
     spark(560, 110, 20) + spark(250, 150, 14, TERRA))
save('big-w3a-aktif', 500, b)

# BIG: four steps, the flag on 4: ADHD is assessed from about age 4
steps = ''
for i in range(4):
    x = 300 + i * 130; top = 400 - (i + 1) * 62
    steps += rr(x, top, 130, 400 - top + 30, 10, [MINT, '#d3e5d8', '#c2dbc9', SAGE][i]) + text(x + 65, top + 50, str(i + 1), 44, SD if i < 3 else '#fff')
b = (floor(400, 500) + steps + line(780, 152, 780, 40, INK, 8) + f'<path d="M784 40 L860 62 L784 86 Z" fill="{TERRA}"/>' +
     shadow(190, 465, 90) + tunas('riset', 170, 198, 105, 270) + path('M250 250 Q420 60 740 70', MUTED, 6, dash='3 16') + spark(560, 40, 16))
save('big-w3a-umur-4', 500, b)

# BIG: a daily routine: makan, main, mandi, tidur
def ic_plate(cx, cy): return f'<ellipse cx="{cx}" cy="{cy+10}" rx="54" ry="20" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>' + circ(cx - 12, cy + 2, 14, SUN) + circ(cx + 14, cy + 6, 12, TERRA) + rr(cx + 52, cy - 30, 10, 60, 5, GREY)
def ic_tub(cx, cy): return f'<path d="M{cx-56} {cy-6} L{cx+56} {cy-6} Q{cx+52} {cy+40} {cx} {cy+40} Q{cx-52} {cy+40} {cx-56} {cy-6} Z" fill="{SKY}"/>' + ''.join(circ(cx + dx, cy - 18 + dy, r, '#fff', .9) for dx, dy, r in ((-20, 0, 12), (4, -10, 14), (26, 2, 10))) + line(cx - 40, cy + 40, cx - 46, cy + 54, SKYD, 8) + line(cx + 40, cy + 40, cx + 46, cy + 54, SKYD, 8)
def ic_moon(cx, cy): return circ(cx, cy, 42, SUN) + circ(cx + 18, cy - 14, 36, CARD) + spark(cx + 40, cy + 26, 10, SKYD)
cards = ''
for i, (ic, lab) in enumerate(((ic_plate, 'makan'), (lambda cx, cy: ball(cx, cy, 40), 'main'), (ic_tub, 'mandi'), (ic_moon, 'tidur'))):
    x = 20 + i * 215
    cards += card(x, 30, 180, 190, ic(x + 90, 105) + text(x + 90, 196, lab, 30, MUTED))
    if i < 3:
        cards += arrow(x + 184, 125, x + 212)
b = floor(330, 500) + cards + shadow(440, 480, 110) + tunas('santai', 200, 233, 340, 250) + spark(260, 300, 16) + spark(640, 290, 14, TERRA)
save('big-w3a-rutinitas', 500, b)

# BIG: room to move (cushion mountain, box tunnel), TV off with a 1-hour clock
b = (floor(360, 500) + rug(330, 440, 300, 48) +
     cushion(80, 340, 190, 60, BLUSH, TERRA) + cushion(110, 290, 140, 54, SAGE, SD) +
     rr(380, 330, 200, 110, 50, BOX) + rr(408, 360, 144, 80, 40, BOXD) + rr(380, 330, 200, 26, 12, BOXD, op=.5) +
     shadow(185, 296, 70, 9) + tunas('hore', 180, 210, 95, 92) + motion(90, 170, 3) +
     tv(650, 160, 190, 130) + clock(800, 130, 38) + spark(320, 120, 16) + ball(600, 440, 26, SKY, CARD))
save('big-w3a-ruang-gerak', 500, b)

# BIG: Mama and Adek ask the doctor; Buku KIA and a stethoscope on the table
T, H = 420, 520
m = P.seat('mama', 1.6, T); a = P.seat('adek', 1.45, T)
b = (P.person('mama', 190, m, 1.6, 'lembut', 'none') + P.person('adek', 440, a + 10, 1.45, 'senang', 'none') + P.table(T, H) +
     book(580, 300, 190, 130, BLUSH, TERRA, -6, 'KIA') + steth(740, 190, .8) +
     P.bubble(470, 0, 400, ['Dok, mau tanya'], 'bl', size=42))
save('big-w3a-tanya-dokter', H, b)

# BIG (cheat rows): normal at 1-3, and worth asking about
b = floor(300, 400) + rug(440, 350, 300, 40) + check(160, 170, 70) + ball(420, 300, 46, TERRA) + block(520, 250, 70, SUN, SUND, 10) + block(620, 290, 50, SAGE, SD, -12) + path('M330 220 Q420 120 540 160', MUTED, 6, dash='3 16')
save('big-w3a-cek-normal', 400, b)
b = (P.bubble(60, 60, 320, ['kata', '+  kata'], 'bl', size=44) + steth(560, 60, 1.0) + circ(470, 260, 6, MUTED, .5))
save('big-w3a-cek-bicara', 400, b)
b = (book(70, 120, 200, 140, BLUSH, TERRA, -6, 'KIA') + steth(400, 60, 1.0) + heart(720, 140, 40) + spark(640, 300, 18))
save('big-w3a-cek-dokter', 400, b)


# ================================================================== 2. w3e-newborn-skip (0-3 bulan)
def basket(x, y, w, h):
    weave = ''.join(path(f'M{x+14} {y+26+i*26} L{x+w-14} {y+26+i*26}', BOXD, 5, op=.5) for i in range(int(h / 30)))
    return (path(f'M{x+30} {y} Q{x+w/2} {y-h*.9} {x+w-30} {y}', BOXD, 12) +
            f'<path d="M{x} {y} L{x+w} {y} L{x+w-22} {y+h} L{x+22} {y+h} Z" fill="{BOX}"/>' + weave + rr(x - 10, y - 12, w + 20, 24, 12, BOXD))
b = (floor(320, 420) + shadow(420, 400, 170) +
     powder(290, 100, 80, 140, -14) + bottle(390, 120, 64, 120, BROWN, BROWND, None) + gurita(510, 150, 90) +
     basket(270, 240, 300, 140) +
     shadow(760, 400, 100) + walker(760, 390, .8) + nope(840, 220, 28) +
     shadow(130, 400, 90) + tunas('mikir', 180, 210, 40, 180) +
     f'<g transform="rotate(-10 420 300)">' + rr(335, 270, 170, 60, 14, TD) + text(420, 315, 'SKIP', 40, '#fff') + '</g>')
save('hero-w3a-newborn-skip', 420, b)

# BIG: powder puffs up (no) / soft towel pat-dry (yes)
b = (floor(360, 500) + powder(150, 130, 130, 230, -18) + cloud(330, 110, 1.3) + nope(130, 90, 36) +
     shadow(560, 450, 150) + towel(560, 410, 260) + check(700, 230, 36) +
     tunas('sayang', 170, 198, 475, 190))
save('big-w3a-bedak', 500, b)

# BIG: gurita (no) / soft top, room to breathe (yes)
b = (floor(380, 500) + gurita(230, 200, 220) + nope(230, 100, 36) + rr(160, 270, 140, 46, 23, BLUSH) + text(230, 302, 'gurita', 28, TD) +
     shirt(560, 300, 250, CARD) + rr(495, 312, 130, 14, 7, SKY, op=.6) + breath(620, 120) + check(720, 260, 34) +
     shadow(560, 470, 130) + shadow(230, 470, 120))
save('big-w3a-gurita', 500, b)

# BIG: nothing on the cord (no bottles) / open and dry, diaper folded below the stump
def baby_front(cx, cy, s):
    r = 54 * s; sk = '#f3cba5'; skd = '#e2ad83'; ty = cy + r * .8
    body = (path(f'M{cx-r*1.1} {ty+r*.4} Q{cx-r*1.8} {ty+r*.9} {cx-r*1.6} {ty+r*1.5}', sk, r * .42) +
            path(f'M{cx+r*1.1} {ty+r*.4} Q{cx+r*1.8} {ty+r*.9} {cx+r*1.6} {ty+r*1.5}', sk, r * .42) +
            rr(cx - r * 1.2, ty, r * 2.4, r * 2.6, r * 1.0, sk) + rr(cx + r * .3, ty + r * .2, r * .8, r * 2.2, r * .4, skd, op=.22) +
            path(f'M{cx} {ty+r*1.25} q{r*.25} -{r*.2} {r*.1} -{r*.55}', '#b98f6a', r * .2) + rr(cx - r * .18, ty + r * .6, r * .6, r * .2, r * .1, SKY) +
            diaper_fold(cx, ty + r * 1.75, r * 2.6))
    head = P.person('adek', cx, cy, s, 'senang', 'none')
    head = head[head.index('<ellipse'):]  # drop the shirt torso, keep the face
    return body + head
b = (floor(400, 500) + bottle(60, 190, 100, 190, BROWN, BROWND) + bottle(180, 230, 80, 150, CARD, SKYD, None) +
     rr(195, 320, 50, 30, 6, SKY, op=.7) + nope(150, 140, 36) + shadow(160, 470, 120) +
     shadow(600, 475, 150) + baby_front(600, 120, 1.25) +
     rr(700, 110, 180, 50, 25, SAGE) + text(790, 145, 'tali pusat', 28, '#fff') + line(720, 160, 625, 262, SAGE, 6) +
     path('M420 230 q30 -10 50 6', SKY, 8) + path('M420 270 q30 -10 56 6', SKY, 8, op=.7) + check(770, 330, 34))
save('big-w3a-tali-pusat', 500, b)

# BIG: baby walker (no) / play on the floor (yes)
b = (floor(380, 500) + shadow(200, 460, 140) + walker(200, 450, 1.1) + nope(200, 150, 34) +
     rug(620, 440, 240, 46) + shadow(620, 450, 80) + tunas('hore', 150, 175, 545, 290) +
     ball(790, 420, 30, SKY, CARD) + block(450, 400, 44, SUN, SUND, 10) + check(760, 260, 32))
save('big-w3a-lantai', 500, b)


# ================================================================== 3. w3e-mitos-2 (0-3 tahun)
# HERO: four "updated" items around Tunas, each with a refresh badge
b = (floor(330, 420) + shadow(440, 400, 90) + tunas('sayang', 170, 198, 355, 200) +
     pillow(140, 300, 170, SKY) + refresh(210, 250, 30) +
     banana(160, 110, 70, -10) + refresh(230, 80, 30) +
     jar(640, 60, 110, 150) + refresh(760, 70, 30) +
     clipper(640, 330, 1.0, -8) + refresh(800, 300, 30) +
     heart(440, 120, 26) + heart(520, 160, 16, BLUSH) + spark(360, 120, 14))
save('hero-w3a-mitos-2', 420, b)

# BIG: no pillow in the crib (empty, flat), tummy time while awake
back, front, mat = crib(60, 120, 340, 320)
b = (floor(400, 500) + back + front + check(230, 80, 34) + pillow(470, 150, 130, BLUSH) + nope(530, 110, 28) +
     rug(640, 455, 200, 40) + shadow(640, 462, 90) + tunas('hore', 190, 221, 545, 235) +
     rr(530, 170, 220, 48, 24, SAGE) + text(640, 204, 'tummy time', 28, '#fff'))
save('big-w3a-bantal', 500, b)

# BIG: banana and water wait until 6 months
b = (floor(380, 500) + banana(170, 220, 100, -12) + rr(80, 300, 80, 110, 14, SKY, op=.85) + rr(80, 300, 80, 24, 12, SKYD) + nope(260, 120, 32) +
     calendar(470, 150, 200, '6', 'bulan') + check(690, 150, 32) +
     shadow(780, 470, 60) + tunas('mikir', 130, 152, 715, 320))
save('big-w3a-pisang', 500, b)

# BIG: honey waits until the first birthday
b = (floor(380, 500) + shadow(200, 460, 110) + jar(130, 200, 150, 240) + nope(300, 190, 34) +
     shadow(580, 460, 140) + cake(580, 450, 240, '1') + check(760, 220, 32) +
     spark(440, 160, 16) + spark(420, 300, 12, TERRA))
save('big-w3a-madu', 500, b)

# BIG: short nails, trimmed while the baby sleeps
b = (floor(400, 500) + moon_window(620, 50, 180, 140) +
     hand(250, 300, 1.4) + clipper(360, 380, 1.0, -18) +
     rug(680, 450, 170, 36) + shadow(680, 456, 70) + tunas('ngantuk', 130, 152, 615, 300) + spark(470, 140, 16))
save('big-w3a-kuku', 500, b)

autocrop(NAMES)

if len(sys.argv) > 1:
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 440, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
