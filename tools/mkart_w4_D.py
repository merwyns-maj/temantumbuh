# Scenes for week 4, group D:
#   w4l-overstimulasi (tanda bayi kebanyakan stimulasi, cara kasih jeda)
#   w4l-finger-food   (finger food pertama, gagging vs tersedak)
# Tunas stands in for the baby. No bottles, teats or pacifiers (PP 28/2024). Short labels only.
# Run: python tools/mkart_w4_D.py [contact-sheet.png]
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *  # artkit palette + person()

NAMES = []
TSKIN = '#eab5a1'   # Tunas arm shade
DIM = '#3d4466'     # dimmed room
EGG = '#f6d877'; EGGD = '#e3b94a'; AVO = '#b9d58a'; AVOD = '#7fa98f'; NUT = '#c9955c'; NUTD = '#a8743f'; GRAPE = '#9a7fc0'; GRAPED = '#7d62a6'


def out(name, h, body):
    svg(name, h, body)
    NAMES.append(name)


# ---------------------------------------------------------------- helpers
def rect(x, y, w, h, f, rx=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'


def check(cx, cy, r=30):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SD}"/>'
            f'<path d="M{cx-r*0.47} {cy} L{cx-r*0.13} {cy+r*0.33} L{cx+r*0.47} {cy-r*0.33}" stroke="#fff" stroke-width="{r*0.28:.0f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=30):
    k = r * 0.38
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TERRA}"/>'
            f'<path d="M{cx-k} {cy-k} L{cx+k} {cy+k} M{cx+k} {cy-k} L{cx-k} {cy+k}" stroke="#fff" stroke-width="{r*0.28:.0f}" stroke-linecap="round"/>')


def pill(cx, cy, label, col=BLUSH, ink=TD, size=40, w=None):
    w = w or len(label) * size * 0.62 + 50
    return f'<rect x="{cx-w/2}" y="{cy-size*0.85}" width="{w}" height="{size*1.7}" rx="{size*0.85}" fill="{col}"/>' + text(cx, cy + size * 0.36, label, size, ink)


def say(x, y, w, h, label, size=44, col=BLUSH, ink=TD, tail='left'):
    tx = x + w - 70 if tail == 'right' else x + 40
    d = 30 if tail == 'right' else -10
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(34, h/2)}" fill="{col}"/><path d="M{tx} {y+h-2} L{tx+d} {y+h+34} L{tx+46} {y+h-2} Z" fill="{col}"/>'
            + text(x + w / 2, y + h / 2 + size * 0.36, label, size, ink))


def arcs(cx, cy, r, col=TERRA, side='both', n=2):
    s = ''
    for k in ((-1, 1) if side == 'both' else ((-1,) if side == 'l' else (1,))):
        for i in range(n):
            rr = r + i * 30
            s += (f'<path d="M{cx+k*rr} {cy-30-i*16} Q{cx+k*(rr+26)} {cy} {cx+k*rr} {cy+30+i*16}" stroke="{col}" stroke-width="{9-i}" fill="none" '
                  f'stroke-linecap="round" opacity="{1-i*0.4}"/>')
    return s


def turn_arrow(x, y, s=1, col=MUTED, flip=False):
    k = -1 if flip else 1
    return (f'<g transform="translate({x} {y}) scale({k*s} {s})"><path d="M0 0 Q-30 -60 -80 -45" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            f'<path d="M-70 -72 L-84 -44 L-56 -30" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')


def note(x, y, s, col):
    return (f'<g transform="translate({x} {y}) scale({s/30})"><ellipse cx="0" cy="0" rx="13" ry="10" fill="{col}" transform="rotate(-20)"/>'
            f'<path d="M11 -4 L11 -46 Q24 -40 30 -28" stroke="{col}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')


def rattle(cx, cy, s=1, rot=-20):
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})"><rect x="-9" y="10" width="18" height="90" rx="9" fill="{SKYD}"/>'
            f'<circle cx="0" cy="-20" r="40" fill="{SUN}"/><circle cx="0" cy="-20" r="40" fill="none" stroke="{SUND}" stroke-width="6"/>'
            f'<circle cx="-12" cy="-32" r="10" fill="#fff" opacity="0.45"/><circle cx="0" cy="108" r="14" fill="{SKYD}"/></g>')


def ball(cx, cy, r=40):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TERRA}"/><path d="M{cx-r} {cy} Q{cx} {cy-r*0.6} {cx+r} {cy}" stroke="{CARD}" stroke-width="{r*0.22}" fill="none"/>'
            f'<path d="M{cx} {cy-r} Q{cx+r*0.5} {cy} {cx} {cy+r}" stroke="{SUN}" stroke-width="{r*0.22}" fill="none"/>')


def block(x, y, s, col, cold, letter=''):
    return (rect(x, y, s, s, col, s * 0.16) + rect(x, y + s * 0.72, s, s * 0.28, cold, s * 0.12) +
            (text(x + s / 2, y + s * 0.62, letter, s * 0.5, CARD) if letter else ''))


def tv(x, y, w=230, h=160, on=True):
    scr = SKY if on else '#5b6378'
    s = (rect(x, y, w, h, INK, 18) + rect(x + 14, y + 14, w - 28, h - 28, scr, 10) +
         f'<path d="M{x+w*0.35} {y+h} L{x+w*0.28} {y+h+40} M{x+w*0.65} {y+h} L{x+w*0.72} {y+h+40}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    if on:
        s += f'<circle cx="{x+w*0.38}" cy="{y+h*0.5}" r="{h*0.18}" fill="{SUN}"/><path d="M{x+w*0.52} {y+h*0.72} l{w*0.12} -{h*0.3} l{w*0.12} {h*0.3} Z" fill="{SAGE}"/>'
    return s


def lamp(cx, top, on=True, dim=False):
    shade = SUN if on and not dim else ('#c9b27a' if dim else LINE)
    s = (f'<path d="M{cx} {top} L{cx} {top+60}" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M{cx-70} {top+130} L{cx-36} {top+60} L{cx+36} {top+60} L{cx+70} {top+130} Z" fill="{shade}"/>'
         f'<rect x="{cx-70}" y="{top+122}" width="140" height="14" rx="7" fill="{SUND if not dim else "#a8915a"}"/>')
    if on and not dim:
        for a in (-50, -25, 0, 25, 50):
            r = math.radians(a + 90)
            s += f'<path d="M{cx+math.cos(r)*90:.0f} {top+140+math.sin(r)*30:.0f} L{cx+math.cos(r)*150:.0f} {top+150+math.sin(r)*80:.0f}" stroke="{SUN}" stroke-width="9" stroke-linecap="round"/>'
    if dim:
        s += f'<circle cx="{cx}" cy="{top+140}" r="34" fill="{SUN}" opacity="0.25"/><circle cx="{cx}" cy="{top+138}" r="16" fill="{SUN}"/>'
    return s


def moon(cx, cy, r, bg):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/><circle cx="{cx+r*0.45}" cy="{cy-r*0.3}" r="{r*0.85}" fill="{bg}"/>'


def mat(cx, cy, w):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w*0.1}" fill="{SAGE}" opacity="0.55"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2-24}" ry="{w*0.1-10}" fill="none" stroke="{CARD}" stroke-width="5" stroke-dasharray="10 12" opacity="0.8"/>')


def fist(cx, cy, s=1):
    return (f'<g transform="translate({cx} {cy}) scale({s})"><circle cx="0" cy="0" r="22" fill="{TSKIN}"/>'
            f'<path d="M-12 -8 Q-6 -16 0 -8 Q6 -16 12 -8" stroke="#c98f7a" stroke-width="4" fill="none" stroke-linecap="round"/></g>')


def grp(body, s, ox=0, oy=0):
    return f'<g transform="translate({ox} {oy}) scale({s})">{body}</g>'


def carrot_stick(cx, cy, L=150, rot=0, w=26, cooked=True):
    col = '#ef9a6b' if cooked else TERRA
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-L/2}" y="{cy-w/2}" width="{L}" height="{w}" rx="{w/2}" fill="{col}"/>'
            f'<rect x="{cx-L/2+8}" y="{cy-w/2+4}" width="{L-30}" height="{w*0.25}" rx="{w*0.12}" fill="#fff" opacity="0.3"/></g>')


def steam(x, y, s=1):
    return ''.join(f'<path d="M{x+i*28*s} {y} q-12 -16 0 -32 q12 -16 0 -32" stroke="{MUTED}" stroke-width="{6*s}" fill="none" stroke-linecap="round" opacity="0.45"/>' for i in range(3))


def omelette(cx, cy, L=160, rot=0, w=34):
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-L/2}" y="{cy-w/2}" width="{L}" height="{w}" rx="10" fill="{EGG}"/>'
            f'<circle cx="{cx-L*0.25}" cy="{cy-4}" r="5" fill="{EGGD}"/><circle cx="{cx+L*0.1}" cy="{cy+6}" r="4" fill="{EGGD}"/><circle cx="{cx+L*0.3}" cy="{cy-6}" r="4" fill="{SAGE}"/></g>')


def avocado(cx, cy, L=150, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><path d="M{cx-L/2} {cy+12} Q{cx-L/2} {cy-26} {cx} {cy-24} Q{cx+L/2} {cy-22} {cx+L/2} {cy+8} Q{cx} {cy+24} {cx-L/2} {cy+12} Z" fill="{AVO}"/>'
            f'<path d="M{cx-L/2+6} {cy+14} Q{cx} {cy+26} {cx+L/2-4} {cy+10}" stroke="{AVOD}" stroke-width="8" fill="none" stroke-linecap="round"/></g>')


def banana_stick(cx, cy, L=140, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx-L/2}" y="{cy-18}" width="{L}" height="36" rx="18" fill="#fbeab0"/>'
            f'<circle cx="{cx-L/2+18}" cy="{cy}" r="10" fill="#f1d98a"/></g>')


def plate(cx, cy, w):
    return (shadow(cx, cy + w * 0.12, w * 0.55) + f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{w*0.17}" fill="{CARD}" stroke="{LINE}" stroke-width="6"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2-40}" ry="{w*0.17-16}" fill="none" stroke="{LINE}" stroke-width="4"/>')


def finger(x, y, L=170, w=44, rot=0):
    """Adult index finger, horizontal, nail at the right end."""
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x}" y="{y-w/2}" width="{L}" height="{w}" rx="{w/2}" fill="{SKIN}"/>'
            f'<rect x="{x}" y="{y-w/2}" width="40" height="{w}" fill="{SKIN}"/>'
            f'<rect x="{x+L-48}" y="{y-w/2+8}" width="38" height="{w-16}" rx="10" fill="#f7e0cb"/>'
            f'<path d="M{x+L*0.42} {y-w/2+6} q6 {w/2-6} 0 {w-12} M{x+L*0.62} {y-w/2+6} q6 {w/2-6} 0 {w-12}" stroke="{SKIND}" stroke-width="4" fill="none" stroke-linecap="round"/></g>')


def thumb_press(cx, cy):
    """Thumb from above pressing a soft piece flat."""
    return (f'<path d="M{cx-80} {cy+36} Q{cx-78} {cy+4} {cx-34} {cy+6} Q{cx} {cy+22} {cx+34} {cy+6} Q{cx+78} {cy+4} {cx+80} {cy+36} Q{cx} {cy+52} {cx-80} {cy+36} Z" fill="{AVO}"/>'
            f'<path d="M{cx-74} {cy+38} Q{cx} {cy+52} {cx+74} {cy+38}" stroke="{AVOD}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<rect x="{cx-30}" y="{cy-130}" width="60" height="130" rx="30" fill="{SKIN}"/><rect x="{cx-20}" y="{cy-40}" width="40" height="30" rx="10" fill="#f7e0cb"/>'
            f'<path d="M{cx-86} {cy+10} l-20 -8 M{cx+86} {cy+10} l20 -8 M{cx-84} {cy+28} l-22 6 M{cx+84} {cy+28} l22 6" stroke="{MUTED}" stroke-width="6" stroke-linecap="round"/>')


def nut(cx, cy, s=1, rot=0):
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})"><path d="M-30 -14 Q-34 -32 -14 -30 Q0 -22 14 -30 Q34 -32 30 -14 Q26 0 30 14 Q34 32 14 30 Q0 22 -14 30 Q-34 32 -30 14 Q-26 0 -30 -14 Z" fill="{NUT}"/>'
            f'<path d="M-18 -10 l8 4 M6 -14 l8 4 M-10 10 l8 4 M10 8 l8 4" stroke="{NUTD}" stroke-width="4" stroke-linecap="round"/></g>')


def grapes(cx, cy, r=20):
    pts = [(0, 0), (-r * 1.8, -r * 0.2), (r * 1.8, -r * 0.2), (-r * 0.9, r * 1.5), (r * 0.9, r * 1.5), (0, r * 3)]
    s = f'<path d="M{cx} {cy-r} Q{cx+6} {cy-r*2.2} {cx+r} {cy-r*2.6}" stroke="{BOXD}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    for dx, dy in pts:
        s += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{GRAPE}"/><circle cx="{cx+dx-r*0.35}" cy="{cy+dy-r*0.35}" r="{r*0.3}" fill="#fff" opacity="0.45"/>'
    return s


def popcorn(cx, cy, s=1):
    return (f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-40 0 L40 0 L30 80 L-30 80 Z" fill="{CARD}" stroke="{TERRA}" stroke-width="5"/>'
            f'<path d="M-20 4 L-16 78 M0 4 L0 78 M20 4 L16 78" stroke="{TERRA}" stroke-width="8"/>'
            + ''.join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="#fff6dc" stroke="{SUND}" stroke-width="3"/>' for dx, dy, r in ((-26, -10, 16), (-4, -20, 18), (20, -12, 16), (8, -36, 14), (-16, -34, 13)))
            + '</g>')


def apple_chunk(cx, cy, s=1):
    return (f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-30 -20 L30 -26 L34 24 L-28 28 Z" fill="#fbf1d4"/>'
            f'<path d="M-30 -20 L30 -26 L28 -34 L-32 -28 Z" fill="#d9604a"/></g>')


def calendar(x, y, w, big, small=None):
    s = (rect(x, y, w, w * 0.92, CARD, 22, f'stroke="{LINE}" stroke-width="6"') + rect(x, y, w, w * 0.26, TERRA, 22) + rect(x, y + w * 0.14, w, w * 0.12, TERRA) +
         f'<circle cx="{x+w*0.28}" cy="{y}" r="9" fill="{INK}"/><circle cx="{x+w*0.72}" cy="{y}" r="9" fill="{INK}"/>' + text(x + w / 2, y + w * 0.66, big, w * 0.3, INK))
    if small:
        s += text(x + w / 2, y + w * 0.84, small, w * 0.13, MUTED)
    return s


def tears(cx, cy, s=1):
    return ''.join(f'<path d="M{cx+k*30*s} {cy} q{k*6*s} {14*s} 0 {22*s} q-{k*6*s} -{8*s} 0 -{22*s}" fill="{SKY}"/>' for k in (-1, 1))


# ================================================================= w4l-overstimulasi
# HERO: lots going on (TV, lamp, toys, music); Tunas turns away and asks for a pause
H = 440
b = (floor(340, H) + tv(30, 40, 220, 150) + arcs(140, 115, 130, SKYD, 'r', 2) +
     note(300, 70, 30, SUND) + note(345, 120, 24, SAGE) + ball(300, 300, 44) + block(370, 262, 72, SKY, SKYD, 'A') + rattle(470, 250, 0.8, 25) +
     shadow(660, 420, 160) + tunas('mikir', 250, 292, 535, 120, flip=True) + turn_arrow(790, 200, 1.0, flip=True) +
     say(600, 0, 250, 96, 'jeda dulu', 44))
out('hero-w4d-buang-muka', H, b)

# 1 buang muka: toy offered, baby turns away
H = 460
b = (floor(360, H) + mat(430, 400, 620) + rattle(190, 200, 1.1, -30) +
     shadow(520, 420, 140) + tunas('mikir', 260, 303, 390, 110, flip=True) + turn_arrow(660, 170, 1.15, flip=True) +
     say(640, 0, 210, 90, 'jeda', 46))
out('big-w4d-noleh', H, b)

# 2 badan melengkung, tangan ngepal, kaki nendang
H = 600
b = '<g transform="translate(0 130)">' + (floor(360, H) + mat(440, 405, 640) + shadow(440, 420, 150) +
     f'<g transform="rotate(-22 440 330)">' + tunas('kaget', 240, 280, 320, 110) + '</g>' +
     f'<path d="M300 230 Q240 300 300 380" stroke="{TERRA}" stroke-width="10" fill="none" stroke-linecap="round"/>' +
     f'<path d="M262 210 Q190 300 262 400" stroke="{TERRA}" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.55"/>' +
     arcs(470, 210, 150, TERRA, 'r', 2) +
     say(660, 260, 200, 86, 'ugh', 44)) + '</g>'
out('big-w4d-melengkung', H, b)

# 3 nguap dan cegukan
H = 460
b = (floor(360, H) + mat(400, 405, 600) + shadow(330, 420, 140) + tunas('ngantuk', 240, 280, 210, 130) +
     say(450, 30, 260, 92, 'hoaam', 46, SKY, '#2f5677') + text(560, 230, 'hik!', 56, TD, rot=-10) + text(650, 300, 'hik!', 40, TD, rot=8) +
     ball(110, 360, 34) + block(560, 330, 60, SUN, SUND))
out('big-w4d-nguap', H, b)

# 4 rewel pas rumah rame: TV, tamu, lampu terang
H = 470
b = (floor(370, H) + lamp(440, 0, on=True) + tv(20, 150, 200, 140) + arcs(120, 220, 115, SKYD, 'r', 1) +
     say(640, 40, 220, 84, 'gemes!', 40) + say(620, 170, 240, 84, 'ciluk ba', 38, SKY, '#2f5677', 'right') +
     shadow(440, 440, 130) + tunas('kaget', 200, 233, 340, 200) + tears(440, 330, 1.2) + arcs(440, 300, 120, TERRA, 'both', 1))
out('big-w4d-rame', H, b)

# 5 kasih jeda: kamar redup, TV mati, didekap
H = 480
b = (rect(0, 0, 880, H, DIM, 24) + rect(0, 380, 880, 100, '#343a58', 24) + moon(120, 90, 46, DIM) +
     ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" opacity="0.6"/>' for x, y in ((220, 60), (60, 190), (250, 170), (780, 230))) +
     lamp(760, 0, on=True, dim=True) + tv(30, 240, 170, 120, on=False) +
     person('mama', 430, 190, 1.3, 'lembut', 'none') +
     tunas('ngantuk', 200, 233, 330, 190) +
     f'<path d="M{430-62*1.3*1.25} 370 Q430 480 {430+62*1.3*1.25} 370" stroke="{SD}" stroke-width="{62*1.3*0.42}" fill="none" stroke-linecap="round"/>' +
     text(600, 110, 'sst', 46, SUN))
out('big-w4d-jeda', H, b)

# cheat icons (how to pause): stop main, lampu redup, suara kecil, dekap
S = 320
out('big-w4d-c-stop', S, rect(70, 200, 180, 110, BOX, 18) + rect(70, 200, 180, 30, BOXD, 14) + block(40, 90, 70, SKY, SKYD) + ball(250, 120, 40) +
    f'<path d="M160 90 L160 170" stroke="{SD}" stroke-width="10" stroke-linecap="round"/><path d="M140 150 L160 172 L180 150" stroke="{SD}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
out('big-w4d-c-lampu', S, rect(0, 0, 320, 320, DIM, 30) + moon(240, 70, 34, DIM) + lamp(140, 50, on=True, dim=True))
out('big-w4d-c-suara', S, tv(10, 40, 200, 140, on=False) +
    f'<path d="M210 230 L240 230 L280 200 L280 300 L240 270 L210 270 Z" fill="{MUTED}"/>' +
    f'<path d="M296 230 l26 26 M322 230 l-26 26" stroke="{TERRA}" stroke-width="10" stroke-linecap="round"/>')
out('big-w4d-c-dekap', S, f'<circle cx="160" cy="170" r="140" fill="{BLUSH}"/>' + tunas('sayang', 200, 233, 60, 50))

# ================================================================= w4l-finger-food
# HERO: Tunas in high chair with a carrot stick, gagging loudly (normal)
H = 440
b = (floor(380, H+60) + shadow(330, 460, 190) + grp(chair(250, 190) + tunas('kaget', 160, 187, 250, 30) + tears(330, 125, 1) +
     carrot_stick(400, 175, 110, -40, 24) + arcs(330, 110, 110, TERRA, 'both', 2), 1.45, -160, -10) +
     say(560, 0, 250, 96, 'uhuk!', 52) + check(700, 230, 46) + text(700, 335, 'normal', 50, SD))
out('hero-w4d-gagging', H + 60, b)

# 1 mulai sekitar 8-9 bulan, udah duduk tegak
H = 600
b = (floor(500, H) + calendar(40, 170, 260, '8-9', 'bulan') +
     shadow(570, 580, 170) + grp(chair(480, 210) + tunas('halo', 160, 187, 480, 48) + carrot_stick(625, 140, 100, -70, 22), 1.3, -150, -20) +
     check(800, 150, 40))
out('big-w4d-ff-mulai', H, b)

# 2 ukuran: sepanjang jari orang dewasa, bisa dipenyet
H = 470
b = (floor(380, H) + rect(30, 60, 470, 300, CARD, 30, f'stroke="{LINE}" stroke-width="6"') +
     finger(80, 140, 190, 50) + carrot_stick(175, 230, 190, 0, 34) + omelette(175, 300, 190, 0, 36) +
     f'<path d="M80 95 L80 335 M270 95 L270 335" stroke="{SD}" stroke-width="6" stroke-dasharray="10 10"/>' + text(390, 245, 'sama', 40, SD) +
     thumb_press(690, 280) + text(690, 400, 'lunak', 40, SD) + check(800, 120, 36))
out('big-w4d-ff-ukuran', H, b)

# 3 contoh: sayur kukus, buah lunak, telur dadar
H = 440
b = (floor(330, H) + plate(440, 290, 700) +
     carrot_stick(250, 270, 150, -12, 30) + carrot_stick(260, 310, 150, -6, 30) + steam(200, 220) +
     avocado(430, 280, 150, 4) + banana_stick(440, 320, 140, -4) +
     omelette(640, 270, 160, 8, 36) + omelette(630, 316, 160, 2, 36) +
     text(250, 110, 'kukus', 40, MUTED) + text(440, 110, 'matang', 40, MUTED) + text(640, 110, 'dadar', 40, MUTED))
out('big-w4d-ff-contoh', H, b)

# 4 tunda: kacang utuh, anggur utuh, popcorn, potongan keras
H = 440
b = (floor(330, H) + shadow(130, 300, 90) + nut(100, 250, 1.3, -10) + nut(170, 270, 1.1, 20) + cross(200, 150, 32) +
     shadow(340, 320, 70) + grapes(340, 200, 26) + cross(410, 120, 32) +
     shadow(560, 320, 70) + popcorn(560, 210, 1.3) + cross(630, 120, 32) +
     shadow(770, 310, 80) + apple_chunk(740, 260, 1.2) + carrot_stick(790, 250, 110, -70, 26, cooked=False) + cross(840, 150, 32) +
     text(130, 390, 'kacang', 34, MUTED) + text(340, 390, 'anggur', 34, MUTED) + text(560, 390, 'popcorn', 34, MUTED) + text(770, 390, 'mentah', 34, MUTED))
out('big-w4d-ff-tunda', H, b)

# 5 gagging berisik vs tersedak diam
H = 470
b = (floor(370, H) + rect(20, 20, 400, 420, CARD, 30, f'stroke="{LINE}" stroke-width="6"') + rect(460, 20, 400, 420, CARD, 30, f'stroke="{LINE}" stroke-width="6"') +
     tunas('kaget', 150, 175, 145, 140) + arcs(220, 210, 100, TERRA, 'both', 2) + tears(220, 225, 0.9) + pill(220, 90, 'berisik', SAGE, CARD, 40) + check(220, 380, 34) +
     f'<g opacity="0.9"><path d="M580 200 L620 200 L680 160 L680 300 L620 260 L580 260 Z" fill="{MUTED}"/>'
     f'<path d="M710 200 l50 50 M760 200 l-50 50" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/></g>' +
     pill(660, 90, 'diam', TERRA, CARD, 40) + pill(660, 380, 'tolong!', TD, CARD, 36))
out('big-w4d-ff-gagging', H, b)

# cheat: duduk tegak dan ditemenin
H = 600
y = seat('mama', 1.3, 430)
b = (floor(430, H) + person('mama', 600, y, 1.3, 'senang', 'none') + table(430, H) + shadow(250, 560, 150) + grp(chair(190, 180) + tunas('halo', 150, 175, 190, 30), 1.3, -60, -20))
out('big-w4d-ff-duduk', H, b)

autocrop(NAMES)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=420))).convert('RGBA') for n in NAMES]
    h = max(i.size[1] for i in ims); cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (420 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 420, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok', len(NAMES))
