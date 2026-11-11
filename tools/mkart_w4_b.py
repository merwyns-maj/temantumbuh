# Scenes for week 4 group B short posts:
#   w4s-susu-uht (plain cow's milk after 1 year), w4s-asip-ml (how many ml of expressed milk per feed),
#   w4s-kolik (rule of 3, tag-team soothing), w4s-gula (added sugar limit, label maths).
# Rules: milk only in glasses, cartons without brands, ASI bags or a small cup. No bottles, teats, pacifiers or formula (PP 28/2024).
# No medicine, drops or oils in the colic art. No brand names anywhere.
# Run: python tools/mkart_w4_b.py [contact-sheet.png]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *
from people import _eyes, _mouth

MILK = '#fbf6ec'; MILKD = '#ece2cf'; GLASS = '#eaf3fa'; GLASSD = '#c3d3e2'; FRD = '#c3d3e2'
CHOC = '#a8714f'; WATER = '#d6ebf8'; SUGAR = '#ffffff'; RICE = '#fbf7ee'; LEAF = '#8fbf7a'


def badge(cx, cy, label, col=SAGE, w=200, ink=CARD, size=38):
    return f'<rect x="{cx-w/2}" y="{cy-32}" width="{w}" height="64" rx="32" fill="{col}"/>' + text(cx, cy + 13, label, size, ink)


def glass(cx, base, h=150, frac=0.8, liquid=MILK, liquid_d=MILKD):
    """Plain tumbler (slightly tapered), liquid to frac of its height."""
    wt, wb = h * 0.62, h * 0.5
    lt = base - h * frac; lw = wb + (wt - wb) * frac
    return (f'<path d="M{cx-wt/2} {base-h} L{cx+wt/2} {base-h} L{cx+wb/2} {base} L{cx-wb/2} {base} Z" fill="{GLASS}" stroke="{GLASSD}" stroke-width="5" stroke-linejoin="round"/>'
            + (f'<path d="M{cx-lw/2+4} {lt} L{cx+lw/2-4} {lt} L{cx+wb/2-4} {base-4} L{cx-wb/2+4} {base-4} Z" fill="{liquid}"/>'
               f'<ellipse cx="{cx}" cy="{lt}" rx="{lw/2-4}" ry="{h*0.04}" fill="{liquid_d}"/>' if frac > 0 else '')
            + f'<path d="M{cx-wt/2+12} {base-h+16} L{cx-wb/2+12} {base-14}" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.8"/>')


def carton(cx, base, s=1.0, body=CARD, band=SKY, label='', label_size=26, cap=SKYD):
    """Generic gable-top carton, no brand. label: one short word on the band."""
    w, h = 120 * s, 200 * s
    x, top = cx - w / 2, base - h
    return (f'<path d="M{x} {top+40*s} L{x+w/2} {top} L{x+w} {top+40*s} Z" fill="{band}"/>'
            f'<rect x="{x+w/2-14*s}" y="{top-18*s}" width="{28*s}" height="{22*s}" rx="{5*s}" fill="{cap}"/>'
            f'<rect x="{x}" y="{top+40*s}" width="{w}" height="{h-40*s}" rx="{8*s}" fill="{body}" stroke="{LINE}" stroke-width="4"/>'
            f'<rect x="{x}" y="{top+90*s}" width="{w}" height="{56*s}" fill="{band}"/>'
            + (text(cx, top + 128 * s, label, label_size * s, INK) if label else ''))


def box_drink(cx, base, s=1.0, col=SUN, cold=SUND, label='', label_size=30):
    """Small rectangular drink box with a straw, no brand."""
    w, h = 110 * s, 170 * s
    x, top = cx - w / 2, base - h
    return (f'<path d="M{cx+18*s} {top} L{cx+30*s} {top-60*s} L{cx+56*s} {top-70*s}" stroke="{TERRA}" stroke-width="{9*s}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="{10*s}" fill="{col}"/>'
            f'<rect x="{x+w*0.62}" y="{top}" width="{w*0.38}" height="{h}" rx="{10*s}" fill="{cold}" opacity="0.45"/>'
            f'<rect x="{x+12*s}" y="{top+50*s}" width="{w-24*s}" height="{60*s}" rx="{8*s}" fill="{CARD}"/>'
            + (text(cx, top + 92 * s, label, label_size * s, INK) if label else ''))


def bag(cx, cy, s=1, rot=0, frac=0.55, label=''):
    """ASI storage bag (same look as w3n-asip-simpan): tapered pouch, zip line, milk to frac, label stripe."""
    top = -70; bot = 76; ml = bot - (bot + 12) * frac * 1.2
    lab = text(0, -26, label, 24, INK) if label else ''
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            f'<path d="M-44 {top} L44 {top} L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="{CARD}" stroke="{FRD}" stroke-width="4"/>'
            f'<path d="M-46 {ml} L46 {ml} L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="#f7ecd6"/>'
            f'<path d="M-44 -54 L44 -54" stroke="{SKYD}" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="-34" y="-46" width="68" height="28" rx="5" fill="{SUN}" opacity="0.85"/>' + lab +
            f'<ellipse cx="-22" cy="{max(ml+30, 30)}" rx="7" ry="14" fill="#fff" opacity="0.5"/></g>')


def cup(cx, base, s=1.0, frac=0.6):
    """Small open cup with a handle (cup feeding), breast milk inside. No teat."""
    w, h = 110 * s, 96 * s
    lt = base - h * frac
    return (f'<path d="M{cx+w/2-6*s} {base-h*0.75} Q{cx+w/2+34*s} {base-h*0.6} {cx+w/2-8*s} {base-h*0.25}" stroke="{SKYD}" stroke-width="{11*s}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx-w/2} {base-h} L{cx+w/2} {base-h} L{cx+w/2-10*s} {base} L{cx-w/2+10*s} {base} Z" fill="{SKY}"/>'
            f'<path d="M{cx-w/2+5*s} {lt} L{cx+w/2-5*s} {lt}" stroke="#f7ecd6" stroke-width="{12*s}" stroke-linecap="round"/>'
            f'<ellipse cx="{cx}" cy="{base-h}" rx="{w/2}" ry="{9*s}" fill="{SKYD}"/><ellipse cx="{cx}" cy="{base-h+2*s}" rx="{w/2-8*s}" ry="{5*s}" fill="#f7ecd6"/>')


def clock(cx, cy, r, hh=3, mm=0, ring=SUND):
    a1 = math.radians((hh % 12) * 30 + mm * 0.5 - 90); a2 = math.radians(mm * 6 - 90)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}" stroke="{ring}" stroke-width="{r*0.11}"/>'
            + ''.join(f'<circle cx="{cx+r*0.78*math.cos(math.radians(i*30))}" cy="{cy+r*0.78*math.sin(math.radians(i*30))}" r="{r*0.04}" fill="{MUTED}"/>' for i in range(12))
            + f'<path d="M{cx} {cy} L{cx+r*0.45*math.cos(a1)} {cy+r*0.45*math.sin(a1)} M{cx} {cy} L{cx+r*0.65*math.cos(a2)} {cy+r*0.65*math.sin(a2)}" stroke="{INK}" stroke-width="{r*0.09}" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.08}" fill="{INK}"/>')


def plate(cx, cy, w=230):
    """Plate of rice, a piece of chicken and greens (a family meal)."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w*0.2}" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>'
            f'<ellipse cx="{cx-w*0.14}" cy="{cy-w*0.05}" rx="{w*0.2}" ry="{w*0.11}" fill="{RICE}" stroke="{LINE}" stroke-width="3"/>'
            f'<ellipse cx="{cx+w*0.17}" cy="{cy-w*0.04}" rx="{w*0.13}" ry="{w*0.07}" fill="{BOX}"/>'
            f'<ellipse cx="{cx+w*0.03}" cy="{cy+w*0.06}" rx="{w*0.11}" ry="{w*0.05}" fill="{LEAF}"/>')


def spoon(cx, cy, s=1.0, rot=0, heap=True):
    """Teaspoon with a heap of sugar."""
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            f'<rect x="30" y="-7" width="110" height="14" rx="7" fill="#b9c3cc"/>'
            f'<ellipse cx="0" cy="0" rx="40" ry="26" fill="#cfd8e0"/><ellipse cx="0" cy="-2" rx="32" ry="19" fill="#e3e9ee"/>'
            + (f'<path d="M-34 -2 Q-24 -40 0 -42 Q24 -40 34 -2 Z" fill="{SUGAR}" stroke="{LINE}" stroke-width="3"/>'
               f'<circle cx="-10" cy="-24" r="3" fill="{LINE}"/><circle cx="8" cy="-16" r="3" fill="{LINE}"/><circle cx="-2" cy="-32" r="2.5" fill="{LINE}"/>' if heap else '')
            + '</g>')


def cross(cx, cy, r, col=TERRA, w=14):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}"/>'
            f'<path d="M{cx-r*0.7} {cy+r*0.7} L{cx+r*0.7} {cy-r*0.7}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


def arrow(x0, y, x1, col=MUTED, w=8):
    return (f'<path d="M{x0} {y} L{x1-14} {y}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x1-26} {y-15} L{x1} {y} L{x1-26} {y+15} Z" fill="{col}"/>')


def baby(cx, cy, s=1.0, expr='nangis', rot=0):
    """Newborn in a blanket (swaddle-shaped bundle, loose at the hips), face only, not photoreal."""
    r = 40 * s
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<path d="M{cx-r*1.15} {cy+r*0.2} Q{cx-r*1.3} {cy+r*2.6} {cx} {cy+r*2.9} Q{cx+r*1.3} {cy+r*2.6} {cx+r*1.15} {cy+r*0.2} Z" fill="{BLUSH}"/>'
            f'<path d="M{cx-r*1.15} {cy+r*0.4} Q{cx} {cy+r*1.5} {cx+r*1.15} {cy+r*0.4}" stroke="#e8a994" stroke-width="{r*0.12}" fill="none"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*1.25}" fill="{BLUSH}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SKIN}"/>'
            + ''.join(f'<ellipse cx="{cx+k*r*0.55}" cy="{cy+r*0.3}" rx="{r*0.17}" ry="{r*0.1}" fill="{CHEEK}" opacity="0.6"/>' for k in (-1, 1))
            + _eyes(cx, cy, r, expr) + _mouth(cx, cy, r, expr) + '</g>')


def cal(x, y, w, h, marked, cols=7, rows=1, col=TERRA, head=SKY):
    """Calendar card: rows x cols cells, `marked` cell indices filled."""
    cw, chh = (w - 30) / cols, (h - 70) / rows
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="18" fill="{head}"/><rect x="{x}" y="{y+26}" width="{w}" height="20" fill="{head}"/>',
           f'<rect x="{x+w*0.25}" y="{y-14}" width="12" height="34" rx="6" fill="{INK}"/><rect x="{x+w*0.75-12}" y="{y-14}" width="12" height="34" rx="6" fill="{INK}"/>']
    for i in range(cols * rows):
        r_, c_ = divmod(i, cols)
        cx_, cy_ = x + 15 + c_ * cw + cw / 2, y + 58 + r_ * chh + chh / 2
        out.append(f'<circle cx="{cx_}" cy="{cy_}" r="{min(cw, chh)*0.36}" fill="{col if i in marked else LINE}"/>')
    return ''.join(out)


def fan(cx, cy, s=1.0):
    """Standing fan with soft sound waves (white noise)."""
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<rect x="-8" y="40" width="16" height="120" rx="8" fill="{SKYD}"/><ellipse cx="0" cy="166" rx="56" ry="14" fill="{SKYD}"/>'
            f'<circle cx="0" cy="0" r="74" fill="{CARD}" stroke="{SKYD}" stroke-width="8"/>'
            + ''.join(f'<ellipse cx="{30*math.cos(math.radians(a))}" cy="{30*math.sin(math.radians(a))}" rx="32" ry="15" fill="{SKY}" transform="rotate({a} {30*math.cos(math.radians(a))} {30*math.sin(math.radians(a))})"/>' for a in (0, 120, 240))
            + f'<circle cx="0" cy="0" r="12" fill="{SKYD}"/>'
            + ''.join(f'<path d="M{90+k*24} {-40+k*-6} Q{108+k*30} 0 {90+k*24} {40+k*6}" stroke="{SAGE}" stroke-width="8" fill="none" stroke-linecap="round" opacity="{1-k*0.25}"/>' for k in range(3))
            + '</g>')


def heart(x, y, s, col=TERRA):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 8 C-14 -8 -30 6 0 30 C30 6 14 -8 0 8 Z" fill="{col}"/>'


def moon(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/><circle cx="{cx+r*0.45}" cy="{cy-r*0.25}" r="{r*0.85}" fill="#3e4f6b"/>'


names = []
def out(name, h, body):
    svg(name, h, body); names.append(name)

# ---------------- w4s-susu-uht ----------------
# HERO: family plate first, two glasses of plain milk beside it, badge "cukup 2 gelas"
b = (floor(470, 560) + shadow(220, 470, 190) + shadow(645, 476, 210) +
     plate(220, 420, 360) + glass(540, 470, 300, 0.82) + glass(765, 470, 300, 0.82) +
     badge(650, 100, 'cukup 2 gelas', SAGE, 330, CARD, 42) + badge(220, 280, 'makan dulu', SUN, 270, INK, 38))
out('hero-w4b-susu-2gelas', 560, b)

icons = {}
cake = (f'<rect x="60" y="170" width="180" height="100" rx="18" fill="{BLUSH}"/><rect x="60" y="170" width="180" height="34" rx="16" fill="{CARD}"/>'
        f'<path d="M60 200 Q90 222 120 200 Q150 222 180 200 Q210 222 240 200" stroke="{CARD}" stroke-width="12" fill="none"/>'
        f'<ellipse cx="150" cy="276" rx="120" ry="16" fill="{LINE}"/>' + text(150, 152, '1', 110, TERRA) +
        f'<path d="M150 18 Q170 40 150 52 Q130 40 150 18 Z" fill="{SUN}"/>')
icons['umur1'] = cake
icons['plain'] = (carton(110, 290, 1.1, CARD, SKY, 'plain', 28) + glass(230, 290, 150, 0.8) )
icons['2gelas'] = glass(80, 280, 190, 0.82) + glass(230, 280, 190, 0.82) + badge(155, 50, '480 ml', SAGE, 190, CARD, 36)
icons['kebanyakan'] = (glass(60, 280, 130, 0.8) + glass(145, 280, 130, 0.8) + glass(230, 280, 130, 0.8) + glass(315, 280, 130, 0.8) +
                       badge(180, 70, 'kebanyakan', TERRA, 260, CARD, 34))
icons['jammakan'] = (plate(120, 220, 210) + glass(275, 270, 150, 0.8) +
                     f'<circle cx="60" cy="80" r="30" fill="{SUN}"/>' + text(60, 93, '1', 36, INK) +
                     f'<circle cx="275" cy="80" r="30" fill="{SAGE}"/>' + text(275, 93, '2', 36, CARD))
for k, body in icons.items():
    out(f'big-w4b-susu-{k}', 320, body)

# ---------------- w4s-asip-ml ----------------
b = (floor(470, 560) + shadow(300, 474, 160) + shadow(620, 474, 130) +
     bag(300, 290, 2.4, -4, 0.7, '') + cup(620, 470, 2.0, 0.6) + clock(760, 130, 80, 10, 10) +
     badge(300, 60, '90-120 ml', SAGE, 300, CARD, 42) + badge(620, 230, 'sekali minum', SUN, 280, INK, 36))
out('hero-w4b-asip-ml', 560, b)

icons = {}
icons['hari1'] = (spoon(110, 200, 1.4, -10, False) + f'<path d="M110 140 Q124 164 110 176 Q96 164 110 140 Z" fill="#f2e2c0"/>' + badge(150, 60, '5 ml', SUN, 150, INK, 36))
icons['hari3'] = cup(130, 280, 1.2, 0.35) + badge(170, 60, '15-30 ml', SUN, 230, INK, 34)
icons['minggu1'] = bag(150, 190, 1.0, -3, 0.35) + badge(150, 40, 's.d. 60 ml', SUN, 230, INK, 34)
icons['bulan'] = bag(150, 190, 1.0, 3, 0.72) + badge(150, 40, '90-120 ml', SAGE, 240, CARD, 34)
icons['perjam'] = clock(110, 160, 92, 1, 0) + f'<path d="M250 110 Q282 160 250 186 Q218 160 250 110 Z" fill="#f2e2c0" stroke="{MILKD}" stroke-width="4"/>' + badge(240, 250, '30 ml', SAGE, 150, CARD, 34)
icons['pergi'] = (f'<rect x="20" y="130" width="180" height="130" rx="18" fill="{BOX}"/><rect x="20" y="170" width="180" height="16" fill="{BOXD}"/>'
                  f'<path d="M80 130 L80 104 Q80 92 92 92 L128 92 Q140 92 140 104 L140 130" stroke="{BOXD}" stroke-width="12" fill="none"/>'
                  + clock(240, 110, 62, 10, 0) + badge(160, 296, '10 jam', SUN, 170, INK, 34))
icons['bagi'] = bag(70, 170, 0.75, -6, 0.7) + bag(160, 170, 0.75, 2, 0.7) + bag(250, 170, 0.75, 6, 0.7) + badge(160, 300, '3 kali', SAGE, 170, CARD, 34)
icons['kecil'] = bag(95, 190, 0.8, -5, 0.45) + bag(215, 190, 0.8, 5, 0.45) + badge(155, 40, '50-100 ml', SUN, 240, INK, 34)
for k, body in icons.items():
    out(f'big-w4b-asip-{k}', 330, body)

# ---------------- w4s-kolik ----------------
# HERO: evening window, Ayah calmly holding a crying newborn, badge "3-4 bulan"
T, H = 470, 560
y = seat('ayah', 2.0, T, True)
b = (f'<rect x="20" y="40" width="200" height="220" rx="20" fill="#3e4f6b"/><rect x="20" y="145" width="200" height="10" fill="{CARD}"/><rect x="115" y="40" width="10" height="220" fill="{CARD}"/>'
     + moon(70, 95, 30) + ''.join(f'<circle cx="{x}" cy="{yy}" r="4" fill="{CARD}"/>' for x, yy in ((180, 70), (195, 120), (170, 210), (60, 220)))
     + person('ayah', 440, y, 2.0, 'lembut', 'pegang') + baby(440, y + 190, 1.45, 'nangis', -8) + table(T, H)
     + badge(720, 60, 'reda 3-4 bulan', SAGE, 300, CARD, 38) + clock(760, 230, 70, 6, 30))
out('hero-w4b-kolik-ayah', H, b)

icons = {}
icons['3jam'] = clock(150, 150, 110, 3, 0) + f'<path d="M150 150 L150 50 A100 100 0 0 1 237 200 Z" fill="{TERRA}" opacity="0.3"/>' + badge(150, 300, '3 jam', TERRA, 170, CARD, 34)
icons['3hari'] = cal(20, 60, 270, 150, {1, 3, 5}, 7, 1) + badge(155, 270, '3 hari', TERRA, 170, CARD, 34)
icons['3minggu'] = cal(20, 30, 270, 210, {0, 1, 2, 7, 8, 9, 14, 15, 16}, 7, 3, TERRA) + badge(155, 290, '3 minggu', TERRA, 210, CARD, 34)
icons['sehat'] = (baby(150, 120, 1.3, 'senang') + heart(250, 60, 1.6) + heart(50, 80, 1.0, SUN))
icons['gendong'] = (f'<path d="M60 280 Q60 140 150 120 Q240 140 240 280 Z" fill="{SAGE}"/>'
                    f'<path d="M100 130 L100 280 M200 130 L200 280" stroke="{SD}" stroke-width="16" stroke-linecap="round"/>'
                    + baby(150, 110, 1.05, 'lembut'))
icons['ayun'] = (f'<path d="M50 70 Q150 20 250 70" stroke="{SAGE}" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="2 22"/>'
                 f'<path d="M228 52 L254 72 L224 86" stroke="{SAGE}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 + baby(150, 150, 1.15, 'lembut', 14))
icons['sshh'] = fan(110, 120, 1.0)
icons['pangkuan'] = (f'<rect x="30" y="200" width="250" height="70" rx="35" fill="{SKYD}"/><rect x="30" y="150" width="250" height="70" rx="35" fill="{SKY}"/>'
                     + f'<g transform="rotate(-90 160 130)">' + baby(160, 60, 0.95, 'lembut') + '</g>'
                     + f'<ellipse cx="190" cy="80" rx="42" ry="22" fill="{SKIN}"/>'
                     + ''.join(f'<path d="M{150+k*30} 40 q10 -10 20 0" stroke="{MUTED}" stroke-width="6" fill="none" stroke-linecap="round"/>' for k in range(3)))
for k, body in icons.items():
    out(f'big-w4b-kolik-{k}', 330, body)

# ---------------- w4s-gula ----------------
# HERO: six teaspoons of sugar in a row, badge "maks 6 sendok teh", generic drink box
b = (floor(470, 560) + shadow(440, 480, 400) +
     ''.join(spoon(110 + i * 125, 430 - (i % 2) * 22, 1.45, -60) for i in range(6)) +
     badge(440, 50, 'maks 6 sendok teh', SAGE, 440, CARD, 42) + badge(440, 130, '2 tahun ke atas', SUN, 330, INK, 36))
out('hero-w4b-gula-6sdt', 560, b)

icons = {}
label_card = (f'<rect x="20" y="20" width="270" height="270" rx="18" fill="{CARD}" stroke="{INK}" stroke-width="6"/>'
              f'<rect x="20" y="20" width="270" height="50" rx="16" fill="{INK}"/><rect x="20" y="50" width="270" height="20" fill="{INK}"/>'
              + text(155, 56, 'nilai gizi', 28, CARD) +
              ''.join(f'<rect x="40" y="{90+i*40}" width="{120-i*14}" height="14" rx="7" fill="{LINE}"/><rect x="{230-i*6}" y="{90+i*40}" width="{40+i*6}" height="14" rx="7" fill="{LINE}"/>' for i in range(2)))
icons['label'] = label_card + f'<rect x="32" y="170" width="246" height="56" rx="12" fill="{SUN}"/>' + text(46, 210, 'Gula', 32, INK, 'start') + text(266, 210, '20 g', 32, INK, 'end') + f'<rect x="40" y="246" width="100" height="14" rx="7" fill="{LINE}"/>'
icons['sajian'] = box_drink(80, 290, 1.0) + box_drink(190, 290, 1.0, SKY, SKYD) + badge(250, 70, 'x2', TERRA, 110, CARD, 40)
icons['bagi4'] = badge(150, 70, '20 g : 4', SUN, 230, INK, 40) + ''.join(spoon(60 + i * 60, 220, 0.62, -60) for i in range(5)) + badge(150, 300, '= 5 sdt', SAGE, 200, CARD, 34)
icons['nol'] = (plate(150, 200, 230) + spoon(230, 90, 0.9, -30) + cross(230, 80, 62))
icons['airputih'] = box_drink(70, 270, 0.9) + arrow(140, 180, 200) + glass(255, 270, 170, 0.75, WATER, '#b9d8ee')
icons['susuplain'] = carton(65, 285, 0.9, CHOC, '#c99273', '', cap='#8a5a3e') + arrow(130, 190, 185) + carton(245, 285, 0.9, CARD, SKY, 'plain', 28)
icons['buah'] = (biscuit(60, 170, 1.4) + arrow(120, 170, 175) +
                 f'<path d="M190 140 A60 60 0 0 1 300 140 Z" fill="#f4a259"/><path d="M200 140 A50 50 0 0 1 290 140" fill="none" stroke="#fde3c4" stroke-width="6"/>'
                 f'<path d="M196 230 Q250 270 300 200 Q260 240 200 214 Z" fill="{SUN}"/>')
icons['grup'] = (f'<rect x="80" y="10" width="150" height="280" rx="24" fill="{INK}"/><rect x="92" y="34" width="126" height="226" rx="10" fill="#eaf4ec"/>'
                 f'<rect x="102" y="54" width="90" height="34" rx="12" fill="{CARD}"/><rect x="122" y="104" width="86" height="34" rx="12" fill="#cfe9c9"/>'
                 f'<rect x="102" y="154" width="70" height="34" rx="12" fill="{CARD}"/>' + heart(150, 200, 1.4) + heart(250, 60, 1.1, SUN))
for k, body in icons.items():
    out(f'big-w4b-gula-{k}', 320, body)

autocrop(names)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=360))).convert('RGBA') for n in names]
    ims = [i.resize((360, 360)) if i.size[1] > 360 else i for i in ims]
    h = max(i.size[1] for i in ims); cols = 6; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (360 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 360, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(names))
