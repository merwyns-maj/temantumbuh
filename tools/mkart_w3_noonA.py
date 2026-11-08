# Design v2 scenes for the week-3 noon "Contekan" posts, group A (w3n-ngobrol, w3n-gigi-telat, w3n-kaki-o).
# Run: python tools/mkart_w3_noonA.py [contact-sheet.png]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

GUM = '#eab5a1'    # Tunas skin shade, used for gums
MINT = '#e3eee6'   # sage tint
SKIN = '#f3cba5'; SKIND = '#e2ad83'   # same skin as people.py
NAMES = []


def out(name, h, body):
    svg(name, h, body)
    NAMES.append(name)


# ---------------- helpers (same shapes as mkart_w2_noon, copied so that script is not re-run on import)
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


def sparkle(cx, cy, s, col=SUN):
    return f'<path d="M{cx} {cy-s} L{cx+s*0.28} {cy-s*0.28} L{cx+s} {cy} L{cx+s*0.28} {cy+s*0.28} L{cx} {cy+s} L{cx-s*0.28} {cy+s*0.28} L{cx-s} {cy} L{cx-s*0.28} {cy-s*0.28} Z" fill="{col}"/>'


def drop(cx, cy, s, col=SKY):
    return f'<path d="M{cx} {cy-s} Q{cx+s*0.75} {cy-s*0.05} {cx+s*0.62} {cy+s*0.35} Q{cx+s*0.45} {cy+s*0.8} {cx} {cy+s*0.8} Q{cx-s*0.45} {cy+s*0.8} {cx-s*0.62} {cy+s*0.35} Q{cx-s*0.75} {cy-s*0.05} {cx} {cy-s} Z" fill="{col}"/>'


def fl(y, H, x0, x1):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{H-y}" rx="24" fill="{FLOOR}"/>'


def calendar(x, y, w, big, small=None):
    h = w * 0.9
    s = rect(x, y, w, h, CARD, 18, f'stroke="{LINE}" stroke-width="6"') + rect(x, y, w, h * 0.26, TERRA, 18) + rect(x, y + h * 0.16, w, h * 0.1, TERRA)
    s += rect(x + w * 0.25, y - 14, 14, 34, INK, 7) + rect(x + w * 0.7, y - 14, 14, 34, INK, 7)
    s += text(x + w / 2, y + h * (0.66 if small else 0.78), big, w * 0.34, INK)
    if small:
        s += text(x + w / 2, y + h * 0.88, small, w * 0.17, MUTED)
    return s


def tooth(cx, cy, s, shine=True, dashed=False):
    w, h = s, s * 1.1
    d = (f'M{cx-w*0.5} {cy-h*0.25} Q{cx-w*0.5} {cy-h*0.5} {cx-w*0.25} {cy-h*0.5} Q{cx-w*0.1} {cy-h*0.5} {cx} {cy-h*0.42} '
         f'Q{cx+w*0.1} {cy-h*0.5} {cx+w*0.25} {cy-h*0.5} Q{cx+w*0.5} {cy-h*0.5} {cx+w*0.5} {cy-h*0.25} '
         f'Q{cx+w*0.5} {cy+h*0.05} {cx+w*0.36} {cy+h*0.2} L{cx+w*0.3} {cy+h*0.46} Q{cx+w*0.24} {cy+h*0.55} {cx+w*0.16} {cy+h*0.42} '
         f'L{cx+w*0.06} {cy+h*0.16} Q{cx} {cy+h*0.08} {cx-w*0.06} {cy+h*0.16} L{cx-w*0.16} {cy+h*0.42} '
         f'Q{cx-w*0.24} {cy+h*0.55} {cx-w*0.3} {cy+h*0.46} L{cx-w*0.36} {cy+h*0.2} Q{cx-w*0.5} {cy+h*0.05} {cx-w*0.5} {cy-h*0.25} Z')
    if dashed:
        return f'<path d="{d}" fill="#fff" fill-opacity="0.45" stroke="#fff" stroke-width="{max(5, s*0.06):.0f}" stroke-dasharray="{s*0.12:.0f} {s*0.09:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
    o = f'<path d="{d}" fill="#fff" stroke="{LINE}" stroke-width="{max(4, s*0.05):.0f}" stroke-linejoin="round"/>'
    if shine:
        o += f'<path d="M{cx-w*0.32} {cy-h*0.2} Q{cx-w*0.3} {cy-h*0.36} {cx-w*0.16} {cy-h*0.38}" stroke="{SKY}" stroke-width="{s*0.07:.0f}" fill="none" stroke-linecap="round"/>'
    return o


def cake(x, y, label='1'):
    """Birthday cake, top-left of the body at x, y (body 300 x 120, candle above)."""
    return (rect(x, y, 300, 120, BLUSH, 20) + rect(x, y, 300, 40, '#fff', 20) +
            f'<path d="M{x+10} {y+36} q25 22 50 0 q25 22 50 0 q25 22 50 0 q25 22 50 0 q25 22 50 0 q20 18 40 0" stroke="#fff" stroke-width="16" fill="none"/>' +
            rect(x + 138, y - 100, 26, 100, SKY, 10) + f'<path d="M{x+151} {y-150} Q{x+172} {y-120} {x+151} {y-104} Q{x+130} {y-120} {x+151} {y-150} Z" fill="{SUN}"/>' +
            text(x + 151, y + 100, label, 72, TD))


def gum(x, y, w, teeth_dashed=0):
    """Lower gum arch seen from the front, top-left x, y, width w; optional dashed teeth still under the gum."""
    h = w * 0.45
    s = (f'<path d="M{x} {y} Q{x+w/2} {y+h*0.55} {x+w} {y} L{x+w} {y+h*0.5} Q{x+w/2} {y+h*1.05} {x} {y+h*0.5} Z" fill="{GUM}"/>'
         f'<path d="M{x} {y} Q{x+w/2} {y+h*0.55} {x+w} {y}" stroke="{TD}" stroke-width="8" fill="none" opacity="0.35"/>')
    if teeth_dashed:
        cx = x + w / 2
        for k in range(teeth_dashed):
            dx = (k - (teeth_dashed - 1) / 2) * w * 0.17
            ty = y + h * 0.27 + abs(dx) * 0.18 + w * 0.08
            s += f'<path d="M{cx+dx-w*0.06} {ty+w*0.07} Q{cx+dx-w*0.065} {ty-w*0.03} {cx+dx} {ty-w*0.035} Q{cx+dx+w*0.065} {ty-w*0.03} {cx+dx+w*0.06} {ty+w*0.07}" stroke="#fff" stroke-width="7" fill="none" stroke-dasharray="10 9" stroke-linecap="round"/>'
    return s


def mouth(cx, cy, s, dashed=2):
    """Open baby mouth seen from the front: lips, pink gums with no teeth yet (dashed outlines = teeth still inside)."""
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="{s*1.12}" ry="{s*0.78}" fill="{BLUSH}"/>'
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{s}" ry="{s*0.64}" fill="{TD}"/>'
    o += f'<path d="M{cx-s*0.62} {cy+s*0.42} Q{cx} {cy+s*0.05} {cx+s*0.62} {cy+s*0.42} Q{cx} {cy+s*0.62} {cx-s*0.62} {cy+s*0.42} Z" fill="#f2a38c"/>'
    o += f'<path d="M{cx-s} {cy-s*0.05} Q{cx-s*0.98} {cy-s*0.64} {cx} {cy-s*0.64} Q{cx+s*0.98} {cy-s*0.64} {cx+s} {cy-s*0.05} Q{cx} {cy-s*0.36} {cx-s} {cy-s*0.05} Z" fill="{GUM}"/>'
    o += f'<path d="M{cx-s} {cy+s*0.05} Q{cx-s*0.95} {cy+s*0.64} {cx} {cy+s*0.64} Q{cx+s*0.95} {cy+s*0.64} {cx+s} {cy+s*0.05} Q{cx} {cy+s*0.52} {cx-s} {cy+s*0.05} Z" fill="{GUM}"/>'
    for k in range(dashed):
        dx = (k - (dashed - 1) / 2) * s * 0.3
        ty = cy + s * 0.42
        o += f'<path d="M{cx+dx-s*0.1} {ty+s*0.12} L{cx+dx-s*0.1} {ty-s*0.0} Q{cx+dx} {ty-s*0.1} {cx+dx+s*0.1} {ty-s*0.0} L{cx+dx+s*0.1} {ty+s*0.12}" stroke="#fff" stroke-width="{max(5, s*0.05):.0f}" fill="none" stroke-dasharray="{s*0.07:.0f} {s*0.06:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
    return o


def hourglass(cx, cy, s):
    return (rect(cx - s * 0.5, cy - s, s, s * 0.14, BOXD, 6) + rect(cx - s * 0.5, cy + s * 0.86, s, s * 0.14, BOXD, 6) +
            f'<path d="M{cx-s*0.4} {cy-s*0.86} L{cx+s*0.4} {cy-s*0.86} L{cx+s*0.06} {cy} L{cx+s*0.4} {cy+s*0.86} L{cx-s*0.4} {cy+s*0.86} L{cx-s*0.06} {cy} Z" fill="{CARD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{cx-s*0.22} {cy-s*0.5} L{cx+s*0.22} {cy-s*0.5} L{cx} {cy-s*0.1} Z" fill="{SUN}"/>'
            f'<path d="M{cx-s*0.32} {cy+s*0.8} Q{cx} {cy+s*0.4} {cx+s*0.32} {cy+s*0.8} Z" fill="{SUN}"/>'
            f'<path d="M{cx} {cy} L{cx} {cy+s*0.5}" stroke="{SUN}" stroke-width="5" stroke-dasharray="4 8" stroke-linecap="round"/>')


def arrow(x0, y, x1, col=SAGE, w=12):
    return (f'<path d="M{x0} {y} L{x1} {y}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x1-30} {y-26} L{x1+4} {y} L{x1-30} {y+26}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


# ---------------- ngobrol
def plate(cx, cy, w):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w*0.16}" fill="{CARD}" stroke="{LINE}" stroke-width="7"/><ellipse cx="{cx}" cy="{cy-2}" rx="{w*0.32}" ry="{w*0.09}" fill="none" stroke="{LINE}" stroke-width="4"/>'


def foam(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{SKYD}" stroke-width="4"/>' for x, y, r in pts)


def sink(x, y, w):
    """Kitchen counter with a sink, counter top at y, from x to x + w (front panel down to y + 150)."""
    s = rect(x, y + 26, w, 124, BOX, 14) + rect(x + 20, y + 50, w * 0.42, 86, BOXD, 10, 'opacity="0.35"') + rect(x + w * 0.52, y + 50, w * 0.42, 86, BOXD, 10, 'opacity="0.35"')
    s += rect(x - 10, y, w + 20, 34, CARD, 14, f'stroke="{LINE}" stroke-width="5"')
    s += rect(x + w * 0.2, y + 4, w * 0.5, 22, SKYD, 10)  # basin opening
    fx = x + w * 0.62
    s += (f'<path d="M{fx} {y+2} L{fx} {y-90} Q{fx} {y-118} {fx+30} {y-118} L{fx+62} {y-118}" stroke="#c8c2b8" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          + drop(fx + 64, y - 80, 12))
    return s


def cat(cx, bottom, s):
    """Sitting cat, side-ish view, sits on y = bottom."""
    return (f'<path d="M{cx+s*0.35} {bottom-s*0.15} Q{cx+s*0.95} {bottom-s*0.1} {cx+s*0.8} {bottom-s*0.7}" stroke="{SUND}" stroke-width="{s*0.14}" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="{cx}" cy="{bottom-s*0.42}" rx="{s*0.45}" ry="{s*0.44}" fill="{SUND}"/>'
            f'<ellipse cx="{cx-s*0.12}" cy="{bottom-s*0.3}" rx="{s*0.22}" ry="{s*0.3}" fill="{SUN}"/>'
            f'<path d="M{cx-s*0.42} {bottom-s*1.08} L{cx-s*0.36} {bottom-s*1.42} L{cx-s*0.12} {bottom-s*1.18} Z" fill="{SUND}"/>'
            f'<path d="M{cx+s*0.42} {bottom-s*1.08} L{cx+s*0.36} {bottom-s*1.42} L{cx+s*0.12} {bottom-s*1.18} Z" fill="{SUND}"/>'
            f'<circle cx="{cx}" cy="{bottom-s*0.98}" r="{s*0.38}" fill="{SUND}"/>'
            f'<circle cx="{cx-s*0.14}" cy="{bottom-s*1.0}" r="{s*0.05}" fill="{INK}"/><circle cx="{cx+s*0.14}" cy="{bottom-s*1.0}" r="{s*0.05}" fill="{INK}"/>'
            f'<path d="M{cx-s*0.05} {bottom-s*0.9} L{cx+s*0.05} {bottom-s*0.9} L{cx} {bottom-s*0.85} Z" fill="{TD}"/>'
            f'<path d="M{cx-s*0.2} {bottom-s*0.88} L{cx-s*0.5} {bottom-s*0.92} M{cx+s*0.2} {bottom-s*0.88} L{cx+s*0.5} {bottom-s*0.92}" stroke="{INK}" stroke-width="3" opacity="0.5"/>')


def car(x, y, w, col=TERRA):
    """Side view; x, y = top-left of the roof, w = length."""
    h = w * 0.42
    s = (f'<path d="M{x+w*0.2} {y+h*0.42} L{x+w*0.32} {y} L{x+w*0.68} {y} L{x+w*0.82} {y+h*0.42} Z" fill="{col}"/>'
         f'<path d="M{x+w*0.27} {y+h*0.38} L{x+w*0.36} {y+h*0.1} L{x+w*0.48} {y+h*0.1} L{x+w*0.48} {y+h*0.38} Z" fill="{SKY}"/>'
         f'<path d="M{x+w*0.53} {y+h*0.38} L{x+w*0.53} {y+h*0.1} L{x+w*0.64} {y+h*0.1} L{x+w*0.74} {y+h*0.38} Z" fill="{SKY}"/>'
         + rect(x, y + h * 0.36, w, h * 0.42, col, h * 0.16) + rect(x + w * 0.9, y + h * 0.46, w * 0.08, h * 0.1, SUN, 4))
    for wx in (0.24, 0.76):
        s += f'<circle cx="{x+w*wx}" cy="{y+h*0.8}" r="{h*0.22}" fill="{INK}"/><circle cx="{x+w*wx}" cy="{y+h*0.8}" r="{h*0.09}" fill="#c8c2b8"/>'
    return s


def banana(cx, cy, s):
    return (f'<path d="M{cx-s} {cy-s*0.3} Q{cx-s*0.6} {cy+s*0.7} {cx+s*0.8} {cy+s*0.1} Q{cx+s*0.95} {cy-s*0.05} {cx+s*0.85} {cy-s*0.2} Q{cx-s*0.3} {cy+s*0.25} {cx-s*0.8} {cy-s*0.45} Z" fill="{SUN}"/>'
            f'<path d="M{cx-s*0.85} {cy-s*0.3} Q{cx-s*0.4} {cy+s*0.45} {cx+s*0.7} {cy+s*0.05}" stroke="{SUND}" stroke-width="5" fill="none"/>'
            + rect(cx - s * 1.08, cy - s * 0.52, s * 0.22, s * 0.16, BOXD, 4))


def papaya(cx, cy, s):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{s}" ry="{s*0.6}" fill="{SAGE}"/><ellipse cx="{cx}" cy="{cy}" rx="{s*0.86}" ry="{s*0.48}" fill="{TERRA}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{s*0.42}" ry="{s*0.2}" fill="{TD}"/>'
            + ''.join(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{s*0.055}" fill="{INK}"/>' for dx, dy in ((-0.25, 0), (-0.1, -0.08), (0.05, 0.06), (0.2, -0.04), (0.3, 0.05), (-0.05, 0.1))))


# hero: Tunas at the sink tells what it is doing, little Tunas answers
b = (floor(350, 440) + tunas('halo', 250, 292, 70, 10) + sink(40, 250, 420) +
     foam(((150, 246, 20), (182, 238, 26), (218, 246, 18), (300, 242, 22))) + plate(390, 236, 110) +
     shadow(680, 420, 90) + tunas('hore', 180, 210, 590, 215) +
     bubble(330, 10, 300, 100, MINT, 'left') + text(480, 78, 'cuci piring', 50, SD) +
     bubble(660, 70, 190, 90, BLUSH, 'left') + text(755, 130, 'piing', 50, TD))
out('hero-w3n-ngobrol', 440, b)

# 1 cerita: plate + sponge in foam, a bubble narrating
b = (fl(330, 420, 40, 640) + shadow(250, 360, 200) + plate(250, 320, 330) +
     foam(((150, 300, 22), (190, 292, 28), (330, 300, 20), (360, 310, 16))) +
     f'<g transform="rotate(-14 250 270)">' + rect(190, 240, 130, 66, SUN, 14) + rect(190, 240, 130, 24, SAGE, 12) + '</g>' +
     drop(420, 230, 18) + drop(455, 270, 13) +
     bubble(300, 40, 300, 110, MINT, 'left') + text(450, 116, 'cuci-cuci', 58, SD))
out('big-w3n-ngobrol-cerita', 420, b)

# 2 tunjuk: little Tunas points, the cat gets a name
b = (fl(330, 420, 30, 760) + shadow(175, 395, 110) + tunas('hore', 220, 257, 65, 140) +
     f'<path d="M290 230 Q400 170 470 220" stroke="{MUTED}" stroke-width="8" fill="none" stroke-dasharray="2 18" stroke-linecap="round"/>' +
     shadow(600, 395, 90) + cat(590, 392, 210) +
     bubble(300, 20, 260, 100, MINT, 'left') + text(430, 92, 'kucing', 56, SD))
out('big-w3n-ngobrol-tunjuk', 420, b)

# 3 tambah: "mobil" grows into "mobil merah"
b = (fl(340, 420, 30, 820) + shadow(430, 405, 260) + car(160, 200, 520) +
     bubble(40, 20, 210, 90, BLUSH, 'left') + text(145, 82, 'mobil', 48, TD) +
     arrow(280, 70, 380, SAGE, 10) +
     bubble(410, 10, 420, 110, MINT, 'left') + text(620, 84, 'mobil merah', 60, SD))
out('big-w3n-ngobrol-tambah', 420, b)

# 4 pilih: banana or papaya, Tunas thinks
b = (fl(330, 420, 30, 840) + shadow(170, 360, 120) + plate(170, 340, 250) + banana(170, 300, 100) +
     shadow(440, 395, 90) + tunas('mikir', 180, 210, 350, 175) +
     shadow(710, 360, 120) + plate(710, 340, 250) + papaya(710, 300, 100) +
     text(440, 120, 'atau', 64, MUTED))
out('big-w3n-ngobrol-pilih', 420, b)

# ---------------- gigi telat
b = (floor(330, 420) + shadow(180, 395, 150) + cake(30, 270) +
     shadow(430, 398, 80) + tunas('santai', 170, 198, 345, 196) +
     f'<g opacity="0.9">' + tooth(660, 220, 200, shine=False).replace('fill="#fff"', 'fill="#fff" fill-opacity="0.7"').replace(f'stroke="{LINE}"', f'stroke="{MUTED}" stroke-dasharray="18 14" stroke-linecap="round"') + '</g>' + hourglass(820, 120, 56) + sparkle(560, 120, 18) + sparkle(640, 70, 12, TERRA))
out('hero-w3n-gigi-telat', 420, b)

b = calendar(70, 120, 260, '12+', 'bulan') + tooth(560, 250, 200) + sparkle(680, 130, 26) + sparkle(450, 140, 16, TERRA)
out('big-w3n-gigitelat-rentang', 420, b)

# keturunan: an old photo of a baby (dulu) next to today's little one
photo = (f'<g transform="rotate(-8 230 230)">' + rect(90, 70, 280, 320, CARD, 12, f'stroke="{LINE}" stroke-width="6"') +
         rect(114, 94, 232, 220, BLUSH, 6) + tunas('santai', 150, 175, 155, 128) + text(230, 368, 'dulu', 46, MUTED) + '</g>')
b = fl(330, 430, 30, 800) + photo + shadow(600, 405, 100) + tunas('hore', 200, 233, 500, 170) + sparkle(470, 150, 20)
out('big-w3n-gigitelat-keturunan', 430, b)

# lap gusi habis makan: empty bowl and spoon, then a damp cloth
cloth = (f'<g transform="rotate(10 600 210)">' + rect(480, 120, 240, 180, MINT, 26) +
         f'<path d="M480 240 Q600 210 720 250" stroke="{SAGE}" stroke-width="7" fill="none" opacity="0.6"/>'
         f'<path d="M480 180 Q600 150 720 190" stroke="{SAGE}" stroke-width="7" fill="none" opacity="0.6"/>' + '</g>')
b = (fl(330, 430, 30, 800) + shadow(200, 370, 150) + bowl(200, 260, 260, TERRA, TD) +
     f'<g transform="rotate(-30 260 230)">' + rect(200, 222, 200, 18, '#c8c2b8', 9) + '<ellipse cx="410" cy="231" rx="40" ry="26" fill="#d8d2c8"/></g>' +
     cloth + drop(560, 350, 18) + drop(620, 385, 13) + drop(700, 345, 15) + sparkle(760, 110, 20))
out('big-w3n-gigitelat-lap', 430, b)

# dokter gigi: dental mirror over the gum, check
mirror = (f'<path d="M640 70 L470 230" stroke="#c8c2b8" stroke-width="22" stroke-linecap="round"/>'
          f'<circle cx="455" cy="248" r="44" fill="{SKY}" stroke="#c8c2b8" stroke-width="12"/><path d="M438 232 Q448 222 462 226" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/>')
b = mouth(260, 260, 190) + mirror.replace('640 70 L470 230', '640 60 L470 200').replace('cx="455" cy="248"', 'cx="455" cy="218"').replace('M438 232 Q448 222 462 226', 'M438 202 Q448 192 462 196') + check(720, 260, 60)
out('big-w3n-gigitelat-dokter', 440, b)


# ---------------- kaki O
def legs(cx, top, s, bow=1.0, bow_r=None):
    """Toddler from the chest down (shirt, diaper, legs, feet), faceless. bow: 0 straight, 1 clearly bowed; bow_r for the right leg."""
    bow_r = bow if bow_r is None else bow_r
    hip = top + s * 1.25
    foot = top + s * 3.0
    o = ''
    for side, bw in ((-1, bow), (1, bow_r)):
        x0 = cx + side * s * 0.28
        knee_x = x0 + side * s * 0.55 * bw
        x1 = cx + side * s * (0.28 + 0.05 * bw)
        o += f'<path d="M{x0} {hip} Q{knee_x} {(hip+foot)/2} {x1} {foot}" stroke="{SKIN}" stroke-width="{s*0.36}" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M{x0+side*s*0.1} {hip+s*0.2} Q{knee_x+side*s*0.08} {(hip+foot)/2} {x1+side*s*0.1} {foot-s*0.1}" stroke="{SKIND}" stroke-width="{s*0.08}" fill="none" stroke-linecap="round" opacity="0.6"/>'
        o += f'<ellipse cx="{x1+side*s*0.14}" cy="{foot+s*0.12}" rx="{s*0.3}" ry="{s*0.15}" fill="{SKIN}"/>'
    shirt = f'<path d="M{cx-s*0.62} {top+s*0.65} Q{cx-s*0.62} {top} {cx} {top} Q{cx+s*0.62} {top} {cx+s*0.62} {top+s*0.65} Z" fill="{SUN}"/>'
    diaper = (f'<path d="M{cx-s*0.66} {top+s*0.55} L{cx+s*0.66} {top+s*0.55} L{cx+s*0.6} {hip+s*0.1} Q{cx} {hip+s*0.45} {cx-s*0.6} {hip+s*0.1} Z" fill="#fff" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
              + rect(cx - s * 0.7, top + s * 0.52, s * 0.3, s * 0.2, SKY, 6) + rect(cx + s * 0.4, top + s * 0.52, s * 0.3, s * 0.2, SKY, 6))
    return o + shirt + diaper


def shoe(cx, cy, s):
    return (f'<path d="M{cx-s} {cy+s*0.35} L{cx-s} {cy-s*0.25} Q{cx-s} {cy-s*0.55} {cx-s*0.6} {cy-s*0.55} L{cx-s*0.2} {cy-s*0.55} Q{cx-s*0.1} {cy-s*0.1} {cx+s*0.5} {cy-s*0.05} Q{cx+s} {cy} {cx+s} {cy+s*0.35} Z" fill="{SKY}"/>'
            + rect(cx - s * 1.05, cy + s * 0.3, s * 2.1, s * 0.2, INK, s * 0.08) +
            f'<path d="M{cx-s*0.45} {cy-s*0.35} L{cx+s*0.05} {cy-s*0.15} M{cx-s*0.4} {cy-s*0.15} L{cx+s*0.15} {cy+s*0.02}" stroke="#fff" stroke-width="{s*0.07}" stroke-linecap="round"/>'
            + rect(cx - s * 0.95, cy + s * 0.12, s * 1.9, s * 0.2, SUN, s * 0.08))


def bundle(cx, cy, s):
    """Tightly wrapped baby lying down, head to the left, legs pulled straight inside a long wrap."""
    o = (f'<path d="M{cx-s*0.9} {cy-s*0.32} L{cx+s*1.3} {cy-s*0.22} Q{cx+s*1.55} {cy} {cx+s*1.3} {cy+s*0.22} L{cx-s*0.9} {cy+s*0.32} Z" fill="{BLUSH}"/>')
    o += f'<circle cx="{cx-s*1.05}" cy="{cy}" r="{s*0.36}" fill="{SKIN}"/>'
    o += f'<path d="M{cx-s*1.38} {cy-s*0.12} Q{cx-s*1.3} {cy-s*0.42} {cx-s*1.0} {cy-s*0.38}" stroke="{BLUSH}" stroke-width="{s*0.14}" fill="none" stroke-linecap="round"/>'
    o += ''.join(f'<path d="M{cx+dx*s} {cy-s*0.32} L{cx+dx*s} {cy+s*0.32}" stroke="{TD}" stroke-width="{s*0.09}" stroke-linecap="round"/>' for dx in (-0.2, 0.4, 1.0))
    o += ''.join(f'<path d="M{cx-s*1.05+dx*s-s*0.07} {cy-s*0.04} Q{cx-s*1.05+dx*s} {cy+s*0.04} {cx-s*1.05+dx*s+s*0.07} {cy-s*0.04}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>' for dx in (-0.13, 0.13))
    o += f'<ellipse cx="{cx-s*1.05}" cy="{cy+s*0.15}" rx="{s*0.07}" ry="{s*0.03}" fill="{TD}"/>'
    return o


alert = f'<path d="M0 -105 L105 75 L-105 75 Z" fill="{TERRA}" stroke="{TERRA}" stroke-width="24" stroke-linejoin="round"/>' + text(0, 58, '!', 130, '#fff')

# hero: bowed legs now, straight later
b = (floor(360, 440) + shadow(220, 425, 120) + legs(220, 70, 110, 1.0) +
     arrow(370, 250, 500) + calendar(370, 80, 130, '2', 'tahun') +
     shadow(660, 425, 110) + legs(660, 70, 110, 0.05) + sparkle(790, 120, 24) + sparkle(540, 330, 14, TERRA))
out('hero-w3n-kaki-o', 440, b)

b = (fl(330, 420, 30, 840) + shadow(170, 400, 90) + legs(170, 50, 95, 1.0) + arrow(320, 230, 470) +
     shadow(650, 400, 90) + legs(650, 50, 95, 0.05))
out('big-w3n-kakio-lurus', 420, b)

b = fl(320, 420, 30, 780) + shadow(380, 330, 280) + bundle(390, 250, 170) + cross(700, 100, 52)
out('big-w3n-kakio-bedong', 420, b)

b = fl(320, 420, 60, 760) + shadow(330, 345, 220) + shoe(330, 240, 170) + cross(640, 90, 52)
out('big-w3n-kakio-sepatu', 420, b)

b = fl(360, 440, 30, 760) + shadow(230, 425, 110) + legs(230, 70, 110, 1.15, 0.05) + f'<g transform="translate(560 200)">{alert}</g>'
out('big-w3n-kakio-dokter', 440, b)

autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 440, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('\n'.join(NAMES))
