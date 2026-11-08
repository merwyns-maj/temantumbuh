# Scenes for w3e-gelar-dokter-anak (what Sp.A, Subsp.xx and (K) mean on a pediatrician's name).
# No real doctor names: the plate says "dr. Nama Dokter". Icons are generic organs and objects, no bottles or formula.
# Run: python tools/mkart_w3_gelar.py [contact-sheet.png]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

H, T = 520, 440
PLUM = '#b48bb0'

def plate(x, y, w, h, name_size=30, code_size=44):
    """Doctor's name plate on the wall: 'dr. Nama Dokter' and 'Sp.A, Subsp.AI' with the Subsp part highlighted."""
    return (f'<rect x="{x+5}" y="{y+8}" width="{w}" height="{h}" rx="22" fill="#000" opacity="0.08"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{CARD}" stroke="{LINE}" stroke-width="4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="22" fill="{SAGE}"/><rect x="{x}" y="{y+30}" width="{w}" height="24" fill="{SAGE}"/>'
            + text(x + w / 2, y + 38, 'RUANG PRAKTIK', 26, CARD)
            + text(x + w / 2, y + 112, 'dr. Nama Dokter,', name_size, MUTED)
            + f'<rect x="{x+w*0.43}" y="{y+136}" width="{w*0.5}" height="{code_size+8}" rx="10" fill="{SUN}" opacity="0.75"/>'
            + text(x + w * 0.07, y + 132 + code_size, 'Sp.A,', code_size, INK, 'start')
            + text(x + w * 0.46, y + 132 + code_size, 'Subsp.AI', code_size, INK, 'start'))

def arrow(x0, y, x1, col=MUTED):
    return (f'<path d="M{x0} {y} L{x1-14} {y}" stroke="{col}" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M{x1-28} {y-16} L{x1} {y} L{x1-28} {y+16} Z" fill="{col}"/>')

# HERO: name plate on the left, Mama holding Adek wondering what Subsp.AI means
m = seat('mama', 1.45, T); a = seat('adek', 1.12, T)
b = (plate(16, 150, 430, 240) +
     person('adek', 800, a, 1.12, 'senang', 'none') + person('mama', 630, m, 1.45, 'lembut', 'peluk') + table(T, H) +
     bubble(470, 8, 330, ['"Subsp.AI', 'itu apa ya?"'], 'br', size=36, think=True))
svg('hero-w3e-gelar-pintu', H, b)

# HOW TO READ: three chips Sp.A / Subsp.AI / (K) with what each means underneath
def chip(cx, y, w, label, col, sub1, sub2):
    return (f'<rect x="{cx-w/2+4}" y="{y+6}" width="{w}" height="96" rx="48" fill="#000" opacity="0.08"/>'
            f'<rect x="{cx-w/2}" y="{y}" width="{w}" height="96" rx="48" fill="{col}"/>' + text(cx, y + 64, label, 50, INK) +
            f'<path d="M{cx} {y+110} L{cx} {y+158}" stroke="{MUTED}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M{cx-14} {y+146} L{cx} {y+166} L{cx+14} {y+146}" stroke="{MUTED}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            + text(cx, y + 214, sub1, 36, INK) + text(cx, y + 256, sub2, 30, MUTED))
b = (f'<rect x="10" y="40" width="860" height="440" rx="30" fill="{CARD}" stroke="{LINE}" stroke-width="4"/>' +
     text(440, 112, 'dr. Nama Dokter,', 38, MUTED) +
     chip(170, 150, 220, 'Sp.A', SKY, 'dokter anak', 'spesialis') +
     chip(450, 150, 300, 'Subsp.AI', SUN, 'bidangnya', 'alergi, imun') +
     chip(720, 150, 160, '(K)', '#a9cdb5', 'konsultan', 'kadang ada'))
svg('big-w3e-baca-gelar', H, b)

# ROW ICONS, one per subspecialty (drawn in a ~300px box)
def peanut(cx, cy, s=1, rot=-30):
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})"><ellipse cx="-30" cy="0" rx="36" ry="30" fill="#dcb57c"/><ellipse cx="30" cy="0" rx="36" ry="30" fill="#dcb57c"/>'
            f'<rect x="-30" y="-18" width="60" height="36" fill="#dcb57c"/>'
            + ''.join(f'<path d="M{x} -18 L{x+2} 18" stroke="#bf9356" stroke-width="4" stroke-linecap="round"/>' for x in (-44, -24, 24, 44)) + '</g>')
icons = {}
icons['ai'] = (f'<path d="M150 30 L250 66 L250 150 Q250 230 150 276 Q50 230 50 150 L50 66 Z" fill="{SKY}"/>'
               f'<path d="M150 30 L250 66 L250 150 Q250 230 150 276 Z" fill="{SKYD}" opacity="0.5"/>' + peanut(150, 160, 1.15))
icons['gh'] = (f'<path d="M120 40 Q120 100 150 110 Q250 120 250 200 Q250 280 160 280 Q80 280 70 220 Q64 180 100 170 Q130 160 120 120 Q110 80 100 40 Z" fill="{TERRA}"/>'
               f'<path d="M150 150 Q210 160 210 205" stroke="{TD}" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>'
               f'<rect x="96" y="20" width="28" height="40" rx="12" fill="{BLUSH}"/>')
foot = lambda x, y, s, rot: (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><ellipse cx="0" cy="0" rx="26" ry="44" fill="{SUN}"/>'
                             + ''.join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="{SUN}"/>' for dx, dy, r in ((-20, -56, 9), (-4, -62, 8), (10, -60, 7), (21, -54, 6), (29, -45, 5))) + '</g>')
icons['tkps'] = (foot(80, 230, 1.1, -10) + foot(150, 150, 1.1, 8) + foot(220, 80, 1.1, -10) +
                 f'<path d="M40 280 L260 280" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>')
icons['resp'] = (f'<rect x="140" y="20" width="20" height="100" rx="10" fill="{SKYD}"/>'
                 f'<path d="M140 110 Q110 120 104 140 M160 110 Q190 120 196 140" stroke="{SKYD}" stroke-width="16" fill="none" stroke-linecap="round"/>'
                 f'<path d="M130 120 Q60 100 40 200 Q30 270 90 276 Q130 280 136 240 Z" fill="{SKY}"/>'
                 f'<path d="M170 120 Q240 100 260 200 Q270 270 210 276 Q170 280 164 240 Z" fill="{SKY}"/>')
icons['npm'] = (f'<rect x="40" y="200" width="220" height="70" rx="20" fill="{SAGE}"/><path d="M30 190 Q150 150 270 190 L270 205 L30 205 Z" fill="{SD}"/>'
                f'<circle cx="150" cy="235" r="26" fill="{CARD}"/><path d="M150 235 L166 220" stroke="{TERRA}" stroke-width="6" stroke-linecap="round"/>'
                f'<circle cx="150" cy="110" r="56" fill="{BLUSH}"/><circle cx="150" cy="110" r="38" fill="#f3cba5"/>'
                f'<circle cx="137" cy="106" r="5" fill="{INK}"/><circle cx="163" cy="106" r="5" fill="{INK}"/><path d="M140 124 Q150 132 160 124" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>')
icons['neuro'] = (f'<path d="M150 60 Q100 30 70 70 Q30 80 40 130 Q20 170 60 200 Q70 250 130 240 Q150 260 170 240 Q230 250 240 200 Q280 170 260 130 Q270 80 230 70 Q200 30 150 60 Z" fill="{BLUSH}"/>'
                  f'<path d="M150 62 L150 238" stroke="#e8a994" stroke-width="7" stroke-linecap="round"/>'
                  f'<path d="M80 110 Q110 100 120 130 M70 170 Q100 160 120 185 M230 110 Q190 100 180 130 M230 170 Q200 160 180 185" stroke="#e8a994" stroke-width="7" fill="none" stroke-linecap="round"/>'
                  f'<path d="M110 270 L140 270 L150 250 L162 292 L172 270 L200 270" stroke="{SUND}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
icons['kardio'] = (f'<path d="M150 90 Q120 30 70 50 Q20 80 50 150 Q80 210 150 260 Q220 210 250 150 Q280 80 230 50 Q180 30 150 90 Z" fill="{TERRA}"/>'
                   f'<path d="M150 90 Q180 30 230 50 Q280 80 250 150 Q220 210 150 260 Z" fill="{TD}" opacity="0.35"/>'
                   f'<path d="M60 150 L110 150 L125 120 L145 185 L162 140 L172 150 L240 150" stroke="{CARD}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
kidney = lambda x, flip: (f'<g transform="translate({x} 140) scale({-1 if flip else 1} 1)"><path d="M10 -100 Q80 -100 80 0 Q80 100 10 100 Q-40 100 -40 60 Q-40 34 -12 22 Q6 0 -12 -22 Q-40 -34 -40 -60 Q-40 -100 10 -100 Z" fill="{TD}"/>'
                          f'<ellipse cx="34" cy="-30" rx="14" ry="26" fill="#fff" opacity="0.25"/>'
                          f'<path d="M-14 0 Q-40 10 -40 160" stroke="{SKYD}" stroke-width="10" fill="none" stroke-linecap="round"/></g>')
icons['nefro'] = kidney(70, True) + kidney(240, False)
icons['end'] = (f'<rect x="60" y="20" width="70" height="270" rx="14" fill="{SUN}"/>'
                + ''.join(f'<path d="M60 {40+i*26} L{90 if i % 2 else 104} {40+i*26}" stroke="{SUND}" stroke-width="6" stroke-linecap="round"/>' for i in range(10))
                + f'<path d="M200 270 L200 70" stroke="{SAGE}" stroke-width="16" stroke-linecap="round"/><path d="M160 110 L200 56 L240 110" stroke="{SAGE}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
icons['honk'] = (f'<path d="M140 20 Q80 120 80 180 Q80 260 140 260 Q200 260 200 180 Q200 120 140 20 Z" fill="{TERRA}"/>'
                 f'<ellipse cx="116" cy="180" rx="14" ry="26" fill="#fff" opacity="0.35"/>'
                 f'<circle cx="236" cy="220" r="44" fill="{PLUM}" opacity="0.75"/><circle cx="236" cy="220" r="26" fill="{PLUM}"/>')
icons['ipt'] = (f'<rect x="120" y="20" width="56" height="200" rx="28" fill="{CARD}" stroke="{LINE}" stroke-width="6"/>'
                f'<rect x="136" y="90" width="24" height="140" rx="12" fill="{TERRA}"/><circle cx="148" cy="250" r="40" fill="{TERRA}"/>'
                + ''.join(f'<path d="M176 {50+i*30} L196 {50+i*30}" stroke="{MUTED}" stroke-width="5" stroke-linecap="round"/>' for i in range(5))
                + f'<g transform="translate(250 90)"><ellipse cx="0" cy="0" rx="22" ry="9" fill="{INK}"/><circle cx="-24" cy="-2" r="7" fill="{INK}"/>'
                  f'<path d="M-30 -2 L-50 4" stroke="{INK}" stroke-width="3"/><ellipse cx="2" cy="-16" rx="16" ry="8" fill="{SKY}" opacity="0.8"/>'
                  f'<path d="M-8 6 L-18 26 M2 8 L0 28 M12 6 L20 26" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>')
icons['neo'] = (f'<path d="M70 150 Q70 90 150 90 Q240 90 250 170 Q256 250 160 262 Q80 270 70 200 Z" fill="{BLUSH}"/>'
                f'<path d="M90 190 Q160 160 240 200" stroke="#e8a994" stroke-width="8" fill="none" stroke-linecap="round"/>'
                f'<circle cx="130" cy="120" r="56" fill="#f3cba5"/><path d="M80 100 Q130 40 184 100 Q170 70 130 66 Q92 68 80 100 Z" fill="{SKY}"/>'
                f'<path d="M110 126 Q118 132 126 126 M140 126 Q148 132 156 126" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<ellipse cx="104" cy="142" rx="10" ry="6" fill="{CHEEK}" opacity="0.6"/><ellipse cx="160" cy="142" rx="10" ry="6" fill="{CHEEK}" opacity="0.6"/>')
for k, body in icons.items():
    svg(f'big-w3e-subsp-{k}', 310, body)

# ROUTE: faskes 1 -> Sp.A -> Subsp., and an IGD badge for emergencies
def stop(cx, y, label, col, glyph):
    return (f'<rect x="{cx-110+4}" y="{y+6}" width="220" height="200" rx="28" fill="#000" opacity="0.07"/>'
            f'<rect x="{cx-110}" y="{y}" width="220" height="200" rx="28" fill="{col}"/>' + glyph + text(cx, y + 180, label, 36, INK))
house = lambda cx, y: (f'<path d="M{cx-60} {y+80} L{cx} {y+30} L{cx+60} {y+80} Z" fill="{TD}"/><rect x="{cx-46}" y="{y+78}" width="92" height="62" fill="{CARD}"/>'
                       f'<rect x="{cx-14}" y="{y+100}" width="28" height="40" fill="{BOX}"/>')
hosp = lambda cx, y: (f'<rect x="{cx-56}" y="{y+30}" width="112" height="110" rx="8" fill="{CARD}"/>'
                      f'<rect x="{cx-10}" y="{y+48}" width="20" height="52" fill="{TERRA}"/><rect x="{cx-26}" y="{y+64}" width="52" height="20" fill="{TERRA}"/>'
                      f'<rect x="{cx-14}" y="{y+108}" width="28" height="32" fill="{SKYD}"/>')
star = lambda cx, y: (f'<circle cx="{cx}" cy="{y+86}" r="62" fill="{CARD}"/>' + text(cx, y + 100, 'Subsp.', 32, INK))
b = (stop(130, 30, 'Faskes 1', '#a9cdb5', house(130, 30)) + arrow(250, 130, 316) +
     stop(440, 30, 'Sp.A', SKY, hosp(440, 30)) + arrow(560, 130, 626) +
     stop(750, 30, 'Rujukan', SUN, star(750, 30)) +
     f'<rect x="120" y="300" width="640" height="110" rx="55" fill="{TERRA}"/>'
     f'<circle cx="196" cy="355" r="36" fill="{CARD}"/><rect x="188" y="333" width="16" height="44" fill="{TERRA}"/><rect x="174" y="347" width="44" height="16" fill="{TERRA}"/>'
     + text(500, 370, 'Darurat? Langsung IGD', 40, CARD))
svg('big-w3e-alur-rujuk', 440, b)

names = ['hero-w3e-gelar-pintu', 'big-w3e-baca-gelar', 'big-w3e-alur-rujuk'] + [f'big-w3e-subsp-{k}' for k in icons]
autocrop(names)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in names]
    ims = [i.resize((440, min(i.size[1], 440))) if i.size[1] > 440 else i for i in ims]
    h = max(i.size[1] for i in ims); cols = 5; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 440, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok')
