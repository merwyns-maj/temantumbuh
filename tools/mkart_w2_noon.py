# Design v2 scenes for the week-2 noon "Contekan Cepat" posts (w2n-*). Run: python tools/mkart_w2_noon.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

NIGHT = SKYD       # window sky at night
GUM = '#eab5a1'    # Tunas skin shade, used for gums
MINT = '#e3eee6'   # sage tint
NAMES = []


def out(name, h, body):
    svg(name, h, body)
    NAMES.append(name)


# ---------------- helpers
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


def tunas_lying(pose, w, h, cx, bottom):
    """Tunas on its back, head to the left (side view of a baby lying down), resting on y = bottom."""
    cy = bottom - 0.35 * w  # the visible body starts 15% in from the image edge
    return f'<g transform="rotate(-90 {cx} {cy})">' + tunas(pose, w, h, cx - w / 2, cy - h / 2) + '</g>'


def window(x, y, w, h, stars=True):
    s = rect(x - 12, y - 12, w + 24, h + 24, BOX, 18) + rect(x, y, w, h, NIGHT, 10)
    s += f'<circle cx="{x+w*0.68}" cy="{y+h*0.38}" r="{h*0.2}" fill="{SUN}"/><circle cx="{x+w*0.76}" cy="{y+h*0.31}" r="{h*0.18}" fill="{NIGHT}"/>'
    if stars:
        for sx, sy in ((0.2, 0.25), (0.35, 0.65), (0.2, 0.8), (0.85, 0.78)):
            s += f'<circle cx="{x+w*sx}" cy="{y+h*sy}" r="5" fill="#fff" opacity="0.85"/>'
    s += rect(x + w / 2 - 6, y, 12, h, BOX) + rect(x, y + h / 2 - 6, w, 12, BOX)
    return s


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


def book(cx, cy, w):
    h = w * 0.42
    s = f'<path d="M{cx-w/2-10} {cy-h/2+14} L{cx} {cy-h/2+30} L{cx+w/2+10} {cy-h/2+14} L{cx+w/2+10} {cy+h/2+16} L{cx} {cy+h/2+30} L{cx-w/2-10} {cy+h/2+16} Z" fill="{TERRA}"/>'
    s += f'<path d="M{cx} {cy-h/2+16} Q{cx-w*0.25} {cy-h/2-10} {cx-w/2} {cy-h/2} L{cx-w/2} {cy+h/2} Q{cx-w*0.25} {cy+h/2-10} {cx} {cy+h/2+16} Z" fill="{CARD}" stroke="{LINE}" stroke-width="4"/>'
    s += f'<path d="M{cx} {cy-h/2+16} Q{cx+w*0.25} {cy-h/2-10} {cx+w/2} {cy-h/2} L{cx+w/2} {cy+h/2} Q{cx+w*0.25} {cy+h/2-10} {cx} {cy+h/2+16} Z" fill="{CARD}" stroke="{LINE}" stroke-width="4"/>'
    # left page: a sun over a hill; right page: a big ball
    s += f'<circle cx="{cx-w*0.3}" cy="{cy-h*0.12}" r="{w*0.07}" fill="{SUN}"/>'
    s += f'<path d="M{cx-w*0.46} {cy+h*0.32} Q{cx-w*0.25} {cy-h*0.05} {cx-w*0.05} {cy+h*0.34} Z" fill="{SAGE}"/>'
    s += f'<circle cx="{cx+w*0.25}" cy="{cy+h*0.05}" r="{w*0.11}" fill="{SKY}"/><path d="M{cx+w*0.14} {cy+h*0.05} L{cx+w*0.36} {cy+h*0.05}" stroke="#fff" stroke-width="6"/>'
    return s


def note(x, y, s, col):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{s*0.55}" ry="{s*0.42}" fill="{col}" transform="rotate(-20 {x} {y})"/>'
            f'<rect x="{x+s*0.38}" y="{y-s*2}" width="{s*0.22}" height="{s*2}" fill="{col}"/>'
            f'<path d="M{x+s*0.6} {y-s*2} Q{x+s*1.4} {y-s*1.6} {x+s*1.1} {y-s*0.9}" stroke="{col}" stroke-width="{s*0.22}" fill="none" stroke-linecap="round"/>')


def thermo(x, y, h, level, label=None, col=TERRA):
    """Standing thermometer, top-left at x,y; level 0..1 of the tube filled."""
    w = h * 0.22
    r = w * 0.95
    s = rect(x, y, w, h, CARD, w / 2, f'stroke="{INK}" stroke-width="6"')
    s += f'<circle cx="{x+w/2}" cy="{y+h}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="6"/>'
    fh = (h - w * 0.6) * level
    s += rect(x + w * 0.3, y + h - fh, w * 0.4, fh + 4, col, w * 0.2)
    s += f'<circle cx="{x+w/2}" cy="{y+h}" r="{r-3}" fill="{col}"/>'
    for k in range(4):
        ty = y + w * 0.7 + k * (h - w) / 4
        s += f'<path d="M{x+w*0.72} {ty} L{x+w*0.92} {ty}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    if label:
        s += text(x + w + 18, y + h * 0.35, label, h * 0.26, TD, anchor='start')
    return s


def tooth(cx, cy, s, shine=True):
    w, h = s, s * 1.1
    d = (f'M{cx-w*0.5} {cy-h*0.25} Q{cx-w*0.5} {cy-h*0.5} {cx-w*0.25} {cy-h*0.5} Q{cx-w*0.1} {cy-h*0.5} {cx} {cy-h*0.42} '
         f'Q{cx+w*0.1} {cy-h*0.5} {cx+w*0.25} {cy-h*0.5} Q{cx+w*0.5} {cy-h*0.5} {cx+w*0.5} {cy-h*0.25} '
         f'Q{cx+w*0.5} {cy+h*0.05} {cx+w*0.36} {cy+h*0.2} L{cx+w*0.3} {cy+h*0.46} Q{cx+w*0.24} {cy+h*0.55} {cx+w*0.16} {cy+h*0.42} '
         f'L{cx+w*0.06} {cy+h*0.16} Q{cx} {cy+h*0.08} {cx-w*0.06} {cy+h*0.16} L{cx-w*0.16} {cy+h*0.42} '
         f'Q{cx-w*0.24} {cy+h*0.55} {cx-w*0.3} {cy+h*0.46} L{cx-w*0.36} {cy+h*0.2} Q{cx-w*0.5} {cy+h*0.05} {cx-w*0.5} {cy-h*0.25} Z')
    out_ = f'<path d="{d}" fill="#fff" stroke="{LINE}" stroke-width="{max(4, s*0.05):.0f}" stroke-linejoin="round"/>'
    if shine:
        out_ += f'<path d="M{cx-w*0.32} {cy-h*0.2} Q{cx-w*0.3} {cy-h*0.36} {cx-w*0.16} {cy-h*0.38}" stroke="{SKY}" stroke-width="{s*0.07:.0f}" fill="none" stroke-linecap="round"/>'
    return out_


def sparkle(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'


def brush(x, y, L, rot=0, dab=True):
    s = f'<g transform="rotate({rot} {x} {y})">'
    s += rect(x, y, L * 0.7, L * 0.09, SAGE, L * 0.045) + rect(x, y + L * 0.05, L * 0.7, L * 0.04, SD, L * 0.02)
    s += rect(x + L * 0.66, y - L * 0.01, L * 0.34, L * 0.11, SAGE, L * 0.04)
    for k in range(6):
        s += rect(x + L * 0.7 + k * L * 0.05, y - L * 0.12, L * 0.03, L * 0.12, SKY, L * 0.012)
    if dab:
        s += f'<ellipse cx="{x+L*0.84}" cy="{y-L*0.14}" rx="{L*0.03}" ry="{L*0.022}" fill="#fff" stroke="{SKYD}" stroke-width="3"/>'
    return s + '</g>'


def grain(cx, cy, s):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{s}" ry="{s*0.5}" fill="#fff" stroke="{MUTED}" stroke-width="4" transform="rotate(-25 {cx} {cy})"/>'


def calendar(x, y, w, big, small=None):
    h = w * 0.9
    s = rect(x, y, w, h, CARD, 18, f'stroke="{LINE}" stroke-width="6"') + rect(x, y, w, h * 0.26, TERRA, 18) + rect(x, y + h * 0.16, w, h * 0.1, TERRA)
    s += rect(x + w * 0.25, y - 14, 14, 34, INK, 7) + rect(x + w * 0.7, y - 14, 14, 34, INK, 7)
    s += text(x + w / 2, y + h * (0.66 if small else 0.78), big, w * 0.34, INK)
    if small:
        s += text(x + w / 2, y + h * 0.88, small, w * 0.17, MUTED)
    return s


def spoon(x, y, L, rot, food=SUN):
    s = f'<g transform="rotate({rot} {x} {y})">' + rect(x, y - L * 0.05, L * 0.75, L * 0.1, '#c8c2b8', L * 0.05)
    s += f'<ellipse cx="{x+L*0.82}" cy="{y}" rx="{L*0.18}" ry="{L*0.12}" fill="#d8d2c8"/>'
    if food:
        s += f'<ellipse cx="{x+L*0.83}" cy="{y-L*0.03}" rx="{L*0.13}" ry="{L*0.08}" fill="{food}"/>'
    return s + '</g>'


def diaper(cx, cy, w, dry=False):
    h = w * 0.7
    s = f'<path d="M{cx-w/2} {cy-h/2} L{cx+w/2} {cy-h/2} L{cx+w*0.42} {cy} Q{cx+w*0.2} {cy+h*0.55} {cx} {cy+h*0.55} Q{cx-w*0.2} {cy+h*0.55} {cx-w*0.42} {cy} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    s += rect(cx - w / 2 - 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8) + rect(cx + w / 2 - w * 0.22 + 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8)
    s += f'<path d="M{cx-w*0.3} {cy-h*0.12} Q{cx} {cy+h*0.05} {cx+w*0.3} {cy-h*0.12}" stroke="{LINE}" stroke-width="5" fill="none"/>'
    return s


def drop(cx, cy, s, col=SKY):
    return f'<path d="M{cx} {cy-s} Q{cx+s*0.75} {cy-s*0.05} {cx+s*0.62} {cy+s*0.35} Q{cx+s*0.45} {cy+s*0.8} {cx} {cy+s*0.8} Q{cx-s*0.45} {cy+s*0.8} {cx-s*0.62} {cy+s*0.35} Q{cx-s*0.75} {cy-s*0.05} {cx} {cy-s} Z" fill="{col}"/>'


def crib(x, y, w, h):
    """Side view; y = top rail, y + h = floor. Returns (back, front, mattress_top)."""
    mat = y + h * 0.56
    back = rect(x, y - 16, 24, h + 16, BOXD, 10) + rect(x + w - 24, y - 16, 24, h + 16, BOXD, 10)
    for sx in range(int(x + 50), int(x + w - 40), 44):
        back += rect(sx, y + 10, 12, mat - y - 10, BOX, 6)
    back += rect(x, y, w, 22, BOX, 11)
    back += rect(x + 18, mat, w - 36, 34, CARD, 12, f'stroke="{LINE}" stroke-width="5"')
    front = rect(x, mat + 32, w, 22, BOXD, 11)
    return back, front, mat


def bed(x, y, w, h):
    """Grown-up bed, side view; y = mattress top, y + h = floor."""
    s = rect(x - 10, y - 110, 34, h + 110, BOXD, 12)  # headboard
    s += rect(x + w - 26, y + 10, 26, h - 10, BOXD, 10)
    s += rect(x, y, w, 60, CARD, 18, f'stroke="{LINE}" stroke-width="5"') + rect(x, y + 50, w, 30, BOX, 12)
    s += f'<ellipse cx="{x+80}" cy="{y-8}" rx="62" ry="24" fill="#fff" stroke="{LINE}" stroke-width="5"/>'
    s += f'<path d="M{x+170} {y-6} Q{x+w*0.6} {y-34} {x+w-10} {y-4} L{x+w-10} {y+30} L{x+170} {y+30} Z" fill="{BLUSH}"/>'
    return s


def pillow(cx, cy, w, f='#fff'):
    h = w * 0.55
    return f'<path d="M{cx-w/2} {cy-h/2} Q{cx} {cy-h/2+14} {cx+w/2} {cy-h/2} Q{cx+w/2-14} {cy} {cx+w/2} {cy+h/2} Q{cx} {cy+h/2-14} {cx-w/2} {cy+h/2} Q{cx-w/2+14} {cy} {cx-w/2} {cy-h/2} Z" fill="{f}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'


def plush(cx, cy, s):
    return (f'<ellipse cx="{cx-s*0.28}" cy="{cy-s*0.8}" rx="{s*0.16}" ry="{s*0.38}" fill="{SUN}"/><ellipse cx="{cx+s*0.28}" cy="{cy-s*0.8}" rx="{s*0.16}" ry="{s*0.38}" fill="{SUN}"/>'
            f'<circle cx="{cx}" cy="{cy-s*0.25}" r="{s*0.42}" fill="{SUN}"/><ellipse cx="{cx}" cy="{cy+s*0.4}" rx="{s*0.42}" ry="{s*0.36}" fill="{SUND}"/>'
            f'<circle cx="{cx-s*0.14}" cy="{cy-s*0.3}" r="{s*0.05}" fill="{INK}"/><circle cx="{cx+s*0.14}" cy="{cy-s*0.3}" r="{s*0.05}" fill="{INK}"/>')


def shirt(cx, cy, w, f):
    h = w * 0.85
    return (f'<path d="M{cx-w*0.22} {cy-h/2} Q{cx} {cy-h*0.36} {cx+w*0.22} {cy-h/2} L{cx+w/2} {cy-h*0.3} L{cx+w*0.38} {cy-h*0.08} L{cx+w*0.28} {cy-h*0.14} '
            f'L{cx+w*0.28} {cy+h/2} L{cx-w*0.28} {cy+h/2} L{cx-w*0.28} {cy-h*0.14} L{cx-w*0.38} {cy-h*0.08} L{cx-w/2} {cy-h*0.3} Z" fill="{f}" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>')


def beanie(cx, cy, w):
    return (f'<path d="M{cx-w/2} {cy} Q{cx-w/2} {cy-w*0.6} {cx} {cy-w*0.6} Q{cx+w/2} {cy-w*0.6} {cx+w/2} {cy} Z" fill="{TERRA}"/>'
            + rect(cx - w / 2 - 8, cy - 10, w + 16, w * 0.22, TD, 12) + f'<circle cx="{cx}" cy="{cy-w*0.64}" r="{w*0.12}" fill="{BLUSH}"/>')


def thick_blanket(cx, cy, w):
    h = w * 0.55
    s = rect(cx - w / 2, cy - h / 2, w, h, BLUSH, 22)
    for k in range(3):
        s += f'<path d="M{cx-w/2+20} {cy-h/2+20+k*h*0.3} Q{cx} {cy-h/2+40+k*h*0.3} {cx+w/2-20} {cy-h/2+20+k*h*0.3}" stroke="{TERRA}" stroke-width="6" fill="none" opacity="0.5"/>'
    return s


def waves(x, y, s, col, n=3, flip=False):
    sg = -1 if flip else 1
    return ''.join(f'<path d="M{x+sg*(20+k*s*0.45)} {y-s*(0.35+k*0.22)} Q{x+sg*(44+k*s*0.6)} {y} {x+sg*(20+k*s*0.45)} {y+s*(0.35+k*0.22)}" stroke="{col}" stroke-width="10" fill="none" stroke-linecap="round"/>' for k in range(n))


def breath(x, y, col=SKY):
    return (f'<path d="M{x} {y} q30 -16 56 0 q26 16 56 0" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x+20} {y+30} q26 -14 50 0 q22 14 46 0" stroke="{col}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.7"/>')


def rug(cx, cy, rx, ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{MINT}"/><ellipse cx="{cx}" cy="{cy}" rx="{rx-22}" ry="{ry-12}" fill="none" stroke="{SAGE}" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round"/>'


def shake(cx, cy, r):
    """Head-shake arcs on both sides of a face."""
    return (f'<path d="M{cx-r} {cy-30} Q{cx-r-26} {cy} {cx-r} {cy+30}" stroke="{TERRA}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx-r-30} {cy-46} Q{cx-r-64} {cy} {cx-r-30} {cy+46}" stroke="{TERRA}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.6"/>'
            f'<path d="M{cx+r} {cy-30} Q{cx+r+26} {cy} {cx+r} {cy+30}" stroke="{TERRA}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx+r+30} {cy-46} Q{cx+r+64} {cy} {cx+r+30} {cy+46}" stroke="{TERRA}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.6"/>')


CID = [0]


def mbowl(cx, top, w, level, food=SUN, bits_col=None, label=None, rice=False):
    """Front-view measuring bowl (cutaway) filled to `level` (0..1)."""
    CID[0] += 1
    cid = f'c{CID[0]}'
    h = w * 0.62
    d = f'M{cx-w/2} {top} L{cx+w/2} {top} Q{cx+w/2} {top+h} {cx} {top+h} Q{cx-w/2} {top+h} {cx-w/2} {top} Z'
    fy = top + h * (1 - level)
    s = f'<defs><clipPath id="{cid}"><path d="{d}"/></clipPath></defs>'
    s += shadow(cx, top + h + 14, w * 0.42)
    s += f'<path d="{d}" fill="{CARD}"/>'
    s += f'<g clip-path="url(#{cid})"><rect x="{cx-w/2}" y="{fy}" width="{w}" height="{h+10}" fill="{food}"/>'
    if rice:
        for k in range(16):
            gx = cx - w * 0.42 + (k * 37) % int(w * 0.84)
            gy = fy + 14 + (k * 23) % int(max(10, h * level - 20))
            s += f'<ellipse cx="{gx}" cy="{gy}" rx="7" ry="4" fill="#fff" opacity="0.9"/>'
    if bits_col:
        for k in range(9):
            bx = cx - w * 0.36 + (k * 53) % int(w * 0.72)
            by = fy + 16 + (k * 31) % int(max(10, h * level - 26))
            s += rect(bx, by, 16, 14, bits_col[k % len(bits_col)], 4)
    s += '</g>'
    s += f'<path d="{d}" fill="none" stroke="{BOXD}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<path d="M{cx-w/2-6} {top} L{cx+w/2+6} {top}" stroke="{BOXD}" stroke-width="10" stroke-linecap="round"/>'
    if label:
        s += text(cx, top + h * 0.62, label, w * 0.26, INK)
    return s


def fl(y, H, x0, x1):
    """Floor that only spans the scene (keeps small cheat-row arts compact)."""
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{H-y}" rx="24" fill="{FLOOR}"/>'


ring = f'<circle cx="0" cy="0" r="40" fill="none" stroke="{SAGE}" stroke-width="20"/>'

# =====================================================================
# 1. w2n-30-menit-malam: evening at home, clock at 8, reading on the rug
b = (floor(330, 420) + window(70, 40, 190, 150) + clock(780, 110, 62, 20, 0) +
     rug(440, 372, 340, 40) + shadow(260, 395, 100) + tunas('sayang', 190, 222, 160, 165) +
     shadow(620, 392, 70) + tunas('hore', 120, 140, 560, 245) + book(440, 352, 170) +
     rect(690, 196, 180, 60, MINT, 30) + text(780, 238, '30 menit', 38, SD))
out('hero-w2n-30-menit-malam', 420, b)

# mandi sambil ngobrol: Tunas in the tub, rubber duck, speech bubble
tub = (f'<path d="M140 250 L520 250 Q520 380 420 380 L240 380 Q140 380 140 250 Z" fill="{SKY}"/>'
       + rect(120, 236, 420, 30, CARD, 15, f'stroke="{SKYD}" stroke-width="6"') + rect(200, 376, 26, 34, SKYD, 8) + rect(434, 376, 26, 34, SKYD, 8))
foam = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{SKYD}" stroke-width="4"/>' for x, y, r in ((170, 232, 26), (205, 216, 30), (470, 226, 28), (505, 238, 20), (240, 236, 18)))
duck = (f'<ellipse cx="440" cy="222" rx="44" ry="28" fill="{SUN}"/><circle cx="470" cy="192" r="24" fill="{SUN}"/>'
        f'<path d="M490 190 L516 198 L490 206 Z" fill="{TERRA}"/><circle cx="474" cy="186" r="5" fill="{INK}"/>')
b = (fl(380, 440, 90, 800) + shadow(330, 418, 220) + tunas('hore', 170, 198, 245, 80) + tub + foam + duck +
     bubble(540, 50, 260, 120, MINT, 'left') + text(670, 132, 'bebek!', 62, SD))
out('big-w2n-mandi-ngobrol', 440, b)

# baca 1 buku: big open book, Tunas listening
b = (fl(300, 420, 60, 760) + shadow(300, 380, 230) + book(300, 290, 400) + shadow(640, 395, 90) + tunas('hore', 180, 210, 550, 185) +
     text(130, 110, '1 buku', 70, SD, anchor='start'))
out('big-w2n-baca-buku', 420, b)

# nyanyi lagu yang sama: big Tunas singing, notes drifting to sleepy little Tunas
b = (fl(320, 420, 60, 700) + shadow(200, 395, 110) + tunas('halo', 200, 233, 100, 160) + shadow(580, 395, 80) + tunas('ngantuk', 150, 175, 505, 222) +
     note(330, 160, 40, TERRA) + note(420, 105, 32, SAGE) + note(510, 150, 28, SUND))
out('big-w2n-nyanyi-lagu', 420, b)

# peluk dan cerita hari ini
b = (fl(330, 430, 60, 760) + shadow(290, 405, 190) + tunas('sayang', 220, 257, 120, 150) + tunas('hore', 150, 175, 320, 235) +
     bubble(430, 40, 320, 120, BLUSH, 'left') + text(590, 122, 'tadi siang...', 54, TD))
out('big-w2n-peluk-cerita', 430, b)

# =====================================================================
# 2. w2n-gigi-pertama: teething is not what makes the fever
b = (floor(330, 420) + shadow(150, 395, 100) + tunas('mikir', 180, 210, 60, 185) +
     f'<g transform="translate(232 356)">{ring}</g>' + drop(150, 345, 16) +
     tooth(380, 225, 150) + sparkle(460, 135, 22) + sparkle(300, 145, 14, TERRA) +
     text(530, 262, '≠', 120, TERRA) + shadow(640, 395, 60) + thermo(610, 80, 250, 0.75) + text(700, 200, '38°', 64, TD, anchor='start'))
out('hero-w2n-gigi-pertama', 420, b)

# gigi muncul 6-12 bulan: gum with two lower front teeth + calendar
gum = (f'<path d="M70 230 Q290 350 510 230 L510 330 Q290 450 70 330 Z" fill="{GUM}"/>'
       f'<path d="M70 230 Q290 350 510 230" stroke="{TD}" stroke-width="8" fill="none" opacity="0.35"/>')
teeth = (f'<path d="M222 300 Q218 214 252 210 Q286 214 282 300 Z" fill="#fff" stroke="{LINE}" stroke-width="6"/>'
         f'<path d="M298 300 Q294 214 328 210 Q362 214 358 300 Z" fill="#fff" stroke="{LINE}" stroke-width="6"/>')
b = gum + teeth + sparkle(400, 190, 26) + sparkle(180, 200, 16, TERRA) + calendar(590, 160, 240, '6-12', 'bulan')
out('big-w2n-gigi-muncul', 440, b)

# tanda tumbuh gigi: drool and chewing a teether ring (held low, face stays clear)
b = (fl(330, 420, 40, 660) + shadow(175, 395, 120) + tunas('mikir', 230, 268, 60, 130) +
     f'<g transform="translate(290 370)">{ring}</g>' + drop(175, 350, 18) + drop(187, 390, 12) +
     bubble(320, 30, 320, 110, MINT, 'left') + text(480, 105, 'gigit-gigit', 54, SD))
out('big-w2n-gigi-tanda', 420, b)

# sikat sejak gigi pertama: pasta sebutir beras (magnified)
b = (brush(40, 320, 500, -8) +
     f'<path d="M450 240 Q500 170 540 180" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="2 16" stroke-linecap="round"/>' +
     f'<path d="M790 300 L850 370" stroke="{BOXD}" stroke-width="30" stroke-linecap="round"/>' +
     f'<circle cx="690" cy="200" r="140" fill="{CARD}" stroke="{LINE}" stroke-width="10"/>' +
     f'<ellipse cx="625" cy="205" rx="48" ry="34" fill="#fff" stroke="{SKYD}" stroke-width="7"/>' + text(690, 225, '=', 64, MUTED) + grain(755, 205, 46))
out('big-w2n-gigi-sikat', 420, b)

# ke dokter gigi sebelum ulang tahun pertama
cake = (rect(140, 260, 300, 120, BLUSH, 20) + rect(140, 260, 300, 40, '#fff', 20) +
        f'<path d="M150 296 q25 22 50 0 q25 22 50 0 q25 22 50 0 q25 22 50 0 q25 22 50 0 q20 18 40 0" stroke="#fff" stroke-width="16" fill="none"/>' +
        rect(278, 160, 26, 100, SKY, 10) + f'<path d="M291 110 Q312 140 291 156 Q270 140 291 110 Z" fill="{SUN}"/>' + text(291, 360, '1', 72, TD))
b = (fl(380, 440, 90, 800) + shadow(290, 400, 190) + cake + tooth(630, 250, 200) + check(735, 140, 44))
out('big-w2n-gigi-dokter', 440, b)

# =====================================================================
# 3. w2n-tanda-kenyang
b = (floor(330, 420) + shadow(330, 395, 150) + chair(250, 170) + tunas('mikir', 150, 175, 255, 20) + shake(330, 90, 80) +
     bowl(200, 112, 110, TERRA, TD) + spoon(620, 100, 200, 180) +
     bubble(600, 170, 220, 96, BLUSH, 'left') + text(710, 236, 'udah!', 58, TD))
out('hero-w2n-tanda-kenyang', 420, b)

# buang muka dari sendok (compact scenes: they render ~300px wide in the cheat rows)
b = (fl(330, 420, 20, 600) + shadow(190, 395, 120) + tunas('mikir', 230, 268, 75, 128) + shake(190, 275, 120) +
     spoon(380, 330, 210, 0) +
     f'<path d="M520 270 Q490 210 440 225" stroke="{MUTED}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M448 198 L436 226 L464 238" stroke="{MUTED}" stroke-width="8" fill="none" stroke-linecap="round"/>')
out('big-w2n-kenyang-noleh', 420, b)

# mulut ditutup rapat
b = (fl(330, 420, 40, 580) + shadow(175, 395, 120) + tunas('mikir', 230, 268, 60, 128) + spoon(300, 330, 220, 0) +
     bubble(320, 40, 250, 110, BLUSH, 'left') + text(445, 116, 'mm-mm', 62, TD))
out('big-w2n-kenyang-mulut', 420, b)

# dorong piring
b = (fl(330, 420, 30, 640) + rect(30, 300, 560, 40, BOX, 16) + shadow(175, 300, 100) + tunas('halo', 230, 268, 60, 40) +
     bowl(400, 238, 170, TERRA, TD) + f'<path d="M505 236 L600 236 M515 270 L620 270 M525 304 L600 304" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/>')
out('big-w2n-kenyang-dorong', 420, b)

# kasih kode: suara atau gerakan tangan
b = (fl(330, 420, 40, 640) + shadow(175, 395, 120) + tunas('halo', 230, 268, 60, 128) +
     bubble(330, 40, 230, 110, BLUSH, 'left') + text(445, 118, 'udah', 66, TD) + note(590, 190, 28, SAGE) + note(640, 140, 22, SUND))
out('big-w2n-kenyang-kode', 420, b)

# =====================================================================
# 4. w2n-tidur-aman: own crib next to the grown-up bed
cb, cf, cm = crib(470, 150, 360, 250)
b = (floor(360, 420) + window(70, 30, 170, 120) + bed(40, 270, 360, 130) + cb +
     tunas_lying('ngantuk', 130, 152, 650, cm + 4) + cf + text(770, 110, 'z', 54, MUTED) + text(810, 80, 'z', 40, MUTED) + check(650, 80, 38))
out('hero-w2n-tidur-aman', 420, b)

cb, cf, cm = crib(120, 140, 420, 280)
b = fl(380, 440, 80, 840) + cb + tunas_lying('ngantuk', 140, 163, 330, cm + 4) + cf + check(670, 150, 50) + text(580, 330, 'telentang', 58, SD, anchor='start')
out('big-w2n-tidur-telentang', 440, b)

cb, cf, cm = crib(60, 140, 380, 280)
b = (fl(380, 440, 30, 860) + cb + cf + check(250, 240, 46) +
     pillow(570, 200, 150) + plush(750, 220, 100) + rect(510, 310, 310, 64, BLUSH, 32) + cross(830, 90, 40))
out('big-w2n-tidur-kosong', 440, b)

cb, cf, cm = crib(470, 150, 330, 250)
b = fl(360, 420, 30, 840) + bed(60, 270, 360, 130) + cb + tunas_lying('ngantuk', 120, 140, 635, cm + 4) + cf + check(440, 80, 44)
out('big-w2n-tidur-sekamar', 420, b)

b = (shirt(220, 230, 280, MINT) + check(340, 100, 46) +
     thick_blanket(630, 310, 240) + beanie(630, 185, 160) + cross(775, 90, 46))
out('big-w2n-tidur-gerah', 420, b)

# =====================================================================
# 5. w2n-nangis-malam: jam 2 pagi, the baby is safe in the crib, you breathe
cb, cf, cm = crib(80, 160, 330, 240)
tears = drop(212, cm - 40, 12) + drop(298, cm - 40, 12)
b = (floor(360, 420) + window(650, 30, 170, 120) + cb + tunas('kaget', 110, 128, 200, cm - 120) + tears + cf +
     text(150, 110, 'oeek', 48, TD) + shadow(560, 395, 90) + tunas('ngantuk', 170, 198, 475, 195) + breath(660, 270) +
     text(690, 240, 'huuf', 40, SKYD, anchor='start') + clock(500, 90, 50, 2, 0))
out('hero-w2n-nangis-malam', 420, b)

b = (diaper(170, 230, 250) + thermo(380, 80, 270, 0.45) + clock(680, 220, 110, 2, 0))
out('big-w2n-nangis-cek', 420, b)

# bedong buat yang belum bisa guling: face stays free, wrap from the chest down
wrap_ = (f'<path d="M200 330 Q200 452 330 452 Q460 452 460 330 Q400 380 330 380 Q260 380 200 330 Z" fill="{BLUSH}"/>'
         f'<path d="M215 350 Q330 430 445 350" stroke="{TERRA}" stroke-width="7" fill="none" opacity="0.45"/><path d="M300 384 L350 446" stroke="{TERRA}" stroke-width="7" opacity="0.45"/>')
b = fl(400, 470, 120, 820) + shadow(330, 455, 150) + tunas('ngantuk', 240, 280, 210, 170) + wrap_ + text(520, 280, 'bedong', 66, SD, anchor='start')
out('big-w2n-nangis-bedong', 470, b)

# sshh + ayun pelan
b = (fl(330, 420, 120, 840) + shadow(330, 395, 100) + tunas('ngantuk', 190, 222, 235, 150) +
     f'<path d="M180 350 Q330 425 480 350" stroke="{SAGE}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M166 326 L178 354 L206 346 M494 326 L482 354 L454 346" stroke="{SAGE}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' +
     text(560, 210, 'sshh...', 76, SD, anchor='start') + waves(450, 190, 64, SKYD, 2))
out('big-w2n-nangis-sshh', 420, b)

cb, cf, cm = crib(40, 170, 320, 230)
b = (fl(360, 420, 20, 860) + cb + tunas_lying('ngantuk', 110, 128, 200, cm + 4) + cf +
     shadow(540, 395, 90) + tunas('ngantuk', 190, 222, 445, 172) + breath(640, 250) + clock(770, 110, 62, 0, 10) + text(770, 220, '10 menit', 38, TD))
out('big-w2n-nangis-napas', 420, b)

# =====================================================================
# 6. w2n-porsi-mpasi: bowls by age
b = (floor(320, 420) + mbowl(160, 210, 190, 0.45, SUN) + mbowl(410, 190, 220, 0.62, SUN, [TERRA, SAGE]) +
     mbowl(670, 170, 250, 0.9, '#f4ead8', [TERRA, SAGE], rice=True) +
     text(160, 170, '6-8 bln', 46, SD) + text(410, 150, '9-11 bln', 46, SD) + text(670, 130, '12-23 bln', 46, SD) + spoon(40, 380, 150, -12))
out('hero-w2n-porsi-mpasi', 420, b)

b = mbowl(280, 120, 360, 0.5, SUN, label='½') + spoon(500, 300, 240, -20) + text(560, 150, '2-3 sdm', 62, SD, anchor='start')
out('big-w2n-porsi-6', 400, b)

b = mbowl(280, 130, 360, 0.7, SUN, [TERRA, SAGE, TD]) + text(280, 105, '½-¾', 76, INK) + tunas('riset', 150, 175, 520, 150)
out('big-w2n-porsi-9', 400, b)

b = (mbowl(280, 130, 360, 0.95, '#f4ead8', [TERRA, SAGE, TD], rice=True) + text(280, 105, '¾-1', 76, INK) + tunas('hore', 150, 175, 520, 150))
out('big-w2n-porsi-12', 400, b)

# camilan 1-2x: a small plate of fruit pieces between meals
plate = f'<ellipse cx="300" cy="300" rx="230" ry="70" fill="{CARD}" stroke="{LINE}" stroke-width="8"/><ellipse cx="300" cy="296" rx="170" ry="46" fill="none" stroke="{LINE}" stroke-width="4"/>'
fruit = (f'<path d="M190 300 Q230 230 290 290 Z" fill="{SUN}"/><path d="M200 296 Q232 250 276 290" stroke="{SUND}" stroke-width="6" fill="none"/>'
         f'<path d="M300 304 Q345 236 400 296 Z" fill="{TERRA}"/><circle cx="340" cy="282" r="6" fill="#fff" opacity="0.6"/>'
         f'<circle cx="250" cy="318" r="22" fill="{SAGE}"/><circle cx="295" cy="324" r="20" fill="{SD}"/><circle cx="380" cy="318" r="20" fill="{SAGE}"/>')
b = shadow(300, 380, 220) + plate + fruit + text(300, 160, '1-2x', 80, SD) + clock(640, 260, 80, 10, 0)
out('big-w2n-porsi-camilan', 400, b)

# =====================================================================
# 7. w2n-demam-kapan-dokter: look at the child, not only the number
blanket = f'<path d="M300 338 Q300 305 400 305 Q500 305 500 338 L500 380 L300 380 Z" fill="{BLUSH}"/>'
b = (floor(340, 420) + shadow(120, 400, 60) + thermo(95, 110, 240, 0.7) + text(180, 160, '38°', 60, TD, anchor='start') +
     bed(300, 330, 300, 70).replace(f'fill="{BLUSH}"', f'fill="{MINT}"') + tunas('ngantuk', 150, 175, 325, 160) + blanket +
     shadow(720, 400, 80) + tunas('riset', 180, 210, 630, 185))
out('hero-w2n-demam-kapan-dokter', 420, b)

b = (fl(330, 420, 60, 820) + shadow(220, 395, 90) + tunas('ngantuk', 170, 198, 135, 200) + thermo(370, 120, 250, 0.7) + text(455, 200, '38°', 62, TD, anchor='start') +
     bubble(540, 40, 260, 110, BLUSH, 'left') + text(670, 115, '&lt; 3 bln', 58, TD))
out('big-w2n-demam-bayi', 420, b)

alert = f'<path d="M660 80 L780 290 L540 290 Z" fill="{TERRA}" stroke="{TERRA}" stroke-width="24" stroke-linejoin="round"/>' + text(660, 268, '!', 150, '#fff')
b = fl(320, 420, 20, 820) + bed(60, 300, 400, 100) + tunas_lying('ngantuk', 130, 152, 270, 304) + text(390, 170, 'z', 54, MUTED) + text(430, 130, 'z', 40, MUTED) + alert
out('big-w2n-demam-bahaya', 420, b)

b = diaper(230, 220, 280) + text(230, 400, 'jarang pipis', 52, MUTED) + drop(620, 220, 130) + f'<path d="M565 240 L675 240" stroke="#fff" stroke-width="24" stroke-linecap="round"/>'
out('big-w2n-demam-cairan', 440, b)

b = clock(230, 210, 150, 9, 0) + text(430, 180, 'lewat', 60, MUTED, anchor='start') + text(430, 280, '24 jam', 92, TD, anchor='start')
out('big-w2n-demam-lama', 400, b)

autocrop(NAMES)
print('\n'.join(NAMES))
