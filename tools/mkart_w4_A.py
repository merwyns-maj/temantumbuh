# Scenes for the week-4 group A SHORT posts: w4s-wake-window, w4s-jam-tidur, w4s-growth-spurt.
# Safe sleep in every sleep scene: baby on the back, flat empty mattress, no pillow, bumper, blanket or toy (AAP).
# Breast milk only as a drop or nothing: no bottle, teat or pacifier (PP 28/2024). No real faces.
# Run: python tools/mkart_w4_A.py [contact-sheet.png]
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

NIGHT = SKYD; MINT = '#e3eee6'; MILK = '#f7ecd6'; FACE = '#f6d2bf'; FACED = '#eab5a1'
NAMES = []


def out(name, h, body):
    svg(name, h, body)
    NAMES.append(name)


def rect(x, y, w, h, f, rx=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'


def fl(y, H, x0, x1):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{H-y}" rx="24" fill="{FLOOR}"/>'


def check(cx, cy, r=30):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SD}"/>'
            f'<path d="M{cx-r*0.47} {cy} L{cx-r*0.13} {cy+r*0.33} L{cx+r*0.47} {cy-r*0.33}" stroke="#fff" stroke-width="{r*0.28:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def tunas_lying(pose, w, h, cx, bottom):
    """Tunas on its back (side view), resting on y = bottom."""
    cy = bottom - 0.35 * w
    return f'<g transform="rotate(-90 {cx} {cy})">' + tunas(pose, w, h, cx - w / 2, cy - h / 2) + '</g>'


def window(x, y, w, h, night=True):
    s = rect(x - 12, y - 12, w + 24, h + 24, BOX, 18) + rect(x, y, w, h, NIGHT if night else SKY, 10)
    if night:
        s += f'<circle cx="{x+w*0.68}" cy="{y+h*0.38}" r="{h*0.2}" fill="{SUN}"/><circle cx="{x+w*0.76}" cy="{y+h*0.31}" r="{h*0.18}" fill="{NIGHT}"/>'
        for sx, sy in ((0.2, 0.25), (0.35, 0.65), (0.2, 0.8), (0.85, 0.78)):
            s += f'<circle cx="{x+w*sx}" cy="{y+h*sy}" r="5" fill="#fff" opacity="0.85"/>'
    else:
        s += f'<circle cx="{x+w*0.3}" cy="{y+h*0.35}" r="{h*0.18}" fill="{SUN}"/>'
    s += rect(x + w / 2 - 6, y, 12, h, BOX) + rect(x, y + h / 2 - 6, w, 12, BOX)
    return s


def clock(cx, cy, r, hour, minute=0, ring=TERRA):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r+8}" fill="{ring}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}"/>'
    for k in range(12):
        a = k * math.pi / 6
        s += f'<circle cx="{cx+r*0.78*math.sin(a):.1f}" cy="{cy-r*0.78*math.cos(a):.1f}" r="{r*0.06:.1f}" fill="{LINE}"/>'
    ah = (hour % 12 + minute / 60) * math.pi / 6
    am = minute * math.pi / 30
    s += f'<path d="M{cx} {cy} L{cx+r*0.48*math.sin(ah):.1f} {cy-r*0.48*math.cos(ah):.1f}" stroke="{INK}" stroke-width="{r*0.13:.0f}" stroke-linecap="round"/>'
    s += f'<path d="M{cx} {cy} L{cx+r*0.7*math.sin(am):.1f} {cy-r*0.7*math.cos(am):.1f}" stroke="{INK}" stroke-width="{r*0.09:.0f}" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.1:.1f}" fill="{TERRA}"/>'
    return s


def sector(cx, cy, r, h0, h1, col, op=1):
    """Pie slice on a 12-hour dial from hour h0 to h1 (clockwise from 12)."""
    a0, a1 = h0 * math.pi / 6, h1 * math.pi / 6
    big = 1 if (h1 - h0) > 6 else 0
    return (f'<path d="M{cx} {cy} L{cx+r*math.sin(a0):.1f} {cy-r*math.cos(a0):.1f} A{r} {r} 0 {big} 1 {cx+r*math.sin(a1):.1f} {cy-r*math.cos(a1):.1f} Z" fill="{col}" opacity="{op}"/>')


def awake_dial(cx, cy, r, lo, hi):
    """Dial showing an awake-time range: solid sage up to `lo` hours, light sage up to `hi`."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r+10}" fill="{SD}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}"/>'
    s += sector(cx, cy, r - 8, 0, hi, SAGE, 0.35) + sector(cx, cy, r - 8, 0, lo, SAGE)
    for k in range(12):
        a = k * math.pi / 6
        s += f'<circle cx="{cx+r*0.86*math.sin(a):.1f}" cy="{cy-r*0.86*math.cos(a):.1f}" r="{r*0.05:.1f}" fill="{INK}" opacity="0.35"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r*0.1:.1f}" fill="{INK}"/>'


def crib(x, y, w, h):
    """Side view; y = top rail, y + h = floor. Returns (back, front, mattress_top). Mattress flat and empty."""
    mat = y + h * 0.56
    back = rect(x, y - 16, 24, h + 16, BOXD, 10) + rect(x + w - 24, y - 16, 24, h + 16, BOXD, 10)
    for sx in range(int(x + 50), int(x + w - 40), 44):
        back += rect(sx, y + 10, 12, mat - y - 10, BOX, 6)
    back += rect(x, y, w, 22, BOX, 11)
    back += rect(x + 18, mat, w - 36, 34, CARD, 12, f'stroke="{LINE}" stroke-width="5"')
    front = rect(x, mat + 32, w, 22, BOXD, 11)
    return back, front, mat


def kid_bed(x, y, w, h):
    """Low child bed, side view, flat mattress top at y, no pillow or blanket. Returns (back, front, top)."""
    back = rect(x - 6, y - 90, 30, h + 90, BOXD, 12) + rect(x + w - 24, y - 40, 30, h + 40, BOXD, 12)
    back += rect(x, y, w, 46, CARD, 16, f'stroke="{LINE}" stroke-width="5"')
    front = rect(x, y + 40, w, 30, BOX, 12)
    return back, front, y


def rug(cx, cy, rx, ry):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{MINT}"/><ellipse cx="{cx}" cy="{cy}" rx="{rx-22}" ry="{ry-12}" fill="none" stroke="{SAGE}" stroke-width="5" stroke-dasharray="2 16" stroke-linecap="round"/>'


def drop(cx, cy, s, col=MILK, stroke=BOX):
    return (f'<path d="M{cx} {cy-s} Q{cx+s*0.75} {cy-s*0.05} {cx+s*0.62} {cy+s*0.35} Q{cx+s*0.45} {cy+s*0.8} {cx} {cy+s*0.8} Q{cx-s*0.45} {cy+s*0.8} {cx-s*0.62} {cy+s*0.35} Q{cx-s*0.75} {cy-s*0.05} {cx} {cy-s} Z" fill="{col}" stroke="{stroke}" stroke-width="{max(3, s*0.08):.0f}"/>'
            f'<ellipse cx="{cx-s*0.25}" cy="{cy+s*0.2}" rx="{s*0.1}" ry="{s*0.2}" fill="#fff" opacity="0.6"/>')


def tear(cx, cy, s):
    return f'<path d="M{cx} {cy} Q{cx+s*0.5} {cy+s*0.9} {cx} {cy+s*1.2} Q{cx-s*0.5} {cy+s*0.9} {cx} {cy} Z" fill="{SKY}"/>'


def calendar(x, y, w, big, small=None):
    h = w * 0.9
    s = rect(x, y, w, h, CARD, 18, f'stroke="{LINE}" stroke-width="6"') + rect(x, y, w, h * 0.26, TERRA, 18) + rect(x, y + h * 0.16, w, h * 0.1, TERRA)
    s += rect(x + w * 0.25, y - 14, 14, 34, INK, 7) + rect(x + w * 0.7, y - 14, 14, 34, INK, 7)
    s += text(x + w / 2, y + h * (0.64 if small else 0.78), big, w * 0.3, INK)
    if small:
        s += text(x + w / 2, y + h * 0.88, small, w * 0.16, MUTED)
    return s


def diaper(cx, cy, w, wet=False):
    h = w * 0.7
    s = f'<path d="M{cx-w/2} {cy-h/2} L{cx+w/2} {cy-h/2} L{cx+w*0.42} {cy} Q{cx+w*0.2} {cy+h*0.55} {cx} {cy+h*0.55} Q{cx-w*0.2} {cy+h*0.55} {cx-w*0.42} {cy} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    s += rect(cx - w / 2 - 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8) + rect(cx + w / 2 - w * 0.22 + 6, cy - h / 2 - 2, w * 0.22, h * 0.24, SKY, 8)
    if wet:
        s += f'<ellipse cx="{cx}" cy="{cy+h*0.1}" rx="{w*0.22}" ry="{h*0.2}" fill="{SUN}" opacity="0.45"/>'
    return s


def baby_face(cx, cy, r, expr):
    """Simple flat cartoon baby head (not a real face). expr: nguap, kosong, nangis."""
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FACE}"/>'
    s += f'<path d="M{cx-r*0.1} {cy-r*0.95} Q{cx+r*0.15} {cy-r*1.3} {cx+r*0.3} {cy-r*1.05}" stroke="{HAIR}" stroke-width="{r*0.1:.0f}" fill="none" stroke-linecap="round"/>'
    s += ''.join(f'<ellipse cx="{cx+k*r*0.55}" cy="{cy+r*0.3}" rx="{r*0.16}" ry="{r*0.1}" fill="{CHEEK}" opacity="0.6"/>' for k in (-1, 1))
    w = max(4, r * 0.08)
    if expr == 'nguap':
        s += ''.join(f'<path d="M{cx+k*r*0.38-r*0.15} {cy-r*0.05} Q{cx+k*r*0.38} {cy+r*0.06} {cx+k*r*0.38+r*0.15} {cy-r*0.05}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
        s += f'<ellipse cx="{cx}" cy="{cy+r*0.42}" rx="{r*0.2}" ry="{r*0.26}" fill="{TD}"/>'
    elif expr == 'kosong':
        s += ''.join(f'<circle cx="{cx+k*r*0.38}" cy="{cy}" r="{r*0.09}" fill="{INK}"/><path d="M{cx+k*r*0.38-r*0.16} {cy-r*0.06} L{cx+k*r*0.38+r*0.16} {cy-r*0.06}" stroke="{FACED}" stroke-width="{w*1.4}" stroke-linecap="round"/>' for k in (-1, 1))
        s += f'<path d="M{cx-r*0.14} {cy+r*0.45} L{cx+r*0.14} {cy+r*0.45}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
    elif expr == 'nangis':
        s += ''.join(f'<path d="M{cx+k*r*0.38-r*0.15} {cy} Q{cx+k*r*0.38} {cy-r*0.12} {cx+k*r*0.38+r*0.15} {cy}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
        s += f'<ellipse cx="{cx}" cy="{cy+r*0.45}" rx="{r*0.22}" ry="{r*0.17}" fill="{TD}"/>'
        s += tear(cx - r * 0.42, cy + r * 0.08, r * 0.28) + tear(cx + r * 0.42, cy + r * 0.08, r * 0.28)
    return s


def fist(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FACED}"/>' + ''.join(f'<path d="M{cx-r*0.5} {cy-r*0.3+k*r*0.3} L{cx+r*0.1} {cy-r*0.3+k*r*0.3}" stroke="{FACE}" stroke-width="{r*0.12:.0f}" stroke-linecap="round"/>' for k in range(3))


def motion(x, y, s, col=TERRA, flip=False):
    sg = -1 if flip else 1
    return ''.join(f'<path d="M{x+sg*k*s*0.35} {y-s*0.4} L{x+sg*(k*s*0.35+s*0.2)} {y-s*0.6}" stroke="{col}" stroke-width="8" stroke-linecap="round"/>' for k in range(3))


def glass(cx, bottom, w):
    h = w * 1.25
    return (f'<path d="M{cx-w/2} {bottom-h} L{cx+w/2} {bottom-h} L{cx+w*0.4} {bottom} L{cx-w*0.4} {bottom} Z" fill="{CARD}" stroke="{SKYD}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{cx-w*0.46} {bottom-h*0.62} L{cx+w*0.46} {bottom-h*0.62} L{cx+w*0.4} {bottom-4} L{cx-w*0.4} {bottom-4} Z" fill="{SKY}" opacity="0.7"/>')


def banana(cx, cy, s):
    return (f'<path d="M{cx-s} {cy-s*0.2} Q{cx} {cy+s*0.9} {cx+s} {cy-s*0.3} Q{cx} {cy+s*0.45} {cx-s} {cy-s*0.2} Z" fill="{SUN}" stroke="{SUND}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="{cx+s*0.9}" y="{cy-s*0.42}" width="{s*0.18}" height="{s*0.2}" rx="4" fill="{BOXD}" transform="rotate(30 {cx+s} {cy-s*0.3})"/>')


def backpack(cx, cy, s):
    return (f'<path d="M{cx-s*0.3} {cy-s*0.55} Q{cx} {cy-s*0.85} {cx+s*0.3} {cy-s*0.55}" stroke="{TD}" stroke-width="{s*0.1:.0f}" fill="none"/>'
            + rect(cx - s * 0.45, cy - s * 0.6, s * 0.9, s * 1.1, TERRA, s * 0.2) + rect(cx - s * 0.32, cy + s * 0.05, s * 0.64, s * 0.35, TD, s * 0.1)
            + rect(cx - s * 0.08, cy - s * 0.02, s * 0.16, s * 0.14, SUN, 4))


def crayon(cx, cy, s, col, rot):
    return (f'<g transform="rotate({rot} {cx} {cy})">' + rect(cx - s * 0.5, cy - s * 0.1, s * 0.85, s * 0.2, col, s * 0.05) +
            f'<path d="M{cx+s*0.35} {cy-s*0.1} L{cx+s*0.55} {cy} L{cx+s*0.35} {cy+s*0.1} Z" fill="{col}"/>' + rect(cx - s * 0.3, cy - s * 0.1, s * 0.1, s * 0.2, '#fff', 0, 'opacity="0.5"') + '</g>')


def ball(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SKY}"/><path d="M{cx-r} {cy} Q{cx} {cy-r*0.4} {cx+r} {cy}" stroke="#fff" stroke-width="{r*0.14:.0f}" fill="none"/>'
            f'<path d="M{cx} {cy-r} Q{cx+r*0.35} {cy} {cx} {cy+r}" stroke="{SUN}" stroke-width="{r*0.14:.0f}" fill="none"/>')


def moon(cx, cy, r, bg=CARD):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/><circle cx="{cx+r*0.45}" cy="{cy-r*0.3}" r="{r*0.85}" fill="{bg}"/>'


def arrow(x0, y, x1, col=SAGE):
    return (f'<path d="M{x0} {y} L{x1-10} {y}" stroke="{col}" stroke-width="12" stroke-linecap="round" stroke-dasharray="2 22"/>'
            f'<path d="M{x1-30} {y-22} L{x1} {y} L{x1-30} {y+22}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def badge(cx, cy, label, col=SAGE, w=200, ink=CARD, size=38):
    return f'<rect x="{cx-w/2}" y="{cy-32}" width="{w}" height="64" rx="32" fill="{col}"/>' + text(cx, cy + 13, label, size, ink)


# =====================================================================
# HERO 1 (w4s-wake-window): awake on the rug with the sun -> about an hour -> asleep on the back in an empty crib
cb, cf, cm = crib(500, 130, 360, 290)
b = (floor(400, 460) + window(40, 10, 150, 110, night=False) + rug(190, 415, 180, 36) + shadow(190, 420, 90) +
     tunas('hore', 200, 233, 90, 185) + arrow(330, 330, 480) + badge(405, 250, '± 1 jam', SUN, 170, INK, 36) +
     cb + tunas_lying('ngantuk', 140, 163, 680, cm + 4) + cf + check(810, 60, 40))
out('hero-w4a-melek-tidur', 460, b)

# HERO 2 (w4s-jam-tidur): night window, child asleep on the back on a flat bed, big clock at 8
kb, kf, kt = kid_bed(250, 300, 360, 90)
b = (floor(390, 440) + window(60, 40, 160, 120) + kb + tunas_lying('ngantuk', 140, 163, 430, kt + 4) + kf +
     clock(730, 150, 100, 8, 0) + moon(820, 30, 26, '#fbf4ea'))
out('hero-w4a-jam-tidur', 440, b)

# HERO 3 (w4s-growth-spurt): Mama hugs the baby close (nursing implied, no bottle), growth ruler with an up arrow
T = 470
from people import _arms
r_ = 62 * 1.5; ty_ = 180 + r_ * 0.95
m = person('mama', 300, 180, 1.5, 'lembut', 'none')
b = (fl(T - 10, 500, 30, 860) + m + tunas('sayang', 170, 198, 345, 222) + _arms('mama', 300, ty_ + 118, r_, 'peluk', *OUTFIT['mama']) +
     rect(670, 60, 90, 400, CARD, 14, f'stroke="{LINE}" stroke-width="6"') +
     ''.join(rect(670, 90 + k * 40, 34 if k % 2 else 52, 7, BOXD, 3) for k in range(9)) +
     f'<path d="M800 380 L800 110" stroke="{TERRA}" stroke-width="16" stroke-linecap="round"/><path d="M766 150 L800 104 L834 150" stroke="{TERRA}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' +
     drop(590, 120, 34) + drop(620, 200, 26) + drop(580, 260, 20))
out('hero-w4a-growth-spurt', 500, b)

# =====================================================================
# Wake window rows: awake-time dial grows with age, Tunas grows beside it
for key, lo, hi, tw_, pose in (('0-3', 1, 2, 80, 'ngantuk'), ('4-6', 1.5, 3, 95, 'halo'), ('6-9', 2, 3, 110, 'santai'),
                               ('9-12', 2.5, 4, 125, 'hore'), ('12-18', 3, 5, 140, 'riset')):
    th = tw_ * 140 / 120
    b = awake_dial(130, 150, 115, lo, hi) + shadow(330, 290, tw_ * 0.45) + tunas(pose, tw_, th, 330 - tw_ / 2, 290 - th)
    out(f'big-w4a-ww-{key}', 300, b)

# Sleepy cues
out('big-w4a-tanda-nguap', 300, baby_face(150, 160, 110, 'nguap') + text(300, 90, 'huaa', 46, MUTED, anchor='start'))
out('big-w4a-tanda-telinga', 300, baby_face(150, 160, 110, 'kosong') + fist(262, 140, 34) + motion(300, 120, 40))
b = (fl(230, 290, 10, 400) + rect(30, 196, 340, 34, CARD, 12, f'stroke="{LINE}" stroke-width="5"') + tunas_lying('kaget', 130, 152, 200, 200) +
     motion(80, 120, 40, TERRA, True) + motion(320, 120, 40))
out('big-w4a-tanda-sentak', 300, b)
out('big-w4a-tanda-rewel', 300, baby_face(150, 160, 110, 'nangis') + ball(320, 230, 40))

# =====================================================================
# Jam tidur: who (age icons) and when (clocks)
cb, cf, cm = crib(20, 60, 300, 220)
out('big-w4a-usia-bayi', 300, cb + tunas_lying('ngantuk', 110, 128, 170, cm + 4) + cf)
out('big-w4a-usia-balita', 300, shadow(150, 285, 70) + tunas('hore', 150, 175, 75, 110) + ball(300, 245, 42))
out('big-w4a-usia-prasekolah', 300, shadow(160, 285, 76) + tunas('santai', 160, 187, 80, 98) + crayon(300, 250, 110, TERRA, -20) + crayon(320, 210, 110, SKYD, -35))
out('big-w4a-usia-sd', 300, shadow(160, 285, 80) + tunas('riset', 170, 198, 75, 87) + backpack(330, 220, 110))
for key, hr in (('8', 8), ('9', 9)):
    out(f'big-w4a-jam-{key}', 300, clock(150, 150, 115, hr, 0) + moon(300, 60, 34))
out('big-w4a-jam-tanda', 300, awake_dial(130, 150, 115, 2, 3) + shadow(320, 290, 55) + tunas('ngantuk', 120, 140, 260, 150))

# =====================================================================
# Growth spurt: when (calendars) and what (signs, prep)
for key, big, small in (('2-3mg', '2-3', 'minggu'), ('6mg', '6', 'minggu'), ('3bl', '3', 'bulan'), ('6bl', '5-6', 'bulan')):
    out(f'big-w4a-gs-{key}', 300, calendar(20, 30, 260, big, small) + f'<path d="M340 250 L340 90" stroke="{SAGE}" stroke-width="14" stroke-linecap="round"/><path d="M314 120 L340 86 L366 120" stroke="{SAGE}" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
b = clock(140, 150, 110, 2, 0) + ''.join(drop(x, y, 26) for x, y in ((300, 70), (340, 150), (300, 230)))
out('big-w4a-gs-nyusu', 300, b)
out('big-w4a-gs-rewel', 300, baby_face(150, 160, 110, 'nangis') + motion(290, 110, 40))
out('big-w4a-gs-minum', 300, fl(250, 300, 10, 380) + glass(120, 250, 120) + banana(270, 220, 80))
b = diaper(90, 130, 120, True) + diaper(230, 130, 120, True) + diaper(160, 230, 120, True) + check(320, 60, 36)
out('big-w4a-gs-popok', 300, b)

autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=360))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 6; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (360 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 360, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
