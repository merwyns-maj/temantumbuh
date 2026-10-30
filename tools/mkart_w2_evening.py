# Design v2 scenes for the w2 evening posts (2 to 8 Nov). Run: python tools/mkart_w2_evening.py
# Every name starts with "w2e-" so it never collides with the noon batch.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

BG = '#fbf4ea'      # slide surface, for cut-outs
GREY = '#c8c2b8'; GREYL = '#e2ddd5'; DARK = '#3b3f4a'; GRAPE = '#9cc49f'; GRAPEL = '#c9e2c6'
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
def path(d, col, w=8, fill='none', dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{ds}/>'
def check(cx, cy, r=30):
    return circ(cx, cy, r, SD) + path(f'M{cx-r*.45} {cy} L{cx-r*.12} {cy+r*.33} L{cx+r*.5} {cy-r*.33}', '#fff', r * .27)
def nope(cx, cy, r=30):
    k = r * .38
    return circ(cx, cy, r, TD) + path(f'M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}', '#fff', r * .27)
def bubble(x, y, w, h, f, tail='left'):
    tx = x + 50 if tail == 'left' else x + w - 90
    tip = tx - 20 if tail == 'left' else tx + 70
    return rr(x, y, w, h, h / 2 if h < 110 else 34, f) + f'<path d="M{tx} {y+h-4} L{tip} {y+h+34} L{tx+46} {y+h-4} Z" fill="{f}"/>'
def note(x, y, s=1, col=SD):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="40" rx="15" ry="11" fill="{col}" transform="rotate(-20 0 40)"/>'
            f'<rect x="10" y="-10" width="7" height="50" fill="{col}"/><path d="M13 -10 Q36 0 32 22" stroke="{col}" stroke-width="7" fill="none"/></g>')
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def stick(x, y, w, h, rot, f, fd):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{f}"/>'
            f'<rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" rx="{h*0.22}" fill="{fd}" opacity="0.5"/></g>')
def grape_half(cx, cy, rx, ry, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GRAPE}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.78}" ry="{ry*.7}" fill="{GRAPEL}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*.5}" ry="{ry*.12}" fill="{GRAPE}" opacity="0.7"/></g>')
def grape(cx, cy, r): return circ(cx, cy, r, GRAPE) + circ(cx - r * .35, cy - r * .35, r * .3, '#fff', .45) + line(cx, cy - r, cx + 4, cy - r - 12, SD, 5)
def coin(cx, cy, r): return circ(cx, cy, r, TERRA) + circ(cx, cy, r * .7, '#eb9a7c')
def jar(x, y, w, h, label='madu'):
    return (rr(x + w * .12, y, w * .76, h * .16, 12, BOXD) + rr(x, y + h * .14, w, h * .86, 34, SUN) +
            rr(x + w * .62, y + h * .2, w * .26, h * .74, 22, SUND, op=.55) + rr(x + w * .14, y + h * .42, w * .72, h * .3, 14, CARD) +
            text(x + w / 2, y + h * .63, label, w * .2, SUND) +
            f'<path d="M{x+w*.25} {y+h*.15} Q{x+w*.3} {y+h*.3} {x+w*.25} {y+h*.36}" stroke="{SUND}" stroke-width="12" fill="none" stroke-linecap="round"/>')
def phone(x, y, w, h, screen=SKY, rot=0, inner=''):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">' + rr(x, y, w, h, w * .16, INK) + rr(x + w * .07, y + h * .07, w * .86, h * .82, w * .1, screen) +
            inner + rr(x + w * .38, y + h * .925, w * .24, h * .03, 4, MUTED) + '</g>')
def tv(x, y, w, h, screen=DARK):
    return (line(x + w * .3, y + h, x + w * .2, y + h + 50, INK, 10) + line(x + w * .7, y + h, x + w * .8, y + h + 50, INK, 10) +
            rr(x, y, w, h, 22, INK) + rr(x + 16, y + 16, w - 32, h - 32, 12, screen))
def book(x, y, w, h, f, fd, rot=0):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">' + rr(x, y, w, h, 12, f) + rr(x, y, w * .16, h, 10, fd) +
            rr(x + w * .3, y + h * .2, w * .5, h * .14, 6, '#fff', op=.55) + '</g>')
def open_book(cx, top, w, h, left='', right='', col=CARD, edge=LINE):
    return (f'<path d="M{cx} {top+16} Q{cx-w*.25} {top-14} {cx-w/2} {top+6} L{cx-w/2} {top+h} Q{cx-w*.25} {top+h-20} {cx} {top+h+10} '
            f'Q{cx+w*.25} {top+h-20} {cx+w/2} {top+h} L{cx+w/2} {top+6} Q{cx+w*.25} {top-14} {cx} {top+16} Z" fill="{col}" stroke="{edge}" stroke-width="6" stroke-linejoin="round"/>' +
            line(cx, top + 18, cx, top + h + 6, edge, 5) + left + right)
def ball(cx, cy, r, f=TERRA, s=SUN):
    return (circ(cx, cy, r, f) + f'<path d="M{cx-r} {cy} Q{cx} {cy-r*.55} {cx+r} {cy}" stroke="{s}" stroke-width="{r*.22}" fill="none"/>' +
            circ(cx - r * .35, cy - r * .4, r * .18, '#fff', .45))
def block(x, y, s, f, fd, rot=0):
    return f'<g transform="rotate({rot} {x+s/2} {y+s/2})">' + rr(x, y, s, s, 10, f) + rr(x, y + s * .72, s, s * .28, 8, fd, op=.6) + circ(x + s / 2, y + s * .4, s * .16, '#fff', .45) + '</g>'
def carton(x, y, w, h, open_top=True):
    flaps = (f'<path d="M{x} {y} L{x-w*.18} {y-h*.22} L{x+w*.22} {y-h*.22} L{x+w*.3} {y} Z" fill="{BOXD}"/>'
             f'<path d="M{x+w} {y} L{x+w*1.18} {y-h*.22} L{x+w*.78} {y-h*.22} L{x+w*.7} {y} Z" fill="{BOXD}"/>') if open_top else ''
    return flaps + rr(x, y, w, h, 8, BOX) + rr(x + w * .62, y, w * .38, h, 8, BOXD, op=.45) + rr(x + w * .1, y + h * .16, w * .34, h * .12, 4, '#ecd2b0')
def spoon(x, y, L, rot, f=SAGE):
    return (f'<g transform="rotate({rot} {x} {y})">' + rr(x, y - 8, L, 16, 8, f) + f'<ellipse cx="{x+L+20}" cy="{y}" rx="30" ry="20" fill="{f}"/>' +
            f'<ellipse cx="{x+L+22}" cy="{y-3}" rx="18" ry="10" fill="#fff" opacity="0.35"/></g>')
def fork(x, y, L, rot, f=GREY):
    t = ''.join(rr(x + L + 4, y - 22 + i * 15, 50, 9, 4, f) for i in range(4))
    return f'<g transform="rotate({rot} {x} {y})">' + rr(x, y - 9, L, 18, 9, f) + rr(x + L - 4, y - 24, 16, 48, 8, f) + t + '</g>'
def cup(x, y, w, h, f=SAGE, water=True):
    b = f'<path d="M{x} {y} L{x+w} {y} L{x+w*.85} {y+h} Q{x+w/2} {y+h+10} {x+w*.15} {y+h} Z" fill="{f}"/>'
    if water:
        b += f'<ellipse cx="{x+w/2}" cy="{y+6}" rx="{w/2-8}" ry="9" fill="{SKY}"/>'
    return b + rr(x + w * .62, y + h * .15, w * .14, h * .6, 6, '#fff', op=.3)
def clock(cx, cy, r, wedge=True):
    b = circ(cx, cy, r + 14, INK) + circ(cx, cy, r, CARD)
    if wedge:
        b += f'<path d="M{cx} {cy} L{cx} {cy-r} A{r} {r} 0 0 1 {cx+r*0.866} {cy-r*0.5} Z" fill="{SUN}"/>'
    b += ''.join(circ(cx + (r - 18) * __import__("math").sin(i * 0.5236), cy - (r - 18) * __import__("math").cos(i * 0.5236), 6, LINE) for i in range(12))
    return b + line(cx, cy, cx, cy - r * .7, INK, 10) + line(cx, cy, cx + r * .45, cy - r * .26, INK, 10) + circ(cx, cy, 10, TD)
def steth(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})">' + path('M0 0 Q-10 90 50 110 Q110 120 120 40', INK, 12) + path('M120 40 L130 0 M120 40 L108 2', INK, 10) +
            path('M50 110 Q60 170 110 175', INK, 12) + circ(122, 178, 28, GREY) + circ(122, 178, 16, GREYL) + circ(0, 0, 8, MUTED) + circ(130, 0, 8, MUTED) + '</g>')
def cat(cx, cy, s, f=BOX, fd=BOXD):
    return (f'<path d="M{cx-s*.85} {cy-s*.3} L{cx-s*.7} {cy-s*1.15} L{cx-s*.2} {cy-s*.75} Z" fill="{f}"/>'
            f'<path d="M{cx+s*.85} {cy-s*.3} L{cx+s*.7} {cy-s*1.15} L{cx+s*.2} {cy-s*.75} Z" fill="{f}"/>' +
            f'<ellipse cx="{cx}" cy="{cy}" rx="{s}" ry="{s*.85}" fill="{f}"/>' + circ(cx - s * .38, cy - s * .1, s * .12, INK) + circ(cx + s * .38, cy - s * .1, s * .12, INK) +
            f'<path d="M{cx-s*.12} {cy+s*.15} L{cx+s*.12} {cy+s*.15} L{cx} {cy+s*.3} Z" fill="{TD}"/>' +
            line(cx - s * .55, cy + s * .25, cx - s * 1.2, cy + s * .15, fd, 4) + line(cx + s * .55, cy + s * .25, cx + s * 1.2, cy + s * .15, fd, 4))
def cat_body(cx, base, s):  # sitting cat
    return (f'<ellipse cx="{cx}" cy="{base-s*.8}" rx="{s*.9}" ry="{s*.85}" fill="{BOX}"/>' +
            path(f'M{cx+s*.8} {base-s*.2} Q{cx+s*1.6} {base-s*.3} {cx+s*1.4} {base-s*1.2}', BOX, s * .25) + cat(cx, base - s * 1.75, s * .75))
def lamp(x, base, h):
    return (rr(x - 50, base - 16, 100, 16, 8, INK) + rr(x - 6, base - h, 12, h, 6, INK) +
            f'<path d="M{x-70} {base-h+70} L{x-40} {base-h-20} L{x+40} {base-h-20} L{x+70} {base-h+70} Z" fill="{SUN}"/>' +
            f'<path d="M{x+10} {base-h-20} L{x+40} {base-h-20} L{x+70} {base-h+70} L{x+35} {base-h+70} Z" fill="{SUND}" opacity="0.5"/>')
def hand_point(x, y, s=1, rot=0):  # flat pointing-hand icon (index finger), no person attached
    sk = '#f2b9a3'
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">' + rr(-40, -30, 70, 66, 24, sk) + rr(10, -28, 70, 22, 11, sk) +
            rr(-30, 30, 50, 16, 8, '#e6a189') + rr(-46, -8, 20, 36, 10, '#e6a189') + '</g>')
def ear(cx, cy, s):
    sk = '#f2b9a3'
    return (f'<path d="M{cx} {cy+s} Q{cx-s*.9} {cy+s} {cx-s*.8} {cy} Q{cx-s*.8} {cy-s} {cx} {cy-s} Q{cx+s*.8} {cy-s} {cx+s*.7} {cy} Q{cx+s*.6} {cy+s*.4} {cx+s*.25} {cy+s*.55} Q{cx} {cy+s*.75} {cx} {cy+s} Z" fill="{sk}"/>' +
            path(f'M{cx-s*.35} {cy+s*.1} Q{cx-s*.4} {cy-s*.5} {cx} {cy-s*.5} Q{cx+s*.35} {cy-s*.5} {cx+s*.3} {cy-s*.05}', '#e6a189', s * .14))
def waves(cx, cy, n=3, col=SD, gap=26, dirn=1):
    return ''.join(path(f'M{cx+dirn*(i*gap)} {cy-24-i*14} Q{cx+dirn*(i*gap+18)} {cy} {cx+dirn*(i*gap)} {cy+24+i*14}', col, 8) for i in range(n))
def table(x, y, w, h=40, legs=90):
    return (line(x + 40, y + h, x + 30, y + h + legs, BOXD, 14) + line(x + w - 40, y + h, x + w - 30, y + h + legs, BOXD, 14) +
            rr(x, y, w, h, 14, BOX) + rr(x, y + h * .6, w, h * .4, 8, BOXD, op=.6))
def bucket(x, y, w, h):
    return (path(f'M{x+10} {y} Q{x+w/2} {y-h*.7} {x+w-10} {y}', GREY, 8) +
            f'<path d="M{x} {y} L{x+w} {y} L{x+w*.86} {y+h} L{x+w*.14} {y+h} Z" fill="{SKY}"/>' +
            f'<path d="M{x+w*.6} {y} L{x+w} {y} L{x+w*.86} {y+h} L{x+w*.55} {y+h} Z" fill="{SKYD}" opacity="0.5"/>' + rr(x - 6, y - 8, w + 12, 18, 9, SKYD))
def steam(x, y): return ''.join(path(f'M{x+i*26} {y} q-14 -20 0 -40 q14 -20 0 -40', LINE, 7) for i in range(2))
def label(x, y, s, size=30, col=MUTED): return text(x, y, s, size, col)


# ================================================================== 1. w2e-d21 kirim pengasuh (mpasi)
b = (floor(320, 420) + shadow(190, 395, 150) + chair(110, 150) + tunas('santai', 150, 175, 110, 10) +
     bowl(40, 104, 80, TERRA, TD) +
     shadow(470, 372, 140, 16) + f'<ellipse cx="470" cy="352" rx="150" ry="34" fill="{CARD}" stroke="{LINE}" stroke-width="6"/>' +
     grape_half(400, 346, 28, 16, -10) + grape_half(450, 352, 28, 16, 8) + stick(500, 330, 100, 22, -4, TERRA, TD) + stick(505, 356, 95, 22, 4, TERRA, TD) +
     check(560, 270, 28) +
     shadow(700, 382, 70, 12) + jar(640, 180, 120, 200) + rr(735, 150, 104, 52, 26, SAGE) + text(787, 186, '1 thn+', 28, '#fff'))
save('hero-w2e-pengasuh', 420, b)

b = (floor(400, 500) + shadow(210, 460, 130) + jar(110, 150, 200, 300) +
     rr(370, 90, 220, 230, 22, CARD, LINE, 6) + rr(370, 90, 220, 56, 22, TERRA) + rr(370, 120, 220, 26, 0, TERRA) +
     circ(420, 90, 9, INK) + circ(540, 90, 9, INK) + text(480, 240, '12', 96, INK) + text(480, 292, 'bulan', 36, MUTED) +
     shadow(700, 470, 110) + tunas('mikir', 160, 187, 620, 280) + nope(300, 150, 30))
save('big-w2e-madu', 500, b)

b = (floor(390, 500) + rr(40, 60, 300, 170, 30, 'none', LINE, 6) + f'<rect x="40" y="60" width="300" height="170" rx="30" fill="none" stroke="{MUTED}" stroke-width="5" stroke-dasharray="4 14"/>' +
     grape(110, 150, 38) + coin(200, 150, 30) + coin(255, 135, 30) + coin(280, 180, 30) + nope(330, 70, 28) +
     shadow(350, 455, 300) + rr(60, 330, 600, 100, 30, BOX) + rr(60, 395, 600, 35, 18, BOXD, op=.6) + circ(615, 360, 14, BG) +
     grape_half(140, 366, 40, 22, -8) + grape_half(220, 372, 40, 22, 6) + grape_half(175, 392, 36, 18, 2) +
     stick(320, 340, 230, 30, -3, TERRA, TD) + stick(325, 378, 225, 30, 3, TERRA, TD) + check(600, 300, 30) +
     path('M360 150 Q470 150 480 280', SD, 10) + path('M458 262 L480 286 L500 260', SD, 10) + text(580, 170, 'belah', 44, SD) +
     tunas('riset', 150, 175, 700, 215))
save('big-w2e-potong-panjang', 500, b)

b = (floor(390, 500) + shadow(250, 455, 140) + chair(170, 190) + tunas('hore', 140, 165, 170, 52) + bowl(100, 150, 80, TERRA, TD) +
     check(110, 90, 30) +
     path('M420 440 C480 380 540 470 600 420 C640 386 670 430 690 420', MUTED, 7, dash='3 18') +
     shadow(770, 462, 70) + f'<g opacity="0.55">' + tunas('kaget', 130, 152, 705, 300) + '</g>' + text(620, 250, 'sambil lari', 40, MUTED) + nope(830, 290, 28))
save('big-w2e-duduk-makan', 500, b)

b = (floor(400, 500) + shadow(300, 465, 250) + rr(60, 320, 480, 120, 26, CARD, LINE, 6) + f'<ellipse cx="300" cy="350" rx="170" ry="26" fill="{GREYL}"/>' +
     path('M150 330 L150 170 Q150 120 200 120 L290 120 Q320 120 320 150 L320 175', GREY, 26) + rr(130, 300, 40, 30, 8, GREY) +
     rr(300, 172, 40, 18, 8, GREY) + rr(306, 190, 28, 130, 14, SKY, op=.85) +
     circ(400, 210, 22, '#fff') + f'<circle cx="400" cy="210" r="22" fill="none" stroke="{SKY}" stroke-width="5"/>' +
     circ(440, 160, 14, '#fff') + f'<circle cx="440" cy="160" r="14" fill="none" stroke="{SKY}" stroke-width="4"/>' +
     circ(380, 140, 10, '#fff') + f'<circle cx="380" cy="140" r="10" fill="none" stroke="{SKY}" stroke-width="4"/>' +
     rr(420, 290, 90, 40, 16, BLUSH) + circ(470, 288, 12, '#fff') + circ(450, 282, 8, '#fff') +
     shadow(700, 470, 110) + tunas('hore', 150, 175, 620, 285) + bowl(830, 430, 70, TERRA, TD) + spoon(760, 415, 30, -20, SAGE) + check(820, 260, 28))
save('big-w2e-cuci-tangan', 500, b)

b = (floor(390, 500) + shadow(200, 455, 130) + chair(120, 190) + tunas('santai', 140, 165, 120, 52) + bowl(50, 150, 80, TERRA, TD) +
     tv(430, 70, 260, 170) + text(560, 175, 'z z', 54, '#8a8f9c') +
     table(540, 330, 280, 34, 80) + phone(710, 190, 90, 150, DARK) + text(835, 220, 'zz', 36, MUTED) + check(430, 340, 30))
save('big-w2e-hp-istirahat', 500, b)

# ================================================================== 2. w2e-d22 jawaban sopan (pintar)
grid = ''.join(line(110, 110 + i * 60, 520, 110 + i * 60, LINE, 3) for i in range(5)) + ''.join(line(110 + i * 82, 100, 110 + i * 82, 360, LINE, 3) for i in range(6))
band = f'<path d="M110 300 C230 250 380 170 520 130 L520 200 C380 240 230 310 110 350 Z" fill="{SAGE}" opacity="0.35"/>'
dots = [(130, 318), (205, 292), (285, 260), (365, 228), (445, 196), (510, 170)]
b = (rr(60, 40, 510, 380, 26, CARD, LINE, 6) + rr(60, 40, 510, 50, 26, BLUSH) + rr(60, 70, 510, 20, 0, BLUSH) + text(140, 78, 'KMS', 30, TD) +
     grid + band + path('M' + ' L'.join(f'{x} {y}' for x, y in dots), SD, 8) + ''.join(circ(x, y, 12, SD) for x, y in dots) +
     line(110, 100, 110, 365, MUTED, 5) + line(105, 365, 525, 365, MUTED, 5) +
     path('M470 120 L520 150', SD, 0) + check(540, 120, 28) +
     shadow(720, 470, 110) + tunas('riset', 170, 198, 630, 260))
save('big-w2e-kms-naik', 500, b)

b = (floor(400, 500) + shadow(300, 465, 200) + rr(140, 370, 320, 60, 18, CARD, LINE, 6) + rr(250, 388, 100, 26, 8, DARK) +
     rr(265, 394, 16, 14, 3, SAGE) + rr(290, 394, 16, 14, 3, SAGE) + rr(315, 394, 16, 14, 3, SAGE) +
     tunas('hore', 150, 175, 225, 192) +
     f'<path d="M110 300 Q300 400 490 300 L470 350 Q300 410 130 350 Z" fill="{BLUSH}"/>' + f'<path d="M110 300 Q300 400 490 300" stroke="{TERRA}" stroke-width="8" fill="none" opacity="0.5"/>' +
     shadow(690, 455, 110) + rr(600, 170, 180, 260, 18, BLUSH) + rr(600, 170, 30, 260, 12, '#e8a993') + rr(650, 220, 100, 50, 10, CARD) + text(700, 256, 'KIA', 34, TD) +
     heart(700, 340, 26, TERRA) + check(800, 160, 28))
save('big-w2e-timbang', 500, b)

cal = rr(60, 70, 330, 290, 24, CARD, LINE, 6) + rr(60, 70, 330, 60, 24, SAGE) + rr(60, 100, 330, 30, 0, SAGE) + circ(130, 70, 9, INK) + circ(320, 70, 9, INK)
for i in range(3):
    for j in range(2):
        cx, cy = 120 + i * 105, 185 + j * 100
        cal += rr(cx - 38, cy - 34, 76, 68, 12, '#f4ece0') + (check(cx, cy, 24) if (i + j * 3) < 5 else circ(cx, cy, 10, LINE))
b = (floor(400, 500) + cal + shadow(520, 470, 100) + tunas('halo', 160, 187, 440, 280) + shadow(730, 470, 100) + steth(640, 250, 1.15))
save('big-w2e-kontrol', 500, b)

b = (floor(390, 500) + ''.join(line(270, 270 + i * 40, 200 + i * 12, 270 + i * 40, MUTED, 8) for i in range(4)) +
     shadow(370, 455, 110) + tunas('hore', 170, 198, 280, 240) +
     shadow(600, 455, 50) + ball(600, 400, 48) + path('M560 450 q-20 0 -40 0', LINE, 0) +
     ''.join(path(f'M{540+i*30} 330 q10 -14 20 0', MUTED, 5) for i in range(0)) +
     block(700, 380, 66, SKY, SKYD, 12) + block(770, 400, 54, SUN, SUND, -10) + block(720, 330, 50, SAGE, SD, 25) +
     text(460, 150, 'wuush', 44, SD, rot=-6) + circ(440, 230, 9, SKY) + circ(458, 210, 7, SKY))
save('big-w2e-aktif', 500, b)

def teacup(x, y):
    return (f'<path d="M{x} {y} L{x+110} {y} Q{x+105} {y+80} {x+55} {y+82} Q{x+5} {y+80} {x} {y} Z" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>' +
            f'<ellipse cx="{x+55}" cy="{y+4}" rx="50" ry="10" fill="{TD}"/>' + path(f'M{x+108} {y+18} q34 6 4 40', LINE, 10) +
            f'<ellipse cx="{x+55}" cy="{y+86}" rx="78" ry="12" fill="{LINE}"/>')
b = (tunas('sayang', 170, 198, 330, 132) + table(40, 330, 800, 46, 100) +
     teacup(130, 240) + steam(170, 225) + teacup(620, 240) + steam(660, 225) +
     f'<ellipse cx="555" cy="322" rx="52" ry="12" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>' + circ(535, 308, 17, SUN) + circ(565, 304, 17, SUND) + circ(580, 314, 14, SUN) +
     heart(560, 120, 26, TERRA) + heart(300, 150, 18, BLUSH))
save('big-w2e-teh', 500, b)

# ================================================================== 3. w2e-d27 buku per usia (pintar)
def stripes_card(x, y, w, h, rot, kind):
    inner = ''
    if kind == 'stripe':
        inner = ''.join(rr(x + 16 + i * (w - 32) / 5, y + 16, (w - 32) / 10, h - 32, 2, INK) for i in range(5))
    elif kind == 'check':
        s = (w - 32) / 4
        inner = ''.join(rr(x + 16 + i * s, y + 16 + j * s, s, s, 0, INK) for i in range(4) for j in range(int((h - 32) / s)) if (i + j) % 2 == 0)
    else:
        cx, cy = x + w / 2, y + h / 2
        inner = circ(cx, cy, w * .4, INK) + circ(cx, cy, w * .3, '#fff') + circ(cx, cy, w * .2, INK) + circ(cx, cy, w * .1, '#fff')
    return f'<g transform="rotate({rot} {x+w/2} {y+h})">' + rr(x, y, w, h, 14, '#fff', LINE, 5) + inner + '</g>'
def bite(id, shape, pts):  # tooth marks cut with slide-colour circles (cairosvg clips masked groups)
    return shape + ''.join(circ(x, y, r, BG) for x, y, r in pts)
def cloth_book(x, y, w, h):
    edge = ' '.join(f'Q{x+w+14} {y+h*(i+.5)/6} {x+w} {y+h*(i+1)/6}' for i in range(6))
    return (f'<path d="M{x} {y} L{x+w} {y} {edge} L{x} {y+h} Z" fill="{BLUSH}"/>' + rr(x, y, 26, h, 10, '#e8a993') +
            ''.join(circ(x + 60 + (i % 3) * 40, y + 50 + (i // 3) * 46, 10, SUN) for i in range(6)) +
            rr(x + w - 4, y + 40, 40, 22, 8, SAGE) + rr(x + w - 4, y + 90, 34, 22, 8, SKY) + rr(x + w - 4, y + 140, 40, 22, 8, SUN))

b = (floor(320, 420) + shadow(190, 380, 140) + book(70, 280, 240, 60, SKY, SKYD) + book(90, 225, 210, 56, SAGE, SD) + book(80, 172, 230, 54, TERRA, TD) +
     stripes_card(130, 40, 120, 130, -6, 'bull') +
     shadow(440, 395, 110) + tunas('hore', 160, 187, 360, 150) +
     bite('b1', book(470, 230, 150, 120, SUN, SUND, 8), [(630, 246, 22), (612, 230, 18), (636, 276, 18)]) + text(660, 200, 'nyam', 40, TD, rot=-8) +
     shadow(740, 395, 90) + cloth_book(670, 220, 140, 160))
save('hero-w2e-buku', 420, b)

b = (floor(400, 500) + shadow(330, 465, 260) + stripes_card(80, 160, 150, 230, -4, 'stripe') + stripes_card(260, 150, 150, 240, 2, 'check') + stripes_card(440, 160, 150, 230, 6, 'bull') +
     shadow(730, 470, 100) + tunas('halo', 160, 187, 650, 280) + bubble(660, 120, 150, 100, BLUSH, 'left') + note(712, 128, .9, TD))
save('big-w2e-buku-kontras', 500, b)

b = (floor(400, 500) + shadow(220, 465, 170) + cloth_book(80, 170, 240, 270) +
     shadow(500, 465, 120) + bite('b2', book(390, 190, 210, 250, SKY, SKYD, 4), [(604, 196, 28), (582, 184, 22), (612, 232, 22)]) +
     text(560, 150, 'nyam', 44, TD, rot=-8) + shadow(740, 470, 90) + tunas('hore', 150, 175, 665, 290))
save('big-w2e-buku-kain', 500, b)

left = ball(250, 230, 60) + rr(190, 320, 120, 14, 7, LINE)
right = (rr(470, 140, 220, 190, 16, '#f4ece0') + cat(580, 250, 60) +
         f'<path d="M470 140 L690 140 L650 60 L430 80 Z" fill="{SUN}"/>' + f'<path d="M470 140 L690 140 L686 150 L472 152 Z" fill="{SUND}" opacity="0.6"/>')
b = (floor(410, 500) + shadow(420, 470, 340) + open_book(420, 110, 600, 300, left, right) + shadow(790, 470, 70) + tunas('kaget', 130, 152, 745, 270))
save('big-w2e-buku-flap', 500, b)

left = circ(200, 190, 40, SUN) + f'<path d="M150 330 L150 260 L210 220 L270 260 L270 330 Z" fill="{TERRA}"/>' + rr(195, 285, 30, 45, 6, TD)
right = ''.join(rr(400, 160 + i * 40, 220 - (i % 2) * 60, 16, 8, LINE) for i in range(4)) + circ(530, 340, 0, LINE)
loop = (f'<path d="M820 150 A70 70 0 1 1 750 80" stroke="{SD}" stroke-width="12" fill="none" stroke-linecap="round"/>' +
        path('M736 62 L752 80 L736 98', SD, 12))
b = (floor(400, 500) + shadow(360, 465, 290) + open_book(360, 120, 520, 260, left, right) + loop + text(750, 165, 'lagi', 44, SD) +
     shadow(730, 475, 90) + tunas('sayang', 140, 163, 650, 300))
save('big-w2e-buku-cerita', 500, b)

right = ball(520, 250, 60, SKY, SKYD)
chips = (rr(60, 30, 200, 64, 32, SAGE) + text(160, 74, 'tunjuk', 36, '#fff') + rr(290, 30, 190, 64, 32, SUN) + text(385, 74, 'sebut', 36, INK) +
         rr(510, 30, 210, 64, 32, BLUSH) + text(615, 74, 'tunggu', 36, TD))
b = (floor(410, 500) + chips + shadow(380, 470, 300) + open_book(380, 160, 520, 240, rr(200, 250, 120, 14, 7, LINE) + rr(200, 290, 90, 14, 7, LINE), right) +
     bubble(560, 130, 150, 80, '#e3eee6', 'left') + text(635, 186, 'bola', 40, SD) +
     hand_point(470, 330, 1.0, -40) + shadow(760, 470, 90) + tunas('riset', 150, 175, 690, 280))
save('big-w2e-buku-tunjuk', 500, b)

# ================================================================== 4. w2e-d29 belum ngomong (pintar)
b = (floor(400, 500) + shadow(120, 460, 70) + lamp(120, 450, 300) + shadow(360, 460, 90) + cat_body(360, 450, 70) +
     path('M640 300 Q520 220 450 250', MUTED, 6, dash='3 16') + path('M470 228 L446 252 L476 266', MUTED, 6) +
     shadow(720, 470, 100) + tunas('halo', 160, 187, 640, 285) + circ(760, 150, 62, '#e3eee6') + hand_point(760, 150, 0.8, 200))
save('big-w2e-nunjuk', 500, b)

b = (floor(400, 500) + bubble(40, 60, 290, 110, '#efe6da', 'right') + text(185, 132, 'ba-ba-ba', 46, '#b8ab9c') +
     bubble(420, 50, 220, 120, '#e3eee6', 'left') + text(530, 132, 'mam', 64, SD) +
     path('M640 120 Q720 120 740 230', SD, 7, dash='3 16') + path('M722 214 L742 236 L758 210', SD, 7) +
     shadow(760, 460, 90) + bowl(760, 330, 150, TERRA, TD) + spoon(690, 300, 40, -30, SAGE) + check(600, 50, 26) +
     shadow(380, 470, 110) + tunas('hore', 170, 198, 300, 270))
save('big-w2e-satu-kata', 500, b)

def word_block(x, y, w, s, f, ink):
    return rr(x, y, w, 100, 18, f) + rr(x, y + 72, w, 28, 12, ink, op=.25) + text(x + w / 2, y + 64, s, 46, ink)
b = (floor(400, 500) + word_block(60, 60, 200, 'bola', SKY, '#2f5677') + text(300, 128, '+', 64, MUTED) + word_block(340, 60, 230, 'jatuh', SUN, '#7a5a12') +
     table(80, 260, 260, 30, 110) + path('M330 250 Q420 230 450 360', MUTED, 6, dash='3 16') + shadow(470, 460, 50) + ball(470, 410, 42) +
     text(560, 380, 'duk', 40, TD) + shadow(740, 470, 100) + tunas('kaget', 160, 187, 660, 280))
save('big-w2e-dua-kata', 500, b)

clinic = (rr(60, 110, 300, 330, 20, CARD, LINE, 6) + rr(60, 110, 300, 70, 20, SAGE) + rr(60, 150, 300, 30, 0, SAGE) +
          rr(195, 120, 30, 50, 6, '#fff') + rr(185, 130, 50, 30, 6, '#fff') + rr(150, 250, 120, 190, 10, '#e3eee6') + circ(250, 350, 9, SD))
b = (floor(430, 500) + clinic + path('M420 400 L380 400', MUTED, 0) +
     ''.join(circ(390 + i * 34, 455, 7, MUTED) for i in range(4)) + shadow(600, 480, 100) + tunas('halo', 160, 187, 520, 290) +
     circ(760, 170, 80, '#e3eee6') + ear(735, 170, 50) + waves(790, 170, 3, SD, 22, 1))
save('big-w2e-ke-dokter', 500, b)

b = (floor(400, 500) + bubble(60, 60, 200, 100, '#efe6da', 'right') + text(160, 125, 'ba?', 50, MUTED) +
     bubble(540, 40, 300, 110, '#e3eee6', 'right') + text(690, 110, 'iya, bola', 46, SD) +
     note(300, 150, 1.0, SUND) + note(470, 190, .8, TERRA) +
     shadow(400, 470, 110) + tunas('hore', 170, 198, 310, 270) +
     shadow(680, 470, 140) + open_book(680, 330, 260, 110, '', '', CARD, LINE) + ball(620, 380, 0) + ball(740, 385, 26, SKY, SKYD))
save('big-w2e-ngobrol', 500, b)

# ================================================================== 5. w2e-d23 alat mpasi (mpasi)
def blender(x, y, op=1):
    return (f'<g opacity="{op}">' + rr(x + 20, y, 120, 26, 10, INK) + f'<path d="M{x+10} {y+26} L{x+150} {y+26} L{x+130} {y+200} L{x+30} {y+200} Z" fill="{SKY}" opacity="0.8"/>' +
            path(f'M{x+150} {y+60} L{x+185} {y+60} L{x+180} {y+160} L{x+140} {y+160}', SKYD, 12) +
            rr(x + 10, y + 200, 140, 90, 18, GREY) + circ(x + 80, y + 245, 18, DARK) + '</g>')
mash = lambda cx, cy, w: f'<path d="M{cx-w*.42} {cy+4} Q{cx-w*.3} {cy-w*.22} {cx} {cy-w*.25} Q{cx+w*.3} {cy-w*.22} {cx+w*.42} {cy+4} Z" fill="{SUN}"/>'
b = (floor(320, 420) + shadow(145, 385, 90) + blender(60, 70, .5) + rr(215, 150, 70, 44, 10, CARD, LINE, 4) + text(250, 182, 'Rp', 26, MUTED) + line(200, 120, 220, 152, LINE, 4) +
     nope(230, 70, 28) +
     shadow(400, 395, 90) + tunas('santai', 150, 175, 325, 150) +
     shadow(660, 395, 140) + mash(660, 300, 220) + bowl(660, 300, 230, TERRA, TD) + fork(640, 250, 120, -40) + check(800, 210, 30))
save('hero-w2e-alat', 420, b)

b = (floor(420, 500) + shadow(250, 480, 140) + chair(170, 210) + rr(130, 380, 170, 16, 8, BOXD) + tunas('hore', 140, 165, 170, 72) +
     path('M180 212 Q240 226 300 212', SKYD, 12) + rr(226, 206, 30, 24, 6, SUN) + rr(234, 212, 14, 12, 3, '#fff') +
     bowl(100, 170, 80, TERRA, TD) + check(110, 110, 28) +
     table(560, 300, 270, 34, 110) + path('M380 340 L540 340', MUTED, 6, dash='3 14') + path('M398 324 L378 340 L398 356 M522 324 L542 340 L522 356', MUTED, 6) +
     text(460, 310, 'jauh', 38, MUTED))
save('big-w2e-kursi-tali', 500, b)

bib = (f'<path d="M560 150 Q560 110 600 110 Q630 110 640 150 Q650 175 680 175 Q710 175 720 150 Q730 110 760 110 Q800 110 800 150 L800 370 Q800 410 760 410 L600 410 Q560 410 560 370 Z" fill="{SKY}"/>' +
       rr(600, 320, 160, 70, 18, SKYD) + circ(620, 230, 10, '#fff', .5) + circ(700, 260, 10, '#fff', .5) + circ(760, 220, 10, '#fff', .5))
b = (floor(400, 500) + shadow(220, 450, 160) + rr(150, 400, 140, 26, 10, SAGE, op=.8) + bowl(220, 330, 220, TERRA, TD) +
     spoon(80, 230, 160, -8, SAGE) + spoon(110, 160, 140, -14, SUN) + rr(360, 120, 92, 64, 32, SD) + text(406, 166, '2x', 36, '#fff') +
     shadow(680, 450, 140) + bib + shadow(470, 470, 80) + tunas('hore', 130, 152, 405, 300))
save('big-w2e-sendok-mangkuk', 500, b)

def tex_bowl(cx, kind, cy=300, w=180):
    b = bowl(cx, cy, w, SKY, SKYD)
    if kind == 0:
        b = f'<ellipse cx="{cx}" cy="{cy}" rx="{w*.44}" ry="13" fill="{SUN}"/>' + b
    if kind == 1:
        b = mash(cx, cy + 2, w * .95) + bits([(cx - 34, cy - 18, 9, SUND), (cx + 12, cy - 24, 10, SUND), (cx + 36, cy - 10, 8, SUND)]) + b
    if kind == 2:
        b = mash(cx, cy + 2, w * .95) + bits([(cx - 40, cy - 16, 11, TERRA), (cx, cy - 26, 12, SAGE), (cx + 36, cy - 12, 11, TERRA), (cx - 12, cy - 6, 10, SAGE)]) + b
    if kind == 3:
        b = (f'<ellipse cx="{cx-20}" cy="{cy-8}" rx="48" ry="22" fill="#fff"/>' + stick(cx + 6, cy - 32, 60, 24, -10, TERRA, TD) + circ(cx + 40, cy - 6, 16, SAGE)) + b
    return b
def strainer(cx, cy, r):
    return (circ(cx, cy, r, GREYL, .9) + ''.join(line(cx - r * .7 + i * r * .28, cy - r * .75, cx - r * .7 + i * r * .28, cy + r * .75, GREY, 3) for i in range(6)) +
            ''.join(line(cx - r * .8, cy - r * .6 + i * r * .3, cx + r * .8, cy - r * .6 + i * r * .3, GREY, 3) for i in range(5)) +
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREY}" stroke-width="10"/>')
def knife(x, y, rot):
    return (f'<g transform="rotate({rot} {x} {y})">' + rr(x, y - 10, 70, 20, 10, INK) +
            f'<path d="M{x+70} {y-12} L{x+190} {y-12} Q{x+200} {y+4} {x+176} {y+14} L{x+70} {y+12} Z" fill="{GREYL}" stroke="{GREY}" stroke-width="4"/></g>')
b = (floor(330, 470) + shadow(440, 400, 400) +
     f'<g transform="rotate(-20 110 210)">' + strainer(110, 210, 62) + rr(168, 202, 120, 16, 8, GREY) + '</g>' + tex_bowl(110, 0) +
     fork(300, 140, 120, 62) + tex_bowl(330, 1) +
     knife(470, 160, 30) + tex_bowl(550, 2) +
     spoon(720, 180, 70, 40, SAGE) + tex_bowl(770, 3) +
     ''.join(path(f'M{x} 330 L{x+22} 348 L{x} 366', MUTED, 8) for x in (210, 430, 650)) +
     label(110, 440, 'saring', 34) + label(330, 440, 'kasar', 34) + label(550, 440, 'cincang', 34) + label(770, 440, 'keluarga', 34) +
     check(250, 70, 30))
save('big-w2e-garpu-saring', 500, b)

b = (floor(400, 500) + shadow(360, 465, 120) + tunas('hore', 180, 210, 260, 250) +
     f'<g transform="rotate(-25 540 300)">' + cup(500, 250, 100, 120, SAGE) + '</g>' +
     circ(470, 330, 9, SKY) + circ(455, 360, 7, SKY) + circ(480, 380, 6, SKY) + f'<ellipse cx="500" cy="455" rx="80" ry="14" fill="{SKY}" opacity="0.6"/>' +
     shadow(710, 465, 60) + cup(660, 330, 100, 120, SUN, True) + check(780, 300, 28) + text(150, 200, 'tumpah', 40, SKYD, rot=-8) + text(150, 245, 'nggak apa', 34, MUTED, rot=-8))
save('big-w2e-gelas-kecil', 500, b)

shelf = rr(60, 230, 620, 26, 10, BOX) + rr(60, 246, 620, 10, 5, BOXD) + line(120, 256, 140, 300, BOXD, 12) + line(620, 256, 600, 300, BOXD, 12)
gadgets = (rr(90, 110, 140, 120, 22, '#d8d2c8') + rr(110, 90, 100, 26, 12, GREY) + circ(160, 180, 20, '#fff', .7) +
           rr(270, 130, 130, 100, 30, BLUSH) + rr(290, 116, 90, 18, 9, '#e8a993') + rr(310, 170, 50, 14, 7, '#fff', op=.6) +
           f'<path d="M470 230 L500 160 L530 230 Z" fill="{SUN}"/>' + heart(590, 200, 30, SKY) + rr(440, 222, 200, 8, 4, SUND, op=.4))
web = path('M60 40 L170 40 M60 40 L60 150 M60 40 L150 130 M60 80 Q100 76 110 98 M60 110 Q118 104 130 112 M95 40 Q100 70 120 85', MUTED, 3)
dust = ''.join(circ(x, y, r, GREY, .5) for x, y, r in [(180, 100, 8), (330, 112, 6), (520, 150, 7), (610, 160, 9), (140, 96, 5)])
b = (floor(400, 500) + shelf + gadgets + web + dust + rr(690, 160, 90, 50, 12, CARD, LINE, 4) + text(735, 196, 'Rp', 30, MUTED) + line(680, 140, 700, 162, LINE, 4) +
     shadow(420, 470, 100) + tunas('ngantuk', 160, 187, 340, 290) + text(640, 380, 'skip dulu', 40, SD))
save('big-w2e-pajangan', 500, b)

# ================================================================== 6. w2e-d24 mainan banyak cara (main)
def wheel(cx, cy, r): return circ(cx, cy, r, INK) + circ(cx, cy, r * .45, GREY)
b = (floor(380, 500) +
     shadow(150, 440, 110) + tunas('kaget', 110, 128, 95, 230) + carton(60, 300, 180, 130, True) +
     shadow(440, 440, 120) + tunas('hore', 110, 128, 385, 200) + carton(330, 280, 220, 120, False) + wheel(380, 410, 32) + wheel(500, 410, 32) +
     circ(560, 300, 14, SUN) +
     shadow(730, 440, 100) + rr(640, 300, 180, 130, 10, BOX) + rr(640, 300, 180, 26, 10, BOXD) + rr(752, 300, 68, 130, 10, BOXD, op=.4) +
     stick(640, 210, 130, 18, 30, BOXD, INK) + stick(700, 210, 130, 18, -30, BOXD, INK) + text(730, 175, 'dung', 40, TD) +
     label(150, 485, 'masuk-keluar') + label(440, 485, 'mobil') + label(730, 485, 'drum'))
save('big-w2e-kardus', 500, b)

b = (floor(380, 500) +
     shadow(140, 440, 90) + block(90, 340, 90, SKY, SKYD) + block(95, 255, 85, SUN, SUND) + block(100, 175, 80, SAGE, SD) + block(105, 100, 75, TERRA, TD) +
     shadow(420, 440, 110) + block(330, 350, 80, SKY, SKYD) + block(380, 280, 70, SUN, SUND, 30) + block(470, 220, 66, SAGE, SD, 60) + block(520, 330, 70, TERRA, TD, -20) +
     text(470, 180, 'brak', 44, TD, rot=-10) + tunas('hore', 100, 117, 300, 140) +
     shadow(730, 440, 120) + ''.join(rr(620 + i * 58, 400, 54, 24, 6, [SKY, SUN, SAGE, TERRA][i % 4]) for i in range(4)) +
     rr(650, 350, 90, 40, 14, TERRA) + rr(670, 330, 46, 26, 10, '#f4a88b') + wheel(670, 392, 12) + wheel(722, 392, 12) +
     label(140, 485, 'susun') + label(430, 485, 'robohin') + label(730, 485, 'jalan'))
save('big-w2e-balok', 500, b)

b = (floor(380, 500) +
     shadow(110, 445, 80) + tunas('hore', 130, 152, 45, 280) + shadow(270, 445, 40) + ball(270, 405, 38) +
     path('M200 350 L380 350', SD, 7, dash='3 16') + path('M362 334 L384 350 L362 366', SD, 7) +
     path('M380 300 L200 300', SAGE, 7, dash='3 16') + path('M218 284 L196 300 L218 316', SAGE, 7) +
     shadow(560, 445, 50) + tunas('kaget', 120, 140, 500, 290) + path('M610 300 Q690 120 760 310', MUTED, 6, dash='3 16') + ball(700, 200, 30, SUN, TERRA) +
     shadow(770, 445, 70) + bucket(710, 330, 130, 110) +
     label(250, 485, 'gelinding') + label(660, 485, 'lempar ke ember'))
save('big-w2e-bola', 500, b)

cloth = lambda d, f=SAGE: f'<path d="{d}" fill="{f}"/>'
doll = circ(0, 0, 0, INK)
b = (floor(380, 500) +
     shadow(140, 445, 100) + tunas('hore', 160, 187, 60, 255) +
     f'<g transform="rotate(-14 140 230)">' + cloth('M40 222 Q140 190 240 222 L246 272 Q218 256 204 280 Q172 256 150 278 Q120 256 96 278 Q74 258 34 272 Z', BLUSH) + '</g>' +
     path('M30 250 q-20 -30 0 -60 M258 210 q24 -24 10 -56', MUTED, 6) + text(290, 330, 'ba', 52, TD) +
     shadow(470, 445, 110) + block(510, 366, 54, SUN, SUND) + cloth('M360 425 Q380 350 450 356 Q520 352 530 425 Z', SKY) +
     path('M370 410 Q330 404 300 380', MUTED, 6) + path('M318 372 L298 380 L310 400', MUTED, 6) +
     shadow(740, 445, 110) + circ(670, 370, 34, BLUSH) + circ(660, 364, 5, INK) + circ(682, 364, 5, INK) + rr(640, 330, 60, 18, 9, TD) +
     cloth('M690 360 L840 350 Q850 400 830 430 L690 430 Q680 400 690 360 Z', SUN) + ''.join(circ(720 + i * 34, 395, 8, SUND) for i in range(4)) +
     label(140, 485, 'cilukba') + label(450, 485, 'tarik') + label(740, 485, 'selimut boneka'))
save('big-w2e-kain', 500, b)

# ================================================================== 7. w2e-d15 screen time (pintar)
def stand_phone(x, y, w, h, pose='sayang'):
    inner = tunas(pose, w * .62, w * .72, x + w * .19, y + h * .22) + heart(x + w * .78, y + h * .2, 14, TERRA)
    return (f'<path d="M{x+w*.2} {y+h+40} L{x+w*.8} {y+h+40} L{x+w*.62} {y+h-20} L{x+w*.38} {y+h-20} Z" fill="{GREY}"/>' + phone(x, y, w, h, '#e3eee6', 0, inner))
b = (floor(320, 420) + shadow(370, 395, 140) + stand_phone(250, 20, 200, 320) +
     shadow(600, 395, 100) + tunas('halo', 160, 187, 520, 140) + bubble(660, 40, 160, 80, '#e3eee6', 'left') + text(740, 96, 'halo', 40, SD) + check(160, 120, 30))
save('hero-w2e-videocall', 420, b)

b = (floor(400, 500) + tv(60, 70, 330, 220) + text(225, 200, 'z z', 60, '#8a8f9c') +
     shadow(600, 470, 200) + tunas('sayang', 160, 187, 460, 280) + open_book(700, 360, 220, 80, '', '', CARD, LINE) + ball(735, 398, 0) +
     heart(640, 230, 26, TERRA) + rr(565, 175, 0, 0, 0, 'none'))
save('big-w2e-tv-mati', 500, b)

b = (floor(400, 500) + shadow(250, 470, 140) + stand_phone(150, 60, 190, 300, 'hore') +
     shadow(560, 470, 100) + tunas('sayang', 160, 187, 480, 280) + heart(440, 160, 22, TERRA) + heart(470, 110, 16, BLUSH) + check(720, 260, 30))
save('big-w2e-vc', 500, b)

b = (floor(400, 500) + clock(200, 200, 140) + text(200, 440, '1 jam', 44, INK) + rr(140, 470, 0, 0, 0, 'none') +
     shadow(600, 470, 150) + tunas('santai', 150, 175, 450, 290) + phone(640, 330, 140, 100, SKY, -8, circ(710, 378, 20, '#fff', .6)) + heart(600, 250, 22, TERRA))
save('big-w2e-satu-jam', 500, b)

def mini_tv(cx, base, s): return rr(cx - s, base - s * 1.3, s * 2, s * 1.3, 10, INK) + rr(cx - s + 8, base - s * 1.3 + 8, s * 2 - 16, s * 1.3 - 16, 6, SKY)
b = (floor(430, 500) + rr(60, 210, 220, 220, 16, SUN) + rr(280, 290, 220, 140, 16, SUND, op=.7) + rr(500, 360, 220, 70, 16, SAGE) +
     mini_tv(170, 200, 70) + mini_tv(390, 280, 50) + mini_tv(610, 350, 30) +
     path('M120 120 Q300 60 560 250', MUTED, 6, dash='3 16') + path('M540 228 L562 252 L532 260', MUTED, 6) +
     shadow(780, 480, 80) + tunas('santai', 140, 163, 720, 290) + check(800, 230, 28))
save('big-w2e-pelan-pelan', 500, b)

pot = (rr(80, 290, 260, 140, 30, GREY) + rr(60, 280, 300, 30, 15, '#b0a99e') + rr(40, 330, 40, 22, 10, '#b0a99e') + rr(340, 330, 40, 22, 10, '#b0a99e') +
       rr(110, 320, 70, 80, 20, '#fff', op=.3))
b = (floor(400, 500) + shadow(210, 460, 170) + pot + stick(150, 160, 190, 24, 40, BOX, BOXD) + text(150, 220, 'dung', 46, TD, rot=-8) +
     shadow(500, 470, 100) + tunas('hore', 170, 198, 410, 270) + note(400, 150, 1.0, SUND) + note(560, 120, .8, TERRA) +
     shadow(720, 470, 110) + open_book(720, 360, 220, 80, '', '', CARD, LINE) + circ(780, 395, 0, INK) + ball(670, 390, 0))
save('big-w2e-gantinya', 500, b)

autocrop(NAMES)
print('ok', len(NAMES))
