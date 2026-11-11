# Story scenes for the w4 LONG batch, group E (18 to 22 Nov):
#   w4l-kakak-adik, w4l-ayah-main, w4l-s02-tantrum-minimarket.  Run: python tools/mkart_w4_E.py [contact.png]
# Every name starts with "w4le-" so it never collides with other batches.
# Family from tools/people.py (Mama in hijab, Ayah, Adek ~2y, Kakak ~4-5y). Flat palette, no real faces, no text but short labels.
import sys, os, io, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

NAMES = []
GREY = '#c8c2b8'; GREYL = '#e2ddd5'; PANTS = '#6b5d50'; PANTSD = '#574a3e'; MINT = '#e3eee6'
GRAPE = '#9b7fc0'; LEAF = '#8fbf7a'


def save(name, h, body):
    svg(name, h, body); NAMES.append(name)


# ------------------------------------------------------------------ small kit
def rr(x, y, w, h, r, f, op=1, rot=0, st=None, sw=0):
    t = f' transform="rotate({rot} {x+w/2} {y+h/2})"' if rot else ''
    s = f' stroke="{st}" stroke-width="{sw}"' if st else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" opacity="{op}"{t}{s}/>'
def circ(cx, cy, r, f, op=1): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" opacity="{op}"/>'
def path(d, col, w=8, fill='none', op=1):
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'
def heart(cx, cy, s, col=TERRA):
    return (f'<path d="M{cx} {cy+s*.9} C{cx-s*1.5} {cy} {cx-s*.9} {cy-s} {cx} {cy-s*.35} '
            f'C{cx+s*.9} {cy-s} {cx+s*1.5} {cy} {cx} {cy+s*.9} Z" fill="{col}"/>')
def spark(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'
def sweat(x, y, s=1):
    return f'<path d="M{x} {y} q{12*s} {26*s} 0 {36*s} q-{12*s} -{10*s} 0 -{36*s}" fill="{SKY}"/>'
def nope(cx, cy, r=34):
    k = r * .4
    return circ(cx, cy, r, TD) + path(f'M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}', '#fff', r * .26)
def check(cx, cy, r=34):
    return circ(cx, cy, r, SD) + path(f'M{cx-r*.45} {cy} L{cx-r*.12} {cy+r*.33} L{cx+r*.5} {cy-r*.33}', '#fff', r * .26)
def block(x, y, s, f, fd, rot=0):
    return f'<g transform="rotate({rot} {x+s/2} {y+s/2})">' + rr(x, y, s, s, 10, f) + rr(x, y + s * .72, s, s * .28, 8, fd, op=.6) + circ(x + s / 2, y + s * .4, s * .16, '#fff', .45) + '</g>'
def pillow(x, y, w, h, f, fd, rot=0):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">' + rr(x, y, w, h, h * .42, f) + rr(x, y + h * .6, w, h * .4, h * .3, fd, op=.45) +
            circ(x + w * .5, y + h * .45, 6, fd) + '</g>')
def zzz(x, y, s=1, col=SKYD):
    return ''.join(text(x + i * 26 * s, y - i * 30 * s, 'z', (30 + i * 8) * s, col) for i in range(3))


def bayi(cx, cy, s=1.0, rot=0, awake=False):
    """Newborn in a swaddle (no bottle, no pacifier). Head on the viewer's left."""
    hx, hy, hr = cx - 52 * s, cy - 6 * s, 30 * s
    eyes = (''.join(f'<path d="M{hx+k*11*s-6*s} {hy+2*s} Q{hx+k*11*s} {hy+7*s} {hx+k*11*s+6*s} {hy+2*s}" stroke="{INK}" stroke-width="{3*s}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
            if not awake else ''.join(circ(hx + k * 11 * s, hy + 2 * s, 3.6 * s, INK) for k in (-1, 1)))
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<ellipse cx="{cx+8*s}" cy="{cy}" rx="{74*s}" ry="{44*s}" fill="{CARD}" stroke="{LINE}" stroke-width="{3*s}"/>'
            f'<path d="M{cx-20*s} {cy+40*s} Q{cx+30*s} {cy-4*s} {cx+76*s} {cy-6*s}" stroke="{BLUSH}" stroke-width="{7*s}" fill="none"/>'
            f'<path d="M{cx+20*s} {cy+42*s} Q{cx+56*s} {cy+18*s} {cx+80*s} {cy+12*s}" stroke="{LINE}" stroke-width="{5*s}" fill="none"/>'
            + circ(hx, hy, hr + 8 * s, BLUSH) + circ(hx, hy, hr, SKIN) + eyes +
            f'<ellipse cx="{hx-14*s}" cy="{hy+12*s}" rx="{6*s}" ry="{4*s}" fill="{CHEEK}" opacity="0.6"/><ellipse cx="{hx+14*s}" cy="{hy+12*s}" rx="{6*s}" ry="{4*s}" fill="{CHEEK}" opacity="0.6"/>'
            f'<path d="M{hx-4*s} {hy-hr+2*s} q{6*s} -{12*s} {12*s} -{2*s}" stroke="{HAIR}" stroke-width="{4*s}" fill="none" stroke-linecap="round"/>'
            '</g>')


def chest(kind, cx, cy, s):
    """Point in front of the chest where person(..., 'pegang') puts the hands."""
    r = head_r(kind, s); return cx, cy + 0.95 * r + 1.1 * r


# ------------------------------------------------------------------ full-body figures (post 2: physical play)
def head(kind, cx, cy, s, expr='senang', rot=0, flip=False):
    """Only the head of a people.py figure (torso clipped off), optionally rotated, for full-body poses."""
    r = head_r(kind, s)
    cid = f'h{abs(hash((kind, cx, cy, s, expr, rot))) % 10**8}'
    clip = f'<clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy-r*0.15}" rx="{r*1.5}" ry="{r*1.27}"/></clipPath>'
    g = f'<g clip-path="url(#{cid})">{person(kind, cx, cy, s, expr, "none", flip)}</g>'
    return f'<defs>{clip}</defs><g transform="rotate({rot} {cx} {cy})">{g}</g>'
def limb(pts, col, w):
    d = f'M{pts[0][0]} {pts[0][1]}'
    if len(pts) == 3:
        d += f' Q{pts[1][0]} {pts[1][1]} {pts[2][0]} {pts[2][1]}'
    else:
        d += ''.join(f' L{x} {y}' for x, y in pts[1:])
    return path(d, col, w)
def hand(x, y, r): return circ(x, y, r, SKIN)
def foot(x, y, r, col=INK, rot=0): return f'<ellipse cx="{x}" cy="{y}" rx="{r*1.35}" ry="{r*0.8}" fill="{col}" transform="rotate({rot} {x} {y})"/>'
def torso(x1, y1, x2, y2, w, col, cold):
    return path(f'M{x1} {y1} L{x2} {y2}', col, w) + path(f'M{x1} {y1} L{x2} {y2}', cold, w * 0.35, op=0.25)
def sock(x, y, r, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">' + f'<ellipse cx="{x}" cy="{y}" rx="{r*1.4}" ry="{r*0.85}" fill="{SAGE}"/>'
            + path(f'M{x-r*0.5} {y-r*0.75} L{x-r*0.5} {y+r*0.75}', CARD, r * 0.25) + path(f'M{x+r*0.2} {y-r*0.8} L{x+r*0.2} {y+r*0.8}', CARD, r * 0.25) + '</g>')
def carpet(x, y, w, h):
    return rr(x, y, w, h, 20, MINT) + ''.join(rr(x + 30, y + 14 + i * 22, w - 60, 6, 3, SAGE, op=.35) for i in range(max(1, int((h - 20) / 22))))


# ================================================================== POST 1: kakak-adik (bust style, table in front)
H, T = 520, 440

# HERO: Mama holds the newborn, Kakak beside her, cross. Thought: "Aku kesel."
m = seat('mama', 1.36, T, True); k = seat('kakak', 1.32, T)
bx, by = chest('mama', 300, m, 1.36)
b = (person('mama', 300, m, 1.36, 'lembut', 'pegang') + bayi(bx + 10, by - 26, 1.05, -8) +
     person('kakak', 640, k, 1.32, 'ngomel', 'none') + table(T, H) +
     bubble(560, 0, 300, ['Aku kesel.'], 'bl', size=40, think=True))
save('hero-w4le-kakak-kesel', H, b)

# 1: involve her: pick a baby outfit together (no forcing)
m = seat('mama', 1.36, T); k = seat('kakak', 1.32, T, True)
kx, ky = chest('kakak', 560, k, 1.32)
onesie = (f'<path d="M{kx-70} {ky-60} L{kx-30} {ky-74} Q{kx} {ky-58} {kx+30} {ky-74} L{kx+70} {ky-60} L{kx+84} {ky-26} L{kx+48} {ky-18} '
          f'L{kx+48} {ky+46} Q{kx} {ky+62} {kx-48} {ky+46} L{kx-48} {ky-18} L{kx-84} {ky-26} Z" fill="{SKY}"/>' +
          circ(kx, ky - 6, 9, CARD) + circ(kx, ky + 22, 9, CARD))
b = (person('mama', 230, m, 1.36, 'senang', 'none') + person('kakak', 560, k, 1.32, 'senang', 'pegang') + onesie + table(T, H) +
     f'<rect x="700" y="{T-70}" width="140" height="70" rx="12" fill="{BOX}"/><rect x="700" y="{T-70}" width="140" height="18" rx="9" fill="{BOXD}"/>' +
     rr(722, T - 96, 46, 30, 8, BLUSH, rot=-10) + rr(772, T - 92, 46, 26, 8, SUN, rot=8) +
     bubble(380, 0, 470, ['"Yang biru buat adik."'], 'bl', size=36))
save('big-w4le-ajak-nyiapin', H, b)

# 2: read a story about a new baby
m = seat('mama', 1.36, T); k = seat('kakak', 1.32, T)
book = (f'<g transform="translate(440 {T-150})">' + rr(-170, 0, 170, 150, 14, CARD, st=LINE, sw=4) + rr(0, 0, 170, 150, 14, CARD, st=LINE, sw=4) +
        circ(-85, 60, 34, SKIN) + rr(-125, 92, 80, 40, 18, TERRA) + bayi(85, 78, 0.62) + path('M0 4 L0 146', LINE, 6) + '</g>')
b = (person('mama', 200, m, 1.36, 'lembut', 'none') + person('kakak', 690, k, 1.32, 'senang', 'none') + table(T, H) + book +
     heart(560, 120, 26, BLUSH) + heart(320, 90, 18, TERRA))
save('big-w4le-baca-cerita', H, b)

# 3: keep big routines steady: Kakak sleeps in her own bed, same as before; calendar with arrows
bed = (rr(80, 300, 560, 120, 30, BOX) + rr(80, 390, 560, 30, 15, BOXD) + rr(60, 230, 50, 220, 20, BOXD) + rr(610, 270, 40, 180, 18, BOXD) +
       rr(120, 262, 150, 70, 30, CARD, st=LINE, sw=4))
kk = person('kakak', 210, 270, 0.92, 'lembut', 'none')
cid = 'bedclip'
kk = f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="880" height="330"/></clipPath></defs><g clip-path="url(#{cid})">{kk}</g>'
blanket = f'<path d="M260 300 Q450 270 630 300 L630 400 L260 400 Q240 350 260 300 Z" fill="{SKY}"/><path d="M260 300 Q450 270 630 300 L630 322 Q450 292 262 322 Z" fill="{SKYD}"/>'
guling = rr(300, 304, 220, 54, 27, CARD, st=LINE, sw=4)
moon = f'<path d="M780 70 a50 50 0 1 0 40 80 a40 40 0 1 1 -40 -80 Z" fill="{SUN}"/>'
b = (floor(440, H) + bed + kk + guling + blanket + moon + spark(700, 70, 14) + spark(840, 200, 10) + zzz(320, 220, 1.1))
save('big-w4le-rutinitas', H, b)

# 4: one-on-one time while the baby sleeps
m = seat('mama', 1.32, T); k = seat('kakak', 1.28, T)
crib = (rr(690, 250, 170, 190, 18, CARD, st=LINE, sw=4) + ''.join(rr(706 + i * 34, 262, 10, 170, 5, LINE) for i in range(5)) + bayi(775, 236, 0.62))
b = (person('mama', 200, m, 1.32, 'senang', 'none') + person('kakak', 470, k, 1.28, 'senang', 'none') + crib + table(T, H) +
     block(250, T - 64, 62, SUN, SUND, -6) + block(320, T - 64, 62, SAGE, SD, 4) + block(285, T - 124, 62, TERRA, TD, -2) +
     zzz(830, 210, 0.9) + heart(340, 90, 28, TERRA))
save('big-w4le-berdua', H, b)

# 5: accept the anger: name it, limit only the hitting
m = seat('mama', 1.36, T); k = seat('kakak', 1.32, T)
b = (person('mama', 240, m, 1.36, 'lembut', 'none') + person('kakak', 640, k, 1.32, 'ngomel', 'none') + table(T, H) +
     bubble(20, 0, 520, ['"Kamu kesel ya,', 'Mama sibuk terus."'], 'br', size=38))
save('big-w4le-terima-kesal', H, b)

# cheat row: visitors greet Kakak first (a small gift for her too)
k = seat('kakak', 1.32, T, True)
kx, ky = chest('kakak', 360, k, 1.32)
gift = (rr(kx - 70, ky - 60, 140, 110, 12, SAGE) + rr(kx - 12, ky - 60, 24, 110, 4, SUN) + rr(kx - 70, ky - 14, 140, 22, 4, SUN) +
        f'<path d="M{kx} {ky-60} q-50 -40 -60 -6 q20 14 60 6 Z M{kx} {ky-60} q50 -40 60 -6 q-20 14 -60 6 Z" fill="{SUN}"/>')
b = (person('kakak', 360, k, 1.32, 'senang', 'pegang') + gift + table(T, H) + spark(560, 140, 22) + spark(170, 110, 16) + heart(600, 240, 24, BLUSH))
save('big-w4le-tamu-kakak', H, b)


# ================================================================== POST 3: tantrum di minimarket (bust style, counter in front)
def shelves():
    out = rr(0, 0, 880, 330, 24, '#f6ead9')
    for i, y in enumerate((96, 210)):
        out += rr(20, y, 840, 14, 7, BOXD, op=.55)
        for j in range(9):
            x = 50 + j * 92
            col = (SKY, SAGE, SUN, BLUSH, TERRA)[(i * 3 + j) % 5]
            out += rr(x, y - 62, 58, 62, 10, col, op=.55)
    return out
def candy_rack(x, y):
    """Small candy rack by the till: lollipops and wrapped sweets (no brands)."""
    out = rr(x, y, 150, 170, 16, CARD, st=LINE, sw=4) + rr(x, y + 80, 150, 10, 5, LINE)
    for i, (dx, col) in enumerate(((30, TERRA), (74, SUN), (118, SAGE))):
        out += path(f'M{x+dx} {y+70} L{x+dx} {y+36}', MUTED, 6) + circ(x + dx, y + 30, 18, col) + f'<path d="M{x+dx-10} {y+28} q10 -12 20 0" stroke="#fff" stroke-width="4" fill="none" opacity="0.6"/>'
        c2 = (BLUSH, SKY, SUN)[i]
        out += f'<path d="M{x+dx-22} {y+128} l10 -8 l0 16 Z M{x+dx+22} {y+128} l-10 -8 l0 16 Z" fill="{c2}"/>' + rr(x + dx - 13, y + 118, 26, 20, 9, c2)
    return out
def queue():
    """Other shoppers as plain silhouettes, no faces."""
    out = ''
    for x, s in ((720, 1.0), (820, 0.9)):
        out += circ(x, 150 * s + 20, 44 * s, GREYL) + f'<path d="M{x-70*s} 330 Q{x-70*s} {220*s+30} {x} {210*s+30} Q{x+70*s} {220*s+30} {x+70*s} 330 Z" fill="{GREYL}"/>'
    return out
def eyes_look(x, y):
    return circ(x - 14, y, 6, MUTED) + circ(x + 10, y, 6, MUTED)

# HERO: Adek wails for candy at the till, Mama surprised
a = seat('adek', 1.42, T); m = seat('mama', 1.3, T)
b = (shelves() + candy_rack(330, T - 170) + person('mama', 160, m, 1.3, 'kaget', 'none') + person('adek', 640, a, 1.42, 'nangis', 'none') +
     table(T, H, col=BOX, edge=BOXD) +
     bubble(490, 0, 380, ['"MAU PERMEN."'], 'bl', size=40))
save('hero-w4le-tantrum-kasir', H, b)

# 1: the scene: long queue, everyone looking
a = seat('adek', 1.3, T); m = seat('mama', 1.3, T)
b = (shelves() + queue() + eyes_look(720, 150) + eyes_look(820, 160) + candy_rack(330, T - 170) +
     person('mama', 170, m, 1.3, 'capek', 'none') + person('adek', 570, a, 1.3, 'nangis', 'none') + table(T, H, col=BOX, edge=BOXD) +
     path('M520 120 l-26 -20 M560 104 l0 -30 M600 120 l26 -20', TERRA, 7))
save('big-w4le-tantrum-antre', H, b)

# 2: stay calm first: Mama breathes
a = seat('adek', 1.3, T); m = seat('mama', 1.4, T)
b = (shelves() + person('mama', 230, m, 1.4, 'lembut', 'tangan-dada') + person('adek', 640, a, 1.3, 'nangis', 'none') + table(T, H, col=BOX, edge=BOXD) +
     bubble(30, 0, 420, ['Tarik napas dulu.'], 'bl', size=36, think=True))
save('big-w4le-tantrum-tenang', H, b)

# 3: name the feeling at eye level
a = seat('adek', 1.36, T); m = seat('mama', 1.4, T)
b = (shelves() + person('mama', 250, m, 1.4, 'lembut', 'none') + person('adek', 640, a, 1.36, 'sedih', 'none') + table(T, H, col=BOX, edge=BOXD) +
     bubble(10, 0, 590, ['"Kamu pengen permen,', 'kesel ya."'], 'br', size=38))
save('big-w4le-tantrum-sebut', H, b)

# 4: a clear limit (candy stays on the rack)
a = seat('adek', 1.36, T); m = seat('mama', 1.4, T)
b = (shelves() + candy_rack(690, T - 170) + nope(780, T - 196, 30) + person('mama', 200, m, 1.4, 'lembut', 'none') + person('adek', 520, a, 1.36, 'ngomel', 'none') +
     table(T, H, col=BOX, edge=BOXD) + bubble(10, 0, 560, ['"Permennya', 'nggak hari ini."'], 'br', size=38))
save('big-w4le-tantrum-batas', H, b)

# 5: a small choice: hold the bananas or push the basket
a = seat('adek', 1.36, T, True); m = seat('mama', 1.4, T)
ax, ay = chest('adek', 640, a, 1.36)
bx_, by_ = ax + 90, ay - 40
banana = (f'<path d="M{bx_-70} {by_-50} Q{bx_-50} {by_+30} {bx_+50} {by_+10} Q{bx_+10} {by_-6} {bx_-50} {by_-60} Z" fill="{SUN}" stroke="{BOXD}" stroke-width="5"/>'
          f'<path d="M{bx_-60} {by_-26} Q{bx_-26} {by_+44} {bx_+66} {by_+32} Q{bx_+24} {by_+18} {bx_-44} {by_-36} Z" fill="#f7d77a" stroke="{BOXD}" stroke-width="5"/>' + rr(bx_ - 78, by_ - 66, 18, 22, 5, BOXD)
          + limb([(ax + 40, ay + 10), (ax + 60, ay - 10), (bx_ - 50, by_ - 10)], SUND, 26) + hand(bx_ - 48, by_ - 12, 17))
basket = (f'<path d="M30 {T-120} L230 {T-120} L210 {T} L50 {T} Z" fill="{TERRA}"/>' + ''.join(path(f'M{70+i*40} {T-104} L{74+i*36} {T-16}', '#fff', 6, op=.45) for i in range(4)) +
          path(f'M60 {T-120} Q130 {T-200} 200 {T-120}', TD, 10))
b = (shelves() + person('mama', 330, m, 1.4, 'senang', 'none') + person('adek', 640, a, 1.36, 'lembut', 'pegang') + banana + basket + table(T, H, col=BOX, edge=BOXD) +
     bubble(20, 0, 560, ['"Mau pegang pisang,', 'atau bawa keranjang?"'], 'br', size=36))
save('big-w4le-tantrum-pilihan', H, b)

# cheat row: move to a quieter spot (outside, by the plant)
a = seat('adek', 1.2, T); m = seat('mama', 1.3, T)
plant = rr(700, T - 110, 110, 110, 14, BOX) + ''.join(f'<ellipse cx="{755+dx}" cy="{T-150+dy}" rx="30" ry="58" fill="{c}" transform="rotate({rot} {755+dx} {T-150+dy})"/>' for dx, dy, rot, c in ((-30, 10, -30, SAGE), (30, 10, 30, SAGE), (0, -10, 0, SD)))
b = (rr(0, 0, 880, 330, 24, MINT) + person('mama', 240, m, 1.3, 'lembut', 'peluk') + person('adek', 480, a, 1.2, 'sedih', 'none') + plant + table(T, H) +
     heart(600, 110, 22, BLUSH))
save('big-w4le-tantrum-sepi', H, b)


# ================================================================== POST 2: ayah main fisik (full-body poses on a carpet)
F = 440   # floor line

# HERO: Ayah "lost" the wrestle, flat on his back; Adek sits on his tummy cheering
ayah_lying_r = head_r('ayah', 1.0)
def ayah_lying(hx, s=1.0, expr='senang', legs='flat'):
    """Ayah on his back, head on the left at hx. Returns svg; hip at hx+300*s."""
    r = 62 * s; y = F - 46 * s
    out = ''
    hip = (hx + 300 * s, y + 6 * s)
    if legs == 'flat':
        out += limb([hip, (hip[0] + 110 * s, y - 40 * s), (hip[0] + 190 * s, y + 10 * s)], PANTSD, 44 * s) + foot(hip[0] + 205 * s, y + 4 * s, 18 * s, INK, -60)
        out += limb([hip, (hip[0] + 130 * s, y - 10 * s), (hip[0] + 230 * s, y + 18 * s)], PANTS, 46 * s) + foot(hip[0] + 245 * s, y + 10 * s, 20 * s, INK, -70)
    out += torso(hx + 90 * s, y, hip[0], hip[1], 110 * s, SKY, SKYD)
    out += head('ayah', hx, y - 8 * s, s, expr, rot=-90)
    return out, hip, y
a_svg, hip, y = ayah_lying(130, 1.0)
arms = (limb([(230, y - 10), (220, y - 90), (170, y - 150)], SKY, 40) + hand(166, y - 156, 22) +
        limb([(250, y + 20), (330, y + 60), (390, y + 40)], SKYD, 40) + hand(398, y + 38, 22))
ad_hip = (370, y - 60)
adek = (limb([ad_hip, (400, y - 10), (450, y + 6)], SKIN, 30) + foot(462, y + 6, 15, TERRA) +
        torso(370, y - 150, 370, y - 64, 92, SUN, SUND) +
        limb([(330, y - 150), (300, y - 210), (300, y - 250)], SUN, 28) + hand(300, y - 256, 17) +
        limb([(410, y - 150), (440, y - 210), (446, y - 250)], SUN, 28) + hand(446, y - 256, 17) +
        sock(446, y - 290, 22, -20) +
        head('adek', 370, y - 222, 1.0, 'senang'))
b = (carpet(40, F - 20, 800, 80) + pillow(560, F - 70, 170, 64, BLUSH, TERRA, 8) + pillow(30, F - 40, 120, 50, SUN, SUND, -6) + a_svg + arms + adek +
     sweat(70, y - 120, 1.1) + sweat(100, y - 150, 0.8) + spark(250, 80, 20) + spark(500, 70, 14, TERRA) +
     bubble(520, 0, 330, ['"Ayah kalah."'], 'bl', size=40))
save('hero-w4le-ayah-kalah', H, b)

# 1 (research): taking turns: this time Ayah wins the sock, Adek is cross, Ayah says "gantian ya"
y = seat('ayah', 1.32, T); a = seat('adek', 1.36, T)
ax_, ay_ = chest('ayah', 260, y, 1.32)
b = (person('ayah', 260, y, 1.32, 'senang', 'none') + limb([(330, ay_ - 30), (380, ay_ - 120), (360, ay_ - 200)], SKYD, 40) + hand(358, ay_ - 206, 22) + sock(358, ay_ - 236, 24, -30) +
     person('adek', 640, a, 1.36, 'ngomel', 'none') + table(T, H, col=MINT, edge=SAGE) +
     bubble(430, 0, 420, ['"Besok gantian ya."'], 'bl', size=36))
save('big-w4le-gantian', H, b)

# 2: kuda-kudaan: Ayah on all fours, Adek on his back, carpet underneath
def kuda(x0, s=1.0, ayah_expr='senang', adek_expr='senang'):
    # x0 = Ayah's hip; he faces right
    out = ''
    back_y = F - 170 * s
    sh = (x0 + 250 * s, back_y)          # shoulder
    hipp = (x0, back_y + 10 * s)
    # far limbs (darker)
    out += limb([(sh[0] - 20 * s, sh[1]), (sh[0] - 10 * s, F - 70 * s), (sh[0] - 4 * s, F - 14 * s)], SKYD, 38 * s) + hand(sh[0] - 4 * s, F - 14 * s, 20 * s)
    out += limb([(hipp[0] + 24 * s, hipp[1]), (hipp[0] + 34 * s, F - 26 * s), (hipp[0] + 34 * s, F - 26 * s), (hipp[0] - 80 * s, F - 22 * s)], PANTSD, 40 * s) + foot(hipp[0] - 96 * s, F - 22 * s, 18 * s, INK, 10)
    out += torso(hipp[0], hipp[1], sh[0], sh[1], 120 * s, SKY, SKYD)
    # near limbs
    out += limb([sh, (sh[0] + 20 * s, F - 80 * s), (sh[0] + 26 * s, F - 14 * s)], SKY, 40 * s) + hand(sh[0] + 28 * s, F - 14 * s, 21 * s)
    out += limb([hipp, (hipp[0] - 6 * s, F - 22 * s), (hipp[0] - 6 * s, F - 22 * s), (hipp[0] - 124 * s, F - 20 * s)], PANTS, 44 * s) + foot(hipp[0] - 142 * s, F - 20 * s, 20 * s, INK, 10)
    out += head('ayah', sh[0] + 80 * s, back_y - 30 * s, s, ayah_expr)
    # Adek riding
    ah = (x0 + 120 * s, back_y - 62 * s)
    out += torso(ah[0], ah[1] - 86 * s, ah[0], ah[1], 88 * s, SUN, SUND)
    out += limb([(ah[0] + 10 * s, ah[1] + 10 * s), (ah[0] + 40 * s, ah[1] + 60 * s), (ah[0] + 20 * s, ah[1] + 110 * s)], SKIN, 28 * s) + foot(ah[0] + 26 * s, ah[1] + 120 * s, 15 * s, TERRA)
    out += limb([(ah[0] + 30 * s, ah[1] - 80 * s), (ah[0] + 90 * s, ah[1] - 40 * s), (ah[0] + 120 * s, ah[1] + 10 * s)], SUN, 26 * s) + hand(ah[0] + 122 * s, ah[1] + 14 * s, 16 * s)
    out += limb([(ah[0] - 30 * s, ah[1] - 80 * s), (ah[0] - 70 * s, ah[1] - 130 * s), (ah[0] - 60 * s, ah[1] - 180 * s)], SUN, 26 * s) + hand(ah[0] - 60 * s, ah[1] - 186 * s, 16 * s)
    out += head('adek', ah[0], ah[1] - 150 * s, s, adek_expr)
    return out
b = (carpet(30, F - 24, 820, 84) + kuda(330) + sweat(720, 150, 1.0) + spark(160, 90, 18) + spark(820, 70, 14, TERRA) +
     path(f'M100 {F-110} l-50 0 M110 {F-70} l-60 0', LINE, 10))
save('big-w4le-kuda', H, b)

# 3: pesawat-pesawatan: Ayah on his back, shins up, Adek lying on his shins, hands held, low to the floor
a_svg, hip, y = ayah_lying(110, 1.0, 'senang', legs='none')
knee = (hip[0] + 70, y - 150)
legs = (limb([hip, (hip[0] + 40, y - 70), knee], PANTS, 46) + limb([knee, (knee[0] + 90, knee[1] - 4), (knee[0] + 170, knee[1] + 6)], PANTS, 42) + foot(knee[0] + 188, knee[1] + 6, 19, INK, 80))
adek_body = (torso(knee[0] + 10, knee[1] - 50, knee[0] + 170, knee[1] - 50, 84, SUN, SUND) +
             limb([(knee[0] + 160, knee[1] - 40), (knee[0] + 230, knee[1] - 50), (knee[0] + 270, knee[1] - 30)], SKIN, 26) + foot(knee[0] + 284, knee[1] - 28, 14, TERRA, 80) +
             head('adek', knee[0] - 50, knee[1] - 78, 1.0, 'senang', rot=-14))
hands_held = (knee[0] - 40, knee[1] + 10)
arms = (limb([(hip[0] - 150, y - 20), (hip[0] - 150, y - 110), hands_held], SKY, 38) +
        limb([(knee[0] + 20, knee[1] - 40), (knee[0] - 10, knee[1] - 10), (hands_held[0] + 8, hands_held[1] - 6)], SUN, 24) +
        hand(*hands_held, 22))
b = (carpet(30, F - 24, 820, 84) + a_svg + legs + adek_body + arms +
     path(f'M{knee[0]+300} {knee[1]-90} l50 0 M{knee[0]+290} {knee[1]-50} l70 0', LINE, 10) + spark(130, 120, 18) + spark(760, 90, 14, TERRA))
save('big-w4le-pesawat', H, b)

# 4: gulat kaos kaki: sitting face to face, legs out, one sock each
y = seat('ayah', 1.2, T); a = seat('adek', 1.24, T)
b = (person('ayah', 200, y, 1.2, 'senang', 'none') + person('adek', 690, a, 1.24, 'senang', 'none') + table(T, H, col=MINT, edge=SAGE) +
     limb([(250, T + 30), (360, T + 36), (430, T + 30)], PANTS, 44) + sock(452, T + 28, 22, 0) +
     limb([(640, T + 34), (580, T + 40), (520, T + 36)], SKIN, 30) + sock(500, T + 34, 18, 0) +
     limb([(270, T - 90), (360, T - 120), (470, T - 40)], SKY, 38) + hand(480, T - 30, 21) +
     limb([(640, T - 90), (580, T - 110), (540, T - 30)], SUN, 28) + hand(534, T - 24, 17) +
     spark(440, 120, 22) + spark(380, 190, 12, TERRA) + heart(520, 170, 18, BLUSH))
save('big-w4le-gulat-kaos-kaki', H, b)

# 5: babies are different: hold close, head supported; no tossing, no hard shaking
y = seat('ayah', 1.4, T, True)
cx_, cy_ = chest('ayah', 280, y, 1.4)
up_icon = (circ(660, 150, 104, CARD) + f'<circle cx="660" cy="150" r="104" fill="none" stroke="{LINE}" stroke-width="5"/>' + bayi(668, 196, 0.66) +
           path('M660 120 L660 54 M634 80 L660 54 L686 80', MUTED, 10) + nope(744, 76, 34))
shake_icon = (circ(660, 390, 104, CARD) + f'<circle cx="660" cy="390" r="104" fill="none" stroke="{LINE}" stroke-width="5"/>' + bayi(668, 394, 0.66) +
              path('M584 340 q-20 25 0 50 q20 25 0 50 M748 340 q20 25 0 50 q-20 25 0 50', MUTED, 8) + nope(744, 316, 34))
b = (person('ayah', 250, y, 1.4, 'lembut', 'pegang') + bayi(cx_ + 10, cy_ - 30, 1.15, -12) + hand(cx_ - 70, cy_ - 34, 26) + table(T, H, col=MINT, edge=SAGE) +
     heart(110, 110, 24, BLUSH))
b = b.replace(table(T, H, col=MINT, edge=SAGE), '') + table(T, H, col=MINT, edge=SAGE) + up_icon + shake_icon
save('big-w4le-bayi-pelan', H, b)

# cheat row: kejar-kejaran, Ayah "slow" on purpose (and out of breath)
def runner_ayah(x, s=1.0):
    hipp = (x, F - 150 * s); sh = (x + 50 * s, F - 290 * s)
    out = limb([hipp, (x - 40 * s, F - 80 * s), (x - 110 * s, F - 40 * s)], PANTSD, 42 * s) + foot(x - 126 * s, F - 40 * s, 19 * s, INK, -30)
    out += limb([(sh[0] - 20 * s, sh[1] + 20 * s), (sh[0] - 70 * s, sh[1] + 80 * s), (sh[0] - 40 * s, sh[1] + 130 * s)], SKYD, 36 * s) + hand(sh[0] - 36 * s, sh[1] + 134 * s, 19 * s)
    out += torso(hipp[0], hipp[1], sh[0], sh[1], 116 * s, SKY, SKYD)
    out += limb([hipp, (x + 60 * s, F - 90 * s), (x + 50 * s, F - 14 * s)], PANTS, 44 * s) + foot(x + 70 * s, F - 14 * s, 20 * s, INK)
    out += limb([sh, (sh[0] + 60 * s, sh[1] + 50 * s), (sh[0] + 110 * s, sh[1] + 20 * s)], SKY, 38 * s) + hand(sh[0] + 116 * s, sh[1] + 16 * s, 21 * s)
    out += head('ayah', sh[0] + 30 * s, sh[1] - 80 * s, s, 'capek')
    return out
def runner_adek(x, s=1.0):
    hipp = (x, F - 96 * s); sh = (x + 20 * s, F - 190 * s)
    out = limb([hipp, (x - 30 * s, F - 50 * s), (x - 70 * s, F - 30 * s)], SKIN, 28 * s) + foot(x - 82 * s, F - 30 * s, 14 * s, TERRA, -30)
    out += torso(hipp[0], hipp[1], sh[0], sh[1], 86 * s, SUN, SUND)
    out += limb([hipp, (x + 40 * s, F - 50 * s), (x + 40 * s, F - 12 * s)], SKIN, 28 * s) + foot(x + 54 * s, F - 12 * s, 15 * s, TERRA)
    out += limb([sh, (sh[0] + 50 * s, sh[1] - 30 * s), (sh[0] + 70 * s, sh[1] - 90 * s)], SUN, 24 * s) + hand(sh[0] + 72 * s, sh[1] - 96 * s, 15 * s)
    out += limb([(sh[0] - 10 * s, sh[1] + 10 * s), (sh[0] - 60 * s, sh[1] + 20 * s), (sh[0] - 80 * s, sh[1] - 30 * s)], SUN, 24 * s) + hand(sh[0] - 82 * s, sh[1] - 36 * s, 15 * s)
    out += head('adek', sh[0] + 6 * s, sh[1] - 64 * s, s, 'senang')
    return out
b = (floor(F - 10, H) + runner_ayah(230) + runner_adek(640) + sweat(170, 60, 1.1) + sweat(140, 100, 0.8) +
     path(f'M450 {F-200} l60 0 M440 {F-150} l80 0 M460 {F-100} l50 0', LINE, 10) + spark(800, 120, 18))
save('big-w4le-kejar', H, b)


autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 440, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
