# Design v2 scenes for the week-3 noon "Contekan" posts, group B (w3n-ruam-popok, w3n-kepala-peyang, w3n-cegukan, w3n-air-putih).
# Run: python tools/mkart_w3_noonB.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

MINT = '#e3eee6'   # sage tint
RASH = '#e8957c'   # soft red dots for the rash
NAMES = []


def out(name, h, body):
    svg(name, h, body)
    NAMES.append(name)


# ---------------- helpers (copied from mkart_w2_noon so that script is not re-run)
def rect(x, y, w, h, f, rx=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'


def check(cx, cy, r=30):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SD}"/>'
            f'<path d="M{cx-r*0.47} {cy} L{cx-r*0.13} {cy+r*0.33} L{cx+r*0.47} {cy-r*0.33}" stroke="#fff" stroke-width="{r*0.28:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=30):
    k = r * 0.38
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TERRA}"/>'
            f'<path d="M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}" stroke="#fff" stroke-width="{r*0.28:.0f}" stroke-linecap="round"/>')


def bubble(x, y, w, h, f, tail='left'):
    tx = x + w - 70 if tail == 'right' else x + 40
    d = 30 if tail == 'right' else -10
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(34, h/2)}" fill="{f}"/><path d="M{tx} {y+h-2} L{tx+d} {y+h+36} L{tx+46} {y+h-2} Z" fill="{f}"/>'


def tunas_lying(pose, w, h, cx, bottom, rot=-90):
    cy = bottom - 0.35 * w
    return f'<g transform="rotate({rot} {cx} {cy})">' + tunas(pose, w, h, cx - w / 2, cy - h / 2) + '</g>'


def crib(x, y, w, h):
    mat = y + h * 0.56
    back = rect(x, y - 16, 24, h + 16, BOXD, 10) + rect(x + w - 24, y - 16, 24, h + 16, BOXD, 10)
    for sx in range(int(x + 50), int(x + w - 40), 44):
        back += rect(sx, y + 10, 12, mat - y - 10, BOX, 6)
    back += rect(x, y, w, 22, BOX, 11)
    back += rect(x + 18, mat, w - 36, 34, CARD, 12, f'stroke="{LINE}" stroke-width="5"')
    front = rect(x, mat + 32, w, 22, BOXD, 11)
    return back, front, mat


def diaper(cx, cy, w, rash=False):
    h = w * 0.7
    s = f'<path d="M{cx-w/2} {cy-h/2} L{cx+w/2} {cy-h/2} L{cx+w*0.42} {cy} Q{cx+w*0.2} {cy+h*0.55} {cx} {cy+h*0.55} Q{cx-w*0.2} {cy+h*0.55} {cx-w*0.42} {cy} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    s += rect(cx - w / 2 - 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8) + rect(cx + w / 2 - w * 0.22 + 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8)
    s += f'<path d="M{cx-w*0.3} {cy-h*0.12} Q{cx} {cy+h*0.05} {cx+w*0.3} {cy-h*0.12}" stroke="{LINE}" stroke-width="5" fill="none"/>'
    if rash:
        for dx, dy in ((-0.12, 0.12), (0.0, 0.2), (0.12, 0.1), (-0.05, 0.32), (0.08, 0.3)):
            s += f'<circle cx="{cx+w*dx}" cy="{cy+h*dy}" r="{w*0.028}" fill="{RASH}"/>'
    return s


def drop(cx, cy, s, col=SKY):
    return f'<path d="M{cx} {cy-s} Q{cx+s*0.75} {cy-s*0.05} {cx+s*0.62} {cy+s*0.35} Q{cx+s*0.45} {cy+s*0.8} {cx} {cy+s*0.8} Q{cx-s*0.45} {cy+s*0.8} {cx-s*0.62} {cy+s*0.35} Q{cx-s*0.75} {cy-s*0.05} {cx} {cy-s} Z" fill="{col}"/>'


def clock(cx, cy, r, hour, minute=0, label=None):
    import math
    s = f'<circle cx="{cx}" cy="{cy}" r="{r+8}" fill="{TERRA}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}"/>'
    for k in range(12):
        a = k * math.pi / 6
        s += f'<circle cx="{cx+r*0.78*math.sin(a):.1f}" cy="{cy-r*0.78*math.cos(a):.1f}" r="{r*0.06:.1f}" fill="{LINE}"/>'
    ah = (hour % 12 + minute / 60) * math.pi / 6
    am = minute * math.pi / 30
    s += f'<path d="M{cx} {cy} L{cx+r*0.48*math.sin(ah):.1f} {cy-r*0.48*math.cos(ah):.1f}" stroke="{INK}" stroke-width="{r*0.13:.0f}" stroke-linecap="round"/>'
    s += f'<path d="M{cx} {cy} L{cx+r*0.7*math.sin(am):.1f} {cy-r*0.7*math.cos(am):.1f}" stroke="{INK}" stroke-width="{r*0.09:.0f}" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.1:.1f}" fill="{TERRA}"/>'
    if label:
        s += text(cx, cy + r * 0.2, label, r * 0.62, TD)
    return s


def fl(y, H, x0, x1):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{H-y}" rx="24" fill="{FLOOR}"/>'


def sparkle(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'


def rug(cx, cy, rx, ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{MINT}"/><ellipse cx="{cx}" cy="{cy}" rx="{rx-22}" ry="{ry-12}" fill="none" stroke="{SAGE}" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round"/>'


def waves(x, y, s, col, n=3, flip=False):
    sg = -1 if flip else 1
    return ''.join(f'<path d="M{x+sg*(20+k*s*0.45)} {y-s*(0.35+k*0.22)} Q{x+sg*(44+k*s*0.6)} {y} {x+sg*(20+k*s*0.45)} {y+s*(0.35+k*0.22)}" stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round"/>' for k in range(n))


def spoon(x, y, L, rot, food=SUN):
    s = f'<g transform="rotate({rot} {x} {y})">' + rect(x, y - L * 0.05, L * 0.75, L * 0.1, '#c8c2b8', L * 0.05)
    s += f'<ellipse cx="{x+L*0.82}" cy="{y}" rx="{L*0.18}" ry="{L*0.12}" fill="#d8d2c8"/>'
    if food:
        s += f'<ellipse cx="{x+L*0.83}" cy="{y-L*0.03}" rx="{L*0.13}" ry="{L*0.08}" fill="{food}"/>'
    return s + '</g>'


# ---------------- new helpers
def breeze(x, y, L, col=SKYD, n=3):
    """Horizontal air lines with curled ends (moving air)."""
    s = ''
    for k in range(n):
        yy = y + k * 34
        ll = L * (1 - 0.18 * (k % 2))
        s += (f'<path d="M{x} {yy} L{x+ll} {yy} Q{x+ll+26} {yy} {x+ll+26} {yy-18} Q{x+ll+26} {yy-36} {x+ll+8} {yy-34}" '
              f'stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round" opacity="{0.9 - k*0.2:.1f}"/>')
    return s


def talc(x, y, w):
    """Powder bottle, top-left x,y; with a puff cloud coming out of the nozzle."""
    h = w * 1.5
    s = rect(x, y + h * 0.18, w, h * 0.82, CARD, w * 0.22, f'stroke="{LINE}" stroke-width="6"')
    s += rect(x + w * 0.12, y + h * 0.04, w * 0.76, h * 0.2, SKY, w * 0.1) + rect(x + w * 0.32, y - h * 0.05, w * 0.36, h * 0.12, SKYD, w * 0.06)
    s += rect(x + w * 0.12, y + h * 0.42, w * 0.76, h * 0.3, BLUSH, 12)
    s += text(x + w / 2, y + h * 0.63, 'bedak', w * 0.24, TD)
    for dx, dy, r in ((0.2, -0.2, 0.13), (0.45, -0.3, 0.17), (0.75, -0.22, 0.12), (0.6, -0.42, 0.1)):
        s += f'<circle cx="{x+w*dx}" cy="{y+h*dy}" r="{w*r}" fill="#fff" stroke="{LINE}" stroke-width="4"/>'
    return s


def tube(x, y, L, rot=0, label='zinc'):
    """Ointment tube lying along +x from x,y (centre line), cap on the right."""
    h = L * 0.3
    s = f'<g transform="rotate({rot} {x} {y})">'
    s += f'<path d="M{x} {y-h*0.55} L{x+L*0.72} {y-h*0.5} Q{x+L*0.78} {y} {x+L*0.72} {y+h*0.5} L{x} {y+h*0.55} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    s += rect(x - L * 0.05, y - h * 0.6, L * 0.07, h * 1.2, SAGE, 6)
    s += rect(x + L * 0.12, y - h * 0.32, L * 0.5, h * 0.64, SAGE, 12)
    s += text(x + L * 0.37, y + h * 0.18, label, h * 0.48, '#fff')
    s += rect(x + L * 0.76, y - h * 0.22, L * 0.2, h * 0.44, SD, 10)
    return s + '</g>'


def dollop(cx, cy, s):
    return (f'<path d="M{cx-s} {cy} Q{cx-s} {cy-s*0.6} {cx-s*0.3} {cy-s*0.62} Q{cx-s*0.2} {cy-s*1.2} {cx+s*0.15} {cy-s*1.05} '
            f'Q{cx+s*0.25} {cy-s*0.7} {cx+s*0.6} {cy-s*0.6} Q{cx+s} {cy-s*0.5} {cx+s} {cy} Z" fill="#fff" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>')


def shield(cx, cy, s, col=SAGE):
    return (f'<path d="M{cx} {cy-s} Q{cx+s*0.5} {cy-s*0.75} {cx+s*0.85} {cy-s*0.78} Q{cx+s*0.9} {cy+s*0.3} {cx} {cy+s} '
            f'Q{cx-s*0.9} {cy+s*0.3} {cx-s*0.85} {cy-s*0.78} Q{cx-s*0.5} {cy-s*0.75} {cx} {cy-s} Z" fill="{col}"/>'
            f'<path d="M{cx-s*0.38} {cy-s*0.02} L{cx-s*0.08} {cy+s*0.3} L{cx+s*0.42} {cy-s*0.32}" stroke="#fff" stroke-width="{s*0.18:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def basin(cx, top, w):
    h = w * 0.42
    s = shadow(cx, top + h + 8, w * 0.46)
    s += f'<path d="M{cx-w/2} {top} Q{cx-w*0.46} {top+h} {cx} {top+h} Q{cx+w*0.46} {top+h} {cx+w/2} {top} Z" fill="{SKYD}"/>'
    s += f'<ellipse cx="{cx}" cy="{top}" rx="{w/2}" ry="{w*0.11}" fill="{SKY}" stroke="{SKYD}" stroke-width="8"/>'
    s += f'<path d="M{cx-w*0.22} {top-2} q20 -10 40 0 q20 10 40 0" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.7"/>'
    return s


def cotton(cx, cy, r):
    return ''.join(f'<circle cx="{cx+dx*r}" cy="{cy+dy*r}" r="{r*rr}" fill="#fff" stroke="{LINE}" stroke-width="4"/>'
                   for dx, dy, rr in ((-0.5, 0.1, 0.6), (0.5, 0.1, 0.6), (0, -0.25, 0.7)))


def sun(cx, cy, r):
    import math
    s = ''.join(f'<path d="M{cx+math.cos(a)*r*1.3:.1f} {cy+math.sin(a)*r*1.3:.1f} L{cx+math.cos(a)*r*1.65:.1f} {cy+math.sin(a)*r*1.65:.1f}" stroke="{SUND}" stroke-width="{r*0.16:.0f}" stroke-linecap="round"/>'
                for a in [k * math.pi / 4 for k in range(8)])
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>'


def glass(x, y, w, h, level=0.6, col=SKY):
    """Small open cup, top-left x,y, with water to `level`."""
    s = f'<path d="M{x} {y} L{x+w} {y} L{x+w*0.86} {y+h} Q{x+w/2} {y+h+8} {x+w*0.14} {y+h} Z" fill="#fff" stroke="{SKYD}" stroke-width="7" stroke-linejoin="round"/>'
    wy = y + h * (1 - level)
    k = (wy - y) / h * 0.14
    s += f'<path d="M{x+w*k+5} {wy} L{x+w*(1-k)-5} {wy} L{x+w*0.86-4} {y+h-4} Q{x+w/2} {y+h+3} {x+w*0.14+4} {y+h-4} Z" fill="{col}"/>'
    s += rect(x + w * 0.66, y + h * 0.12, w * 0.1, h * 0.55, '#fff', 5, 'opacity="0.55"')
    return s


def pause_icon(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SAGE}"/>' + rect(cx - r * 0.38, cy - r * 0.42, r * 0.24, r * 0.84, '#fff', r * 0.08)
            + rect(cx + r * 0.14, cy - r * 0.42, r * 0.24, r * 0.84, '#fff', r * 0.08))


def hik(x, y, s, rot=-10):
    return text(x, y, 'hik!', s, TD, rot=rot)


def spool(cx, cy, s):
    return (rect(cx - s * 0.55, cy - s * 0.7, s * 1.1, s * 0.18, BOX, 6) + rect(cx - s * 0.55, cy + s * 0.52, s * 1.1, s * 0.18, BOX, 6)
            + rect(cx - s * 0.42, cy - s * 0.52, s * 0.84, s * 1.04, TERRA, 8)
            + ''.join(f'<path d="M{cx-s*0.42} {cy-s*0.36+k*s*0.2} L{cx+s*0.42} {cy-s*0.3+k*s*0.2}" stroke="{TD}" stroke-width="4"/>' for k in range(5))
            + f'<path d="M{cx+s*0.42} {cy+s*0.2} Q{cx+s*0.9} {cy+s*0.3} {cx+s*0.8} {cy+s*0.75} Q{cx+s*0.7} {cy+s*1.1} {cx+s*1.1} {cy+s*1.0}" stroke="{TERRA}" stroke-width="6" fill="none" stroke-linecap="round"/>')


def dor(x, y, w, h):
    """Spiky 'DOR!' burst used for startling."""
    import math
    cx, cy = x + w / 2, y + h / 2
    pts = []
    for k in range(18):
        a = k * math.pi / 9
        r = 1.0 if k % 2 == 0 else 0.74
        pts.append(f'{cx+math.cos(a)*w/2*r:.1f} {cy+math.sin(a)*h/2*r:.1f}')
    return f'<path d="M{" L".join(pts)} Z" fill="{SUN}"/>' + text(cx, cy + h * 0.13, 'DOR!', h * 0.34, TD)


def hpillow(cx, cy, w):
    """Head-shaping pillow: a soft pillow with a round dip in the middle."""
    h = w * 0.5
    s = f'<path d="M{cx-w/2} {cy-h/2} Q{cx} {cy-h/2+12} {cx+w/2} {cy-h/2} Q{cx+w/2-12} {cy} {cx+w/2} {cy+h/2} Q{cx} {cy+h/2-12} {cx-w/2} {cy+h/2} Q{cx-w/2+12} {cy} {cx-w/2} {cy-h/2} Z" fill="{BLUSH}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{w*0.22}" ry="{h*0.28}" fill="{TERRA}" opacity="0.35"/><ellipse cx="{cx}" cy="{cy+4}" rx="{w*0.15}" ry="{h*0.18}" fill="{TERRA}" opacity="0.3"/>'
    return s


def swap_arrows(cx, cy, w, col=SD):
    return (f'<path d="M{cx-w/2} {cy} Q{cx} {cy-w*0.4} {cx+w/2} {cy}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx+w/2-30} {cy-14} L{cx+w/2} {cy} L{cx+w/2-6} {cy-32}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{cx+w/2} {cy+40} Q{cx} {cy+w*0.4+40} {cx-w/2} {cy+40}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx-w/2+30} {cy+54} L{cx-w/2} {cy+40} L{cx-w/2+6} {cy+72}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def bouncer(x, y, w):
    """Baby bouncer seat, side view; x,y = top-left of the seat back; returns (back, front)."""
    back = f'<path d="M{x} {y} Q{x+w*0.12} {y+w*0.5} {x+w*0.45} {y+w*0.62} L{x+w} {y+w*0.5} L{x+w*0.98} {y+w*0.62} L{x+w*0.4} {y+w*0.76} Q{x-w*0.06} {y+w*0.6} {x-w*0.08} {y+w*0.02} Z" fill="{SKY}"/>'
    front = (f'<path d="M{x+w*0.05} {y+w*0.75} Q{x+w*0.5} {y+w*0.95} {x+w*1.05} {y+w*0.7}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.55"/>'
             f'<path d="M{x+w*0.2} {y+w*0.78} L{x+w*0.12} {y+w*0.96} M{x+w*0.85} {y+w*0.74} L{x+w*0.95} {y+w*0.96}" stroke="{INK}" stroke-width="10" stroke-linecap="round" opacity="0.55"/>')
    return back, front


def jug(x, y, w, h, level):
    s = rect(x, y, w, h, '#fff', 20, f'stroke="{SKYD}" stroke-width="8"')
    wy = y + h * (1 - level)
    s += rect(x + 8, wy, w - 16, y + h - wy - 8, SKY, 14)
    s += f'<path d="M{x+w} {y+h*0.2} Q{x+w+60} {y+h*0.25} {x+w+50} {y+h*0.55} Q{x+w+40} {y+h*0.75} {x+w} {y+h*0.75}" stroke="{SKYD}" stroke-width="12" fill="none"/>'
    s += f'<path d="M{x} {y+8} L{x-26} {y-14}" stroke="{SKYD}" stroke-width="10" stroke-linecap="round"/>'
    for k in range(4):
        ty = y + h * (0.2 + k * 0.18)
        s += f'<path d="M{x+16} {ty} L{x+48} {ty}" stroke="{SKYD}" stroke-width="6" stroke-linecap="round"/>'
    return s


# =====================================================================
# 1. w3n-ruam-popok: powder out, water + air + zinc in
b = (floor(330, 420) +
     shadow(160, 400, 80) + talc(95, 150, 130) + cross(235, 150, 40) +
     shadow(440, 405, 110) + tunas('santai', 190, 222, 345, 140) + diaper(440, 368, 118, rash=True) +
     tube(575, 330, 210, -18) + dollop(820, 365, 34) + drop(640, 165, 34) + breeze(690, 120, 110, SKYD, 2) + check(800, 230, 40))
out('hero-w3n-ruam-popok', 420, b)

b = diaper(190, 220, 280, rash=True) + clock(560, 220, 120, 4, 0) + text(560, 410, 'maks 4 jam', 54, TD)
out('big-w3n-ruam-ganti', 440, b)

b = (basin(260, 220, 360) + drop(150, 110, 34) + drop(230, 70, 26) + drop(330, 105, 30) +
     shadow(620, 395, 110) + cotton(620, 340, 70) + cotton(720, 360, 50))
out('big-w3n-ruam-air', 440, b)

b = (fl(330, 420, 60, 640) + f'<rect x="80" y="300" width="400" height="44" rx="22" fill="{MINT}"/>' +
     tunas_lying('santai', 230, 268, 290, 312) + breeze(440, 110, 120, SKYD, 3) + sun(560, 270, 34))
out('big-w3n-ruam-angin', 420, b)

b = tube(70, 260, 440, -12) + dollop(620, 300, 70) + shield(760, 210, 90)
out('big-w3n-ruam-salep', 420, b)

# =====================================================================
# 2. w3n-kepala-peyang: back to sleep stays, the special pillow goes
cb, cf, cm = crib(60, 150, 440, 250)
b = (floor(360, 420) + cb + tunas_lying('ngantuk', 170, 198, 280, cm + 4) + cf + text(420, 110, 'z', 54, MUTED) + text(455, 80, 'z', 40, MUTED) +
     check(110, 90, 40) + shadow(700, 380, 120) + hpillow(700, 310, 230) + cross(800, 210, 44) + text(700, 160, 'bantal peyang', 40, TD))
out('hero-w3n-kepala-peyang', 420, b)

cb, cf, cm = crib(120, 140, 420, 280)
b = fl(380, 440, 80, 840) + cb + tunas_lying('ngantuk', 140, 163, 330, cm + 4) + cf + check(670, 150, 50) + text(580, 330, 'telentang', 58, SD, anchor='start')
out('big-w3n-peyang-telentang', 440, b)

ball = f'<circle cx="590" cy="330" r="56" fill="{SUN}"/><path d="M534 330 Q590 300 646 330 M590 274 Q565 330 590 386" stroke="{TERRA}" stroke-width="10" fill="none"/>'
b = (fl(330, 420, 60, 700) + tunas('hore', 260, 303, 120, 60) +
     f'<rect x="70" y="290" width="400" height="80" rx="40" fill="{MINT}"/><path d="M110 330 L430 330" stroke="{SAGE}" stroke-width="6" stroke-dasharray="2 16" stroke-linecap="round"/>' +
     ball + sun(620, 120, 40))
out('big-w3n-peyang-tummy', 420, b)

cb, cf, cm = crib(60, 170, 480, 240)
b = (fl(380, 440, 30, 840) + cb + tunas_lying('ngantuk', 120, 140, 200, cm + 4) +
     f'<circle cx="440" cy="{cm-48}" r="50" fill="none" stroke="{SAGE}" stroke-width="7" stroke-dasharray="4 16" stroke-linecap="round"/>' + cf +
     swap_arrows(320, 90, 250) + text(700, 300, 'gantian', 62, SD))
out('big-w3n-peyang-arah', 440, b)

bk, bf = bouncer(110, 120, 300)
b = (fl(360, 420, 60, 820) + shadow(270, 405, 170) + bk + tunas('santai', 150, 175, 170, 160) + bf +
     clock(620, 200, 90, 0, 15) + text(620, 360, 'sebentar', 52, TD))
out('big-w3n-peyang-duduk', 420, b)

# =====================================================================
# 3. w3n-cegukan: hiccups stop on their own, no startling needed
b = (floor(330, 420) + shadow(260, 400, 120) + tunas('kaget', 220, 257, 150, 140) +
     hik(120, 130, 56, -14) + hik(420, 100, 48, 10) + hik(450, 200, 38, 8) +
     dor(560, 120, 220, 170) + cross(790, 110, 44) + clock(690, 335, 50, 0, 5) + check(770, 300, 26))
out('hero-w3n-cegukan', 420, b)

b = (fl(330, 420, 40, 640) + shadow(200, 395, 120) + tunas('kaget', 240, 280, 80, 110) + hik(400, 110, 60, 10) + pause_icon(530, 250, 95))
out('big-w3n-cegukan-jeda', 420, b)

pat = ''.join(f'<path d="M{x} {y} q18 -24 0 -48" stroke="{TERRA}" stroke-width="9" fill="none" stroke-linecap="round" opacity="{o}"/>' for x, y, o in ((410, 280, 1), (440, 292, 0.7), (470, 304, 0.45)))
b = (fl(330, 420, 40, 640) + shadow(260, 395, 130) + tunas('halo', 260, 303, 130, 90) + pat +
     f'<path d="M90 330 L90 170 M60 200 L90 160 L120 200" stroke="{SD}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' +
     text(520, 200, 'puk puk', 60, TD))
out('big-w3n-cegukan-sendawa', 420, b)

b = (fl(330, 420, 40, 660) + shadow(220, 395, 130) + tunas('sayang', 250, 292, 95, 100) + clock(520, 220, 95, 9, 0) + check(610, 130, 40))
out('big-w3n-cegukan-tenang', 420, b)

b = dor(60, 90, 330, 250) + cross(370, 100, 46) + spool(640, 200, 160) + cross(800, 100, 46)
out('big-w3n-cegukan-mitos', 420, b)

# =====================================================================
# 4. w3n-air-putih: under 6 months, breast milk is the water
b = (floor(330, 420) + sun(130, 130, 56) +
     shadow(400, 400, 120) + tunas('sayang', 220, 257, 290, 140) + sparkle(540, 140, 20) +
     shadow(700, 400, 60) + glass(640, 220, 120, 170, 0.6) + cross(790, 190, 44) +
     rect(600, 80, 200, 64, MINT, 32) + text(700, 126, '0-6 bln', 40, SD))
out('hero-w3n-air-putih', 420, b)

ASI = '#fbf4ea'
dclip = '<defs><clipPath id="asid"><path d="M260 40 Q410 200 384 280 Q350 370 260 370 Q170 370 136 280 Q110 200 260 40 Z"/></clipPath></defs>'
b = (dclip + '<path d="M260 40 Q410 200 384 280 Q350 370 260 370 Q170 370 136 280 Q110 200 260 40 Z" fill="' + ASI + '"/>' +
     f'<g clip-path="url(#asid)"><rect x="100" y="110" width="320" height="270" fill="{SKY}" opacity="0.55"/></g>' +
     f'<path d="M260 40 Q410 200 384 280 Q350 370 260 370 Q170 370 136 280 Q110 200 260 40 Z" fill="none" stroke="{LINE}" stroke-width="8"/>' +
     text(260, 290, '90%', 80, SKYD) + text(560, 210, 'isinya', 46, MUTED, anchor='start') + text(560, 280, 'air', 80, SKYD, anchor='start') + check(700, 110, 44))
out('big-w3n-air-asi', 420, b)

b = (fl(330, 420, 40, 820) + sun(110, 110, 50) + shadow(340, 395, 120) + tunas('sayang', 230, 268, 225, 125) +
     bubble(500, 60, 300, 110, BLUSH, 'left') + text(650, 135, 'nyusu lagi', 50, TD))
out('big-w3n-air-haus', 420, b)

b = (fl(330, 420, 40, 820) + shadow(250, 395, 120) + bowl(250, 270, 240, TERRA, TD) + spoon(70, 260, 160, -20) +
     shadow(590, 395, 70) + glass(530, 200, 130, 180, 0.35) + text(740, 160, '6 bln+', 50, SD))
out('big-w3n-air-gelas', 420, b)

b = jug(110, 90, 230, 290, 0.5) + text(470, 220, '120-240', 76, SKYD, anchor='start') + text(470, 300, 'ml sehari', 52, MUTED, anchor='start')
out('big-w3n-air-takaran', 420, b)

autocrop(NAMES)
print('\n'.join(NAMES))
