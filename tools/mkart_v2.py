# Design v2 scenes: bigger, two-tone shading, floor shadows, Tunas inside the scene.
# hero-*.svg 880x420 (hook slide), big-*.svg 880x500 (point slides). Run: python tools/mkart_v2.py
import base64, io, os
import cairosvg
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'design/svg/food')
INK='#4a3f35'; MUTED='#7a6c5f'; TERRA='#e07856'; TD='#c46040'; SAGE='#7fa98f'; SD='#5f8a70'; SUN='#f3c45f'; SUND='#d9a63c'
BLUSH='#f6cdbd'; SKY='#9cc3e6'; SKYD='#7aa6cf'; CARD='#fffdf9'; BOX='#d9a874'; BOXD='#b9844f'; LINE='#e9dccb'; FLOOR='#f1e4d0'
def tunas(pose, w, h, x, y, flip=False):
    png = cairosvg.svg2png(url=os.path.join(ROOT, f'design/svg/tunas/tunas-{pose}.svg'), output_width=w * 2, output_height=h * 2)
    b = base64.b64encode(png).decode()
    tr = f' transform="translate({2*x+w} 0) scale(-1 1)"' if flip else ''
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{b}"{tr}/>'
def shadow(cx, cy, rx, ry=None): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry or rx*0.16}" fill="#000" opacity="0.07"/>'
def floor(y, H): return f'<rect x="0" y="{y}" width="880" height="{H-y}" rx="24" fill="{FLOOR}"/>'
def text(x,y,s,size,col,anchor='middle',rot=0): return f'<text x="{x}" y="{y}" font-family="sans-serif" font-weight="800" font-size="{size}" text-anchor="{anchor}" fill="{col}" transform="rotate({rot} {x} {y})">{s}</text>'
def chair(x, y):  # high chair, side view, seat top at y
    return (f'<path d="M{x+20} {y+40} L{x-10} {y+250} M{x+130} {y+40} L{x+160} {y+250}" stroke="{BOXD}" stroke-width="16" stroke-linecap="round"/>'
            f'<rect x="{x}" y="{y}" width="150" height="46" rx="14" fill="{BOX}"/><rect x="{x}" y="{y+30}" width="150" height="16" rx="8" fill="{BOXD}"/>'
            f'<rect x="{x+118}" y="{y-120}" width="30" height="140" rx="12" fill="{BOX}"/><rect x="{x+134}" y="{y-120}" width="14" height="140" rx="7" fill="{BOXD}"/>'
            f'<rect x="{x-60}" y="{y-34}" width="150" height="20" rx="10" fill="{SKY}"/><rect x="{x-60}" y="{y-22}" width="150" height="8" rx="4" fill="{SKYD}"/>')
def bowl(cx, cy, w, f, fd, rot=0):
    h = w * 0.45
    return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx-w/2} {cy} Q{cx-w/2} {cy+h} {cx} {cy+h} Q{cx+w/2} {cy+h} {cx+w/2} {cy} Z" fill="{f}"/>'
            f'<path d="M{cx} {cy+h} Q{cx+w/2} {cy+h} {cx+w/2} {cy} L{cx+w/4} {cy} Q{cx+w/4} {cy+h*0.8} {cx} {cy+h} Z" fill="{fd}" opacity="0.6"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w*0.1}" fill="#fff" opacity="0.5"/></g>')
def bits(pts): return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><circle cx="{x-r*0.3}" cy="{y-r*0.3}" r="{r*0.35}" fill="#fff" opacity="0.4"/>' for x,y,r,c in pts)
def splat(cx, cy, w, col):
    return (f'<path d="M{cx-w/2} {cy} Q{cx-w*0.45} {cy-26} {cx-w*0.2} {cy-18} Q{cx-w*0.1} {cy-40} {cx+w*0.1} {cy-20} Q{cx+w*0.35} {cy-34} {cx+w/2} {cy} Z" fill="{col}"/>'
            f'<circle cx="{cx-w*0.6}" cy="{cy-10}" r="8" fill="{col}"/><circle cx="{cx+w*0.62}" cy="{cy-16}" r="6" fill="{col}"/>')
def svg(name, vb_h, body):
    open(os.path.join(OUT, f'{name}.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 880 {vb_h}">{body}</svg>')

# HERO: Tunas in the high chair, bowl flying, splat on the floor
b = (floor(330, 420) + shadow(330, 395, 150) + chair(250, 150) + tunas('hore', 150, 175, 250, 10) +
     f'<path d="M420 120 Q560 40 640 250" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 18" stroke-linecap="round"/>' +
     bowl(560, 110, 120, TERRA, TD, rot=140) + bits([(600, 160, 12, SUN), (630, 210, 10, SAGE), (580, 190, 9, SUN), (650, 260, 8, SUN)]) +
     splat(690, 360, 150, SUN) + bits([(660, 345, 9, SAGE), (720, 350, 8, SAGE)]) + text(790, 290, 'plok!', 64, TD, rot=-8) +
     f'<path d="M760 120 l18 -26 M790 140 l28 -12 M770 160 l30 4" stroke="{TERRA}" stroke-width="7" stroke-linecap="round"/>')
svg('hero-lempar', 420, b)

# BIG 1: cause and effect loop: drop -> plok -> again
def loop(cx, cy, r, col):
    return (f'<path d="M{cx+r} {cy} A{r} {r} 0 1 1 {cx} {cy-r}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx-14} {cy-r-18} L{cx+6} {cy-r} L{cx-14} {cy-r+18}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
b = (floor(390, 500) + shadow(230, 455, 140) + chair(170, 210) + tunas('kaget', 130, 150, 170, 80) +
     f'<path d="M350 250 C380 300 360 360 340 400" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>' +
     f'<g transform="rotate(55 360 230)"><rect x="330" y="222" width="90" height="16" rx="8" fill="#c8c2b8"/><ellipse cx="324" cy="230" rx="22" ry="14" fill="#d8d2c8"/></g>' +
     splat(340, 440, 80, SUN) + text(420, 360, 'plok!', 44, TD) +
     loop(660, 250, 110, SD) + text(660, 238, 'lagi!', 52, SD) + text(660, 290, 'lagi!', 40, SAGE))
svg('big-lempar-jatuh', 500, b)

# BIG 2: calm reaction: loud bubble crossed out, calm bubble with Tunas santai picking the bowl up
def bubble(x, y, w, h, f, tail_right=False):
    tx = x + w - 80 if tail_right else x + 40
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{f}"/><path d="M{tx} {y+h-2} L{tx+(30 if tail_right else -10)} {y+h+40} L{tx+50} {y+h-2} Z" fill="{f}"/>'
b = (floor(400, 500) + bubble(40, 40, 360, 130, BLUSH) + text(220, 128, 'JANGAN!!', 64, TD) +
     f'<path d="M80 60 L360 150 M360 60 L80 150" stroke="{TD}" stroke-width="12" stroke-linecap="round" opacity="0.5"/>' +
     bubble(480, 70, 360, 120, '#e3eee6', tail_right=True) + text(660, 145, 'oke, lanjut', 52, SD) +
     shadow(560, 470, 150) + tunas('santai', 170, 195, 480, 250) + bowl(700, 400, 120, TERRA, TD) +
     f'<circle cx="836" cy="58" r="28" fill="{SD}"/><path d="M822 58 L832 68 L850 48" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
svg('big-reaksi-tenang', 500, b)

# BIG 3: finger food cut long on a plate, Tunas holding a stick
def stick(x, y, w, h, rot, f, fd):
    return f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{f}"/><rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" rx="{h*0.22}" fill="{fd}" opacity="0.5"/></g>'
b = (floor(380, 500) + shadow(380, 440, 300) + f'<ellipse cx="380" cy="380" rx="320" ry="80" fill="{CARD}" stroke="{LINE}" stroke-width="8"/>' +
     f'<ellipse cx="380" cy="380" rx="250" ry="56" fill="none" stroke="{LINE}" stroke-width="4"/>' +
     stick(150, 350, 170, 34, -6, TERRA, TD) + stick(170, 392, 160, 34, 5, TERRA, TD) +
     stick(350, 340, 150, 40, 8, '#ecd9a6', SUND) + stick(360, 388, 150, 40, -4, '#ecd9a6', SUND) +
     f'<circle cx="560" cy="360" r="34" fill="{SD}"/><circle cx="590" cy="336" r="30" fill="{SD}"/><circle cx="604" cy="372" r="28" fill="{SAGE}"/><rect x="566" y="370" width="26" height="46" rx="10" fill="{SAGE}"/>' +
     tunas('riset', 170, 195, 660, 120) + stick(790, 260, 110, 30, 70, TERRA, TD) +
     text(130, 120, 'potong', 46, SD, anchor='start') + text(130, 176, 'memanjang', 46, SD, anchor='start') +
     f'<path d="M150 210 L330 210" stroke="{SD}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1 18"/>')
svg('big-jari-latihan', 500, b)

# BIG 4: high chair over a mat, crumbs land on it, Tunas happy
def mat(x, y, w, h):
    stripes = ''.join(f'<rect x="{x+20+i*70}" y="{y}" width="34" height="{h}" fill="#d6e6f4"/>' for i in range(int((w-40)/70)))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{SKY}"/>' + stripes + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="none" stroke="{SKYD}" stroke-width="6"/>'
b = (floor(360, 500) + mat(90, 380, 620, 70) + chair(330, 150) + tunas('hore', 140, 165, 330, 20) +
     bits([(200, 405, 11, SUN), (260, 420, 9, SAGE), (560, 410, 10, SUN), (620, 425, 8, TERRA), (480, 430, 9, SUN)]) +
     f'<rect x="720" y="330" width="120" height="110" rx="14" fill="{CARD}" stroke="{LINE}" stroke-width="5"/><path d="M740 350 L820 350 M740 380 L820 380 M740 410 L800 410" stroke="{LINE}" stroke-width="8" stroke-linecap="round"/>' +
     text(780, 300, 'handuk', 34, MUTED) + text(120, 330, 'alas', 52, SD, anchor='start') +
     f'<circle cx="250" cy="250" r="30" fill="{SD}"/><path d="M236 250 L246 260 L264 240" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
svg('big-alas-kursi', 500, b)

from PIL import Image
for n in ['hero-lempar', 'big-lempar-jatuh', 'big-reaksi-tenang', 'big-jari-latihan', 'big-alas-kursi']:
    f = os.path.join(OUT, n + '.svg'); src = open(f).read()
    im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=src.encode(), output_width=880))).convert('RGBA')
    x0, y0, x1, y1 = im.getbbox()
    pad = 16
    vb = f'{max(0, x0 - pad)} {max(0, y0 - pad)} {min(880, x1 + pad) - max(0, x0 - pad)} {y1 + pad - max(0, y0 - pad)}'
    import re
    open(f, 'w').write(re.sub(r'viewBox="[^"]+"', f'viewBox="{vb}"', src, count=1))
print('ok')
