"""Shared drawing kit for design v2 scenes (flat token palette, floor, soft shadows, Tunas inside the scene).
Import it: `from artkit import *`, draw with the helpers, write with svg(name, height, body), then autocrop([names]).
hero-<name>.svg: 880 x ~420, the hook slide. big-<name>.svg: 880 x ~500, a point slide (also used small in cheat sheets).
"""
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


def autocrop(names, pad=16):
    """Shrink each SVG's viewBox to its drawn content so render.py can size it from the real aspect ratio."""
    import re
    from PIL import Image
    for n in names:
        f = os.path.join(OUT, n + '.svg'); src = open(f).read()
        im = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=src.encode(), output_width=880))).convert('RGBA')
        vb0 = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
        scale = vb0[2] / 880
        x0, y0, x1, y1 = im.getbbox()
        x0, y0, x1, y1 = (vb0[0] + x0 * scale, vb0[1] + y0 * scale, vb0[0] + x1 * scale, vb0[1] + y1 * scale)
        vb = f'{max(vb0[0], x0 - pad):.0f} {max(vb0[1], y0 - pad):.0f} {min(vb0[0] + vb0[2], x1 + pad) - max(vb0[0], x0 - pad):.0f} {min(vb0[1] + vb0[3], y1 + pad) - max(vb0[1], y0 - pad):.0f}'
        open(f, 'w').write(re.sub(r'viewBox="[^"]+"', f'viewBox="{vb}"', src, count=1))
