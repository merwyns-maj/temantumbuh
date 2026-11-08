# Scenes for w3n-asip-simpan (how long expressed breast milk keeps: room, cooler bag, fridge, 1-door and 2-door freezer, thawed).
# Milk is drawn in ASI storage bags only: no bottles, teats or formula (PP 28/2024).
# Run: python tools/mkart_w3_asip.py [contact-sheet.png]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

MILK = '#f7ecd6'; MILKD = '#ead7b4'; FROST = '#e3f0fa'; FR = '#e6eef5'; FRD = '#c3d3e2'; ICE = '#bfe0f2'

def bag(cx, cy, s=1, rot=0, frozen=False):
    """ASI storage bag: tapered pouch, zip line, milk to two-thirds, label stripe."""
    fill = '#eef6fb' if frozen else MILK
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
            f'<path d="M-44 -70 L44 -70 L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="{CARD}" stroke="{FRD}" stroke-width="4"/>'
            f'<path d="M-46 -12 L46 -12 L48 60 Q48 76 32 76 L-32 76 Q-48 76 -48 60 Z" fill="{fill}"/>'
            f'<path d="M-44 -54 L44 -54" stroke="{SKYD}" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="-30" y="-40" width="60" height="18" rx="4" fill="{SUN}" opacity="0.8"/>'
            + (f'<path d="M-30 20 l10 -10 M-6 34 l12 -12 M20 18 l10 -10" stroke="#fff" stroke-width="4" stroke-linecap="round"/>' if frozen else
               f'<ellipse cx="-20" cy="20" rx="8" ry="18" fill="#fff" opacity="0.5"/>') + '</g>')

def badge(cx, cy, label, col=SAGE, w=200, ink=CARD, size=38):
    return f'<rect x="{cx-w/2}" y="{cy-32}" width="{w}" height="64" rx="32" fill="{col}"/>' + text(cx, cy + 13, label, size, ink)

def fridge1(x, y, w=230, h=400, open_freezer=True):
    """Single-door fridge with the small freezer box inside (door open)."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{FR}"/>'
            f'<rect x="{x+18}" y="{y+18}" width="{w-36}" height="{h-36}" rx="12" fill="#f8fbfe"/>'
            f'<rect x="{x+30}" y="{y+30}" width="{w-60}" height="110" rx="10" fill="{FROST}" stroke="{FRD}" stroke-width="4"/>'
            + ''.join(f'<path d="M{x+44+i*30} {y+34} l6 12 l6 -12" stroke="#fff" stroke-width="4" fill="none"/>' for i in range(5))
            + f'<rect x="{x+18}" y="{y+230}" width="{w-36}" height="8" fill="{FRD}"/><rect x="{x+18}" y="{y+320}" width="{w-36}" height="8" fill="{FRD}"/>')

def fridge2(x, y, w=250, h=440):
    """Two-door fridge, top freezer door ajar."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{FR}"/>'
            f'<rect x="{x}" y="{y+150}" width="{w}" height="10" fill="{FRD}"/>'
            f'<rect x="{x+w-36}" y="{y+40}" width="12" height="70" rx="6" fill="#b5c7d8"/><rect x="{x+w-36}" y="{y+190}" width="12" height="100" rx="6" fill="#b5c7d8"/>'
            f'<rect x="{x+20}" y="{y+20}" width="{w-80}" height="112" rx="10" fill="{FROST}"/>')

def thermo(x, y, col=TERRA, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-16" y="-90" width="32" height="130" rx="16" fill="{CARD}" stroke="{FRD}" stroke-width="5"/>'
            f'<rect x="-7" y="-40" width="14" height="80" rx="7" fill="{col}"/><circle cx="0" cy="56" r="26" fill="{col}"/></g>')

def clock(cx, cy, r, label):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CARD}" stroke="{SUND}" stroke-width="10"/>'
            f'<path d="M{cx} {cy} L{cx} {cy-r*0.6} M{cx} {cy} L{cx+r*0.45} {cy+r*0.2}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="8" fill="{INK}"/>' + badge(cx, cy + r + 46, label, SUN, 170, INK, 34))

# HERO: 1-door fridge (2 minggu) next to 2-door fridge (3-6 bulan)
b = (shadow(220, 556, 190) + shadow(650, 556, 200) +
     fridge1(70, 120, 300, 430) + bag(150, 186, 0.5, -6, True) + bag(220, 186, 0.5, 4, True) + bag(290, 186, 0.5, -2, True) +
     fridge2(490, 100, 320, 450) + bag(560, 172, 0.56, -6, True) + bag(640, 172, 0.56, 5, True) +
     badge(220, 60, 'cuma 2 minggu', TERRA, 300) + badge(650, 40, 'bisa 3-6 bulan', SAGE, 310) +
     text(220, 610, 'kulkas 1 pintu', 38, INK) + text(650, 610, 'kulkas 2 pintu', 38, INK))
svg('hero-w3n-asip-freezer', 640, b)

S = 300  # icon box
icons = {}
icons['ruang'] = (bag(110, 170, 1.1) + thermo(230, 170, TERRA, 1.0) +
                  f'<circle cx="250" cy="40" r="26" fill="{SUN}"/>' + ''.join(f'<path d="M{250+38*__import__("math").cos(a)} {40+38*__import__("math").sin(a)} L{250+52*__import__("math").cos(a)} {40+52*__import__("math").sin(a)}" stroke="{SUN}" stroke-width="7" stroke-linecap="round"/>' for a in [i*0.785 for i in range(8)]))
icons['cooler'] = (f'<rect x="30" y="90" width="240" height="180" rx="26" fill="{SKY}"/><rect x="30" y="90" width="240" height="44" rx="22" fill="{SKYD}"/>'
                   f'<path d="M100 90 Q100 30 150 30 Q200 30 200 90" stroke="{SKYD}" stroke-width="14" fill="none" stroke-linecap="round"/>'
                   + bag(110, 196, 0.62, -6) + bag(180, 196, 0.62, 6) + f'<rect x="210" y="160" width="46" height="80" rx="10" fill="{ICE}" stroke="#fff" stroke-width="4"/>')
icons['kulkas'] = (f'<rect x="40" y="20" width="220" height="270" rx="20" fill="{FR}"/><rect x="56" y="36" width="188" height="238" rx="10" fill="#f8fbfe"/>'
                   f'<rect x="56" y="150" width="188" height="7" fill="{FRD}"/>' + bag(120, 110, 0.5) + bag(170, 110, 0.5, 5) +
                   f'<path d="M210 230 L150 230" stroke="{SAGE}" stroke-width="10" stroke-linecap="round"/><path d="M170 210 L146 230 L170 250" stroke="{SAGE}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
icons['1pintu'] = fridge1(40, 0, 220, 300) + bag(110, 58, 0.38, -6, True) + bag(150, 58, 0.38, 4, True) + bag(190, 58, 0.38, -2, True)
icons['2pintu'] = fridge2(40, 0, 230, 300) + bag(90, 60, 0.42, -6, True) + bag(140, 60, 0.42, 5, True) + bag(190, 60, 0.42, -3, True)
icons['cair'] = (f'<rect x="40" y="20" width="220" height="270" rx="20" fill="{FR}"/><rect x="56" y="36" width="188" height="238" rx="10" fill="#f8fbfe"/>'
                 + bag(150, 120, 0.8) + badge(150, 238, '24 jam', SUN, 170, INK, 34))
icons['hangat'] = (bag(150, 110, 0.9, -8) +
                   f'<path d="M30 170 L270 170 Q262 290 150 290 Q38 290 30 170 Z" fill="{SKY}"/><path d="M30 170 L270 170 L266 196 L34 196 Z" fill="{SKYD}" opacity="0.6"/>'
                   + ''.join(f'<path d="M{x} 30 q-14 -16 0 -32 q14 -16 0 -32" stroke="{MUTED}" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.5" transform="translate(0 60)"/>' for x in (60, 240)))
icons['sisa'] = clock(150, 120, 100, '2 jam')
icons['beku'] = (f'<rect x="40" y="40" width="220" height="200" rx="20" fill="{FROST}" stroke="{FRD}" stroke-width="6"/>' + bag(150, 140, 0.8, 0, False) +
                 f'<circle cx="150" cy="140" r="118" fill="none" stroke="{TERRA}" stroke-width="16"/><path d="M68 222 L232 58" stroke="{TERRA}" stroke-width="16" stroke-linecap="round"/>')
for k, body in icons.items():
    svg(f'big-w3n-asip-{k}', 320, body)

names = ['hero-w3n-asip-freezer'] + [f'big-w3n-asip-{k}' for k in icons]
autocrop(names)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=360))).convert('RGBA') for n in names]
    h = max(i.size[1] for i in ims); cols = 5; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (360 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 360, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok')
