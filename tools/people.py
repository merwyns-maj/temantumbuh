"""Flat illustrated family for story posts: Mama (hijab), Ayah, Adek (about 2 years).
No real faces, not photoreal (CLAUDE.md rule 6). Same palette as artkit.
person(kind, cx, cy, s, expr, arms) draws a bust (head + torso); cy is the head centre, s the scale (1 = adult head r 62).
expr: senang, lembut, sedih, nangis, capek, kaget, ngomel. arms: none, pegang, peluk, tangan-dada.
"""
from artkit import *

SKIN = '#f3cba5'; SKIND = '#e2ad83'; HAIR = '#3b2f2a'; CHEEK = '#f2a38c'
OUTFIT = {'mama': (SAGE, SD), 'ayah': (SKY, SKYD), 'adek': (SUN, SUND)}
HIJAB = ('#d98b72', '#c4735b')

def _brows(cx, ey, r, dx, w, kind):
    out = ''
    for k in (-1, 1):
        ox, ix = cx + k * (dx + r * 0.16), cx + k * (dx - r * 0.12)
        if kind == 'sad': oy, iy = ey - r * 0.2, ey - r * 0.33
        else: oy, iy = ey - r * 0.32, ey - r * 0.2   # cross
        out += f'<path d="M{ox} {oy} L{ix} {iy}" stroke="{INK}" stroke-width="{w*0.85}" stroke-linecap="round"/>'
    return out

def _eyes(cx, cy, r, expr):
    dx, ey = r * 0.36, cy - r * 0.02
    w = max(3, r * 0.07)
    if expr in ('senang',):
        return ''.join(f'<path d="M{cx+k*dx-r*0.13} {ey+r*0.04} Q{cx+k*dx} {ey-r*0.14} {cx+k*dx+r*0.13} {ey+r*0.04}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
    if expr in ('lembut', 'capek'):
        if expr == 'capek':
            return _brows(cx, ey, r, dx, w, 'sad') + ''.join(f'<path d="M{cx+k*dx-r*0.14} {ey} L{cx+k*dx+r*0.14} {ey}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/><path d="M{cx+k*dx-r*0.11} {ey} Q{cx+k*dx} {ey+r*0.09} {cx+k*dx+r*0.11} {ey}" fill="{INK}"/>' for k in (-1, 1))
        lid = ''
        return lid + ''.join(f'<path d="M{cx+k*dx-r*0.13} {ey} Q{cx+k*dx} {ey+r*0.1} {cx+k*dx+r*0.13} {ey}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
    if expr == 'nangis':
        e = ''.join(f'<path d="M{cx+k*dx-r*0.15} {ey-r*0.02} Q{cx+k*dx} {ey+r*0.1} {cx+k*dx+r*0.15} {ey-r*0.02}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>' for k in (-1, 1))
        e += ''.join(f'<path d="M{cx+k*dx} {ey+r*0.1} Q{cx+k*(dx+r*0.08)} {ey+r*0.4} {cx+k*dx} {ey+r*0.55} Q{cx+k*(dx-r*0.08)} {ey+r*0.4} {cx+k*dx} {ey+r*0.1} Z" fill="{SKY}"/>' for k in (-1, 1))
        e += _brows(cx, ey, r, dx, w, 'sad')
        return e
    e = ''.join(f'<circle cx="{cx+k*dx}" cy="{ey}" r="{r*0.075 if expr!="kaget" else r*0.09}" fill="{INK}"/><circle cx="{cx+k*dx+r*0.025}" cy="{ey-r*0.03}" r="{r*0.025}" fill="#fff"/>' for k in (-1, 1))
    if expr == 'sedih':
        e += _brows(cx, ey, r, dx, w, 'sad')
    if expr == 'ngomel':
        e += _brows(cx, ey, r, dx, w, 'cross')
    return e

def _mouth(cx, cy, r, expr):
    my = cy + r * 0.38; w = max(3, r * 0.07)
    if expr in ('senang',):
        return f'<path d="M{cx-r*0.24} {my-r*0.05} Q{cx} {my+r*0.3} {cx+r*0.24} {my-r*0.05} Z" fill="{TD}"/><path d="M{cx-r*0.12} {my+r*0.12} Q{cx} {my+r*0.2} {cx+r*0.12} {my+r*0.12}" stroke="#f6a08a" stroke-width="{w}" fill="none"/>'
    if expr == 'lembut':
        return f'<path d="M{cx-r*0.17} {my} Q{cx} {my+r*0.16} {cx+r*0.17} {my}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    if expr in ('sedih', 'capek'):
        return f'<path d="M{cx-r*0.15} {my+r*0.08} Q{cx} {my-r*0.04} {cx+r*0.15} {my+r*0.08}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    if expr == 'nangis':
        return f'<ellipse cx="{cx}" cy="{my+r*0.06}" rx="{r*0.2}" ry="{r*0.17}" fill="{TD}"/><ellipse cx="{cx}" cy="{my+r*0.15}" rx="{r*0.11}" ry="{r*0.06}" fill="#f6a08a"/>'
    if expr == 'kaget':
        return f'<ellipse cx="{cx}" cy="{my+r*0.04}" rx="{r*0.09}" ry="{r*0.12}" fill="{TD}"/>'
    if expr == 'ngomel':
        return f'<path d="M{cx-r*0.2} {my+r*0.04} L{cx+r*0.2} {my-r*0.02}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
    return ''

def _arms(kind, cx, ty, r, arms, col, cold):
    w = r * 0.42
    if arms == 'pegang':   # both forearms forward, hands together in front of chest
        return (f'<path d="M{cx-r*1.15} {ty+r*0.5} Q{cx-r*0.9} {ty+r*1.35} {cx-r*0.2} {ty+r*1.15}" stroke="{cold}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+r*1.15} {ty+r*0.5} Q{cx+r*0.9} {ty+r*1.35} {cx+r*0.2} {ty+r*1.15}" stroke="{cold}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                f'<circle cx="{cx-r*0.18}" cy="{ty+r*1.13}" r="{w*0.55}" fill="{SKIN}"/><circle cx="{cx+r*0.18}" cy="{ty+r*1.13}" r="{w*0.55}" fill="{SKIN}"/>')
    if arms == 'peluk':    # arms reaching to one side (hug the child on the viewer's right)
        return (f'<path d="M{cx+r*1.1} {ty+r*0.45} Q{cx+r*1.9} {ty+r*0.7} {cx+r*2.5} {ty+r*0.55}" stroke="{cold}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                f'<circle cx="{cx+r*2.55}" cy="{ty+r*0.55}" r="{w*0.55}" fill="{SKIN}"/>')
    if arms == 'tangan-dada':
        return (f'<path d="M{cx+r*1.1} {ty+r*0.5} Q{cx+r*0.9} {ty+r*1.2} {cx+r*0.2} {ty+r*0.75}" stroke="{cold}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
                f'<circle cx="{cx+r*0.15}" cy="{ty+r*0.72}" r="{w*0.55}" fill="{SKIN}"/>')
    return ''

def person(kind, cx, cy, s=1.0, expr='senang', arms='none', flip=False):
    r = 62 * s if kind != 'adek' else 54 * s
    col, cold = OUTFIT[kind]
    ty = cy + r * 0.95          # top of torso
    tw = r * (1.35 if kind != 'adek' else 1.15)
    th = r * 2.6  # long torso: a table drawn in front cuts it off
    g = []
    # torso
    g.append(f'<path d="M{cx-tw} {ty+th} Q{cx-tw} {ty} {cx} {ty} Q{cx+tw} {ty} {cx+tw} {ty+th} Z" fill="{col}"/>')
    g.append(f'<path d="M{cx+tw*0.25} {ty+r*0.05} Q{cx+tw} {ty+r*0.1} {cx+tw} {ty+th} L{cx+tw*0.45} {ty+th} Z" fill="{cold}" opacity="0.35"/>')
    if kind == 'mama':  # hijab drapes over the shoulders
        hc, hd = HIJAB
        g.append(f'<path d="M{cx-r*1.08} {cy-r*0.1} Q{cx-r*1.15} {cy+r*1.25} {cx-r*0.2} {ty+r*0.75} L{cx+r*0.2} {ty+r*0.75} Q{cx+r*1.15} {cy+r*1.25} {cx+r*1.08} {cy-r*0.1} Z" fill="{hc}"/>')
        g.append(f'<circle cx="{cx}" cy="{cy-r*0.05}" r="{r*1.1}" fill="{hc}"/>')
        g.append(f'<path d="M{cx+r*0.35} {cy-r*1.0} Q{cx+r*1.2} {cy-r*0.6} {cx+r*1.05} {cy+r*0.6}" stroke="{hd}" stroke-width="{r*0.12}" fill="none" opacity="0.5"/>')
    else:
        g.append(f'<rect x="{cx-r*0.22}" y="{cy+r*0.7}" width="{r*0.44}" height="{r*0.4}" fill="{SKIND}"/>')
    # face
    g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.86 if kind=="mama" else r}" ry="{r*0.92 if kind=="mama" else r}" fill="{SKIN}"/>')
    if kind == 'ayah':
        g.append(f'<path d="M{cx-r*1.02} {cy-r*0.05} Q{cx-r*1.05} {cy-r*1.15} {cx} {cy-r*1.08} Q{cx+r*1.05} {cy-r*1.15} {cx+r*1.02} {cy-r*0.05} Q{cx+r*0.85} {cy-r*0.6} {cx+r*0.3} {cy-r*0.62} Q{cx-r*0.3} {cy-r*0.45} {cx-r*0.85} {cy-r*0.55} Z" fill="{HAIR}"/>')
        g.append(f'<ellipse cx="{cx-r*1.0}" cy="{cy+r*0.05}" rx="{r*0.14}" ry="{r*0.2}" fill="{SKIN}"/><ellipse cx="{cx+r*1.0}" cy="{cy+r*0.05}" rx="{r*0.14}" ry="{r*0.2}" fill="{SKIN}"/>')
    if kind == 'adek':
        g.append(f'<path d="M{cx-r*0.95} {cy-r*0.25} Q{cx-r*0.9} {cy-r*1.05} {cx} {cy-r*1.02} Q{cx+r*0.9} {cy-r*1.05} {cx+r*0.95} {cy-r*0.25} Q{cx+r*0.5} {cy-r*0.6} {cx} {cy-r*0.55} Q{cx-r*0.5} {cy-r*0.65} {cx-r*0.95} {cy-r*0.25} Z" fill="{HAIR}"/>')
        g.append(f'<path d="M{cx-r*0.05} {cy-r*1.0} Q{cx+r*0.2} {cy-r*1.35} {cx+r*0.35} {cy-r*1.15}" stroke="{HAIR}" stroke-width="{r*0.12}" fill="none" stroke-linecap="round"/>')
    if kind == 'mama':
        g.append(f'<path d="M{cx-r*0.88} {cy-r*0.2} Q{cx-r*0.8} {cy-r*0.95} {cx} {cy-r*0.92} Q{cx+r*0.8} {cy-r*0.95} {cx+r*0.88} {cy-r*0.2} Q{cx+r*0.6} {cy-r*0.7} {cx} {cy-r*0.72} Q{cx-r*0.6} {cy-r*0.7} {cx-r*0.88} {cy-r*0.2} Z" fill="{HIJAB[1]}"/>')
    # cheeks, eyes, mouth
    if expr not in ('capek',):
        g.append(''.join(f'<ellipse cx="{cx+k*r*0.55}" cy="{cy+r*0.28}" rx="{r*0.16}" ry="{r*0.1}" fill="{CHEEK}" opacity="0.55"/>' for k in (-1, 1)))
    g.append(_eyes(cx, cy, r, expr)); g.append(_mouth(cx, cy, r, expr))
    if expr == 'capek':
        g.append(f'<path d="M{cx+r*1.05} {cy-r*0.9} q{r*0.12} {r*0.25} 0 {r*0.35} q-{r*0.12} -{r*0.1} 0 -{r*0.35}" fill="{SKY}"/>')
    g.append(_arms(kind, cx, ty, r, arms, col, cold))
    body = ''.join(g)
    if flip: body = f'<g transform="translate({2*cx} 0) scale(-1 1)">{body}</g>'
    return body

def bubble(x, y, w, lines, tail='bl', size=30, col=CARD, ink=INK, think=False):
    """Speech (or thought) bubble with its top-left at x, y. tail: bl, br (bottom-left/right) or none."""
    h = 28 + len(lines) * size * 1.25
    out = [f'<rect x="{x+4}" y="{y+6}" width="{w}" height="{h}" rx="22" fill="#000" opacity="0.08"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{col}" stroke="{LINE}" stroke-width="3"/>']
    if think:
        tx = x + (w * 0.25 if tail == 'bl' else w * 0.75)
        out += [f'<circle cx="{tx}" cy="{y+h+18}" r="12" fill="{col}" stroke="{LINE}" stroke-width="3"/>',
                f'<circle cx="{tx-14 if tail=="bl" else tx+14}" cy="{y+h+42}" r="7" fill="{col}" stroke="{LINE}" stroke-width="3"/>']
    elif tail in ('bl', 'br'):
        tx = x + (40 if tail == 'bl' else w - 40)
        d = -1 if tail == 'bl' else 1
        out.append(f'<path d="M{tx-18} {y+h-2} L{tx+d*-6} {y+h+30} L{tx+18} {y+h-2} Z" fill="{col}" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>')
        out.append(f'<rect x="{tx-20}" y="{y+h-6}" width="40" height="6" fill="{col}"/>')
    for i, t in enumerate(lines):
        out.append(f'<text x="{x+w/2}" y="{y+18+size*1.05+i*size*1.25}" font-family="sans-serif" font-weight="800" font-size="{size}" text-anchor="middle" fill="{ink}">{t}</text>')
    return ''.join(out)

def biscuit(cx, cy, s=1.0, rot=0, half=None):
    """Round biscuit; half='l' or 'r' draws one broken half."""
    r = 34 * s
    clip = ''
    if half == 'l': d = f'M{cx} {cy-r} L{cx-6*s} {cy-r*0.3} L{cx+4*s} {cy+r*0.1} L{cx-5*s} {cy+r*0.6} L{cx} {cy+r} A{r} {r} 0 0 1 {cx} {cy-r} Z'
    elif half == 'r': d = f'M{cx} {cy-r} L{cx-6*s} {cy-r*0.3} L{cx+4*s} {cy+r*0.1} L{cx-5*s} {cy+r*0.6} L{cx} {cy+r} A{r} {r} 0 0 0 {cx} {cy-r} Z'
    else: d = None
    shape = f'<path d="{d}" fill="{BOX}"/>' if d else f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BOX}"/>'
    dots = ''.join(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{3.5*s}" fill="{BOXD}"/>' for dx, dy in ((-14, -10), (12, -14), (-8, 12), (14, 10), (0, -2))
                   if not half or (half == 'l' and dx <= 0) or (half == 'r' and dx > 0))
    return f'<g transform="rotate({rot} {cx} {cy})">{shape}{dots}</g>'

def table(y, H, col=FLOOR, edge=BOX):
    """A table or floor edge drawn IN FRONT of the busts, so they sit behind it."""
    return f'<rect x="0" y="{y}" width="880" height="{H-y}" rx="18" fill="{col}"/><rect x="0" y="{y}" width="880" height="12" rx="6" fill="{edge}" opacity="0.35"/>'

def head_r(kind, s): return (62 if kind != 'adek' else 54) * s
def seat(kind, s, top, holding=False):
    """Head-centre y so the hands (holding) or the chest sit just above a table top."""
    r = head_r(kind, s)
    return top - (2.5 * r if holding else 2.1 * r)
