# Scenes for w2e-d32-bantu-beresin (chores 1-3 yrs). Run: python tools/mkart_w2_chores.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artkit import *

def toybox(x, y, w=200, h=120):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{BOX}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{BOXD}"/>'
            f'<rect x="{x+w*0.55}" y="{y+26}" width="{w*0.45}" height="{h-26}" rx="0" fill="{BOXD}" opacity="0.25"/>')
def block(x, y, s, f, rot=0):
    return f'<g transform="rotate({rot} {x+s/2} {y+s/2})"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="8" fill="{f}"/><rect x="{x}" y="{y+s*0.6}" width="{s}" height="{s*0.4}" rx="8" fill="#000" opacity="0.08"/></g>'
def ball(cx, cy, r, f):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}"/><circle cx="{cx-r*0.35}" cy="{cy-r*0.35}" r="{r*0.3}" fill="#fff" opacity="0.4"/>'
def basket(x, y, w=190, h=130):
    weave = ''.join(f'<path d="M{x+12} {y+22+i*24} L{x+w-12} {y+22+i*24}" stroke="{BOXD}" stroke-width="5" opacity="0.5"/>' for i in range(5))
    return f'<path d="M{x} {y} L{x+w} {y} L{x+w-18} {y+h} L{x+18} {y+h} Z" fill="{BOX}"/>' + weave + f'<rect x="{x-8}" y="{y-10}" width="{w+16}" height="20" rx="10" fill="{BOXD}"/>'
def shirt(x, y, f, rot=0, s=1):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M-40 -30 L-15 -40 Q0 -28 15 -40 L40 -30 L52 -2 L30 6 L30 44 L-30 44 L-30 6 L-52 -2 Z" fill="{f}"/>'
            f'<path d="M-30 20 L30 20 L30 44 L-30 44 Z" fill="#000" opacity="0.07"/></g>')
def spark(x, y, s=1, col=SUN):
    return f'<path d="M{x} {y-16*s} L{x+5*s} {y-5*s} L{x+16*s} {y} L{x+5*s} {y+5*s} L{x} {y+16*s} L{x-5*s} {y+5*s} L{x-16*s} {y} L{x-5*s} {y-5*s} Z" fill="{col}"/>'

# HERO: Tunas carrying a block to the toy box, blocks already inside, sparkles
b = (floor(330, 420) + shadow(560, 395, 150) + toybox(470, 250, 230, 130) +
     block(500, 210, 56, SKY, -8) + ball(600, 226, 30, TERRA) + block(640, 214, 48, SUN, 10) +
     shadow(280, 395, 90) + tunas('hore', 160, 186, 200, 196) + block(320, 160, 60, SAGE, 14) +
     f'<path d="M380 170 Q430 130 480 190" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>' +
     spark(760, 150, 1.2) + spark(420, 90, 0.8, TERRA) + spark(150, 140, 0.9, SAGE) +
     ball(110, 360, 26, SKY) + block(760, 330, 44, TERRA, -12))
svg('hero-w2e-beresin', 420, b)

# BIG 1: research: Tunas with clipboard next to a focus target and a toy box
def target(cx, cy, r):
    return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r*k}" fill="{c}"/>' for k, c in ((1, TERRA), (0.72, CARD), (0.45, TERRA), (0.2, CARD)))
b = (floor(380, 500) + shadow(250, 450, 110) + tunas('riset', 170, 198, 165, 255) +
     target(470, 250, 110) + f'<path d="M640 120 L486 246" stroke="{SD}" stroke-width="10" stroke-linecap="round"/><path d="M640 120 L676 108 L664 146 Z" fill="{SD}"/>' +
     toybox(640, 340, 180, 100) + block(665, 306, 44, SKY) + ball(755, 318, 24, SUN) +
     text(470, 420, 'fokus', 46, SD))
svg('big-w2e-riset-fokus', 500, b)

# BIG 2: toys into the box, with a music note (clean-up song)
b = (floor(380, 500) + shadow(560, 455, 140) + toybox(450, 320, 230, 130) + block(480, 285, 52, SKY, -6) + ball(580, 296, 28, TERRA) +
     shadow(260, 455, 90) + tunas('hore', 150, 175, 180, 270) + block(300, 230, 58, SUN, 18) +
     f'<path d="M360 240 Q410 200 470 270" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>' +
     f'<path d="M760 150 L760 240" stroke="{SAGE}" stroke-width="9" stroke-linecap="round"/><ellipse cx="744" cy="242" rx="20" ry="15" fill="{SAGE}"/>' +
     f'<path d="M810 120 L810 210 M810 120 L850 130 L850 196" stroke="{TERRA}" stroke-width="9" fill="none" stroke-linecap="round"/><ellipse cx="794" cy="212" rx="20" ry="15" fill="{TERRA}"/><ellipse cx="834" cy="198" rx="20" ry="15" fill="{TERRA}"/>' +
     block(90, 410, 40, SAGE, 8) + ball(150, 430, 20, SUN))
svg('big-w2e-mainan-kotak', 500, b)

# BIG 3: dirty clothes into the basket
b = (floor(380, 500) + shadow(600, 460, 130) + basket(510, 320, 190, 130) + shirt(600, 300, SKY, -12, 0.9) +
     shadow(280, 460, 90) + tunas('santai', 150, 175, 200, 280) + shirt(380, 230, TERRA, 25, 0.8) +
     f'<path d="M420 210 Q480 170 540 260" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>' +
     shirt(120, 430, SUN, -8, 0.6))
svg('big-w2e-baju-keranjang', 500, b)

# BIG 4: wiping a spill with a small cloth
b = (floor(360, 500) + f'<rect x="120" y="230" width="460" height="26" rx="10" fill="{BOX}"/><rect x="150" y="256" width="20" height="150" rx="8" fill="{BOXD}"/><rect x="530" y="256" width="20" height="150" rx="8" fill="{BOXD}"/>' +
     f'<g transform="rotate(80 260 200)"><rect x="230" y="160" width="60" height="80" rx="12" fill="{SKY}"/><rect x="230" y="160" width="60" height="18" rx="9" fill="{SKYD}"/></g>' +
     f'<path d="M290 228 Q360 210 430 226 Q470 232 440 238 L300 240 Z" fill="#d6e6f4"/>' +
     f'<path d="M380 400 Q430 380 480 400 Q520 410 470 420 L390 420 Z" fill="#d6e6f4"/>' +
     shadow(680, 455, 100) + tunas('hore', 150, 175, 600, 280) +
     f'<g transform="rotate(-12 560 380)"><rect x="520" y="360" width="90" height="46" rx="10" fill="{SUN}"/><path d="M530 372 L600 372 M530 388 L600 388" stroke="{SUND}" stroke-width="4"/></g>' +
     spark(470, 360, 0.8, SKY))
svg('big-w2e-lap-tumpahan', 500, b)

# BIG 5: setting the table with spoons and napkins
def spoon(x, y, rot):
    return f'<g transform="rotate({rot} {x} {y})"><rect x="{x}" y="{y}" width="70" height="12" rx="6" fill="#c8c2b8"/><ellipse cx="{x-14}" cy="{y+6}" rx="20" ry="13" fill="#d8d2c8"/></g>'
def napkin(x, y, f):
    return f'<path d="M{x} {y} L{x+70} {y} L{x+70} {y+60} L{x} {y+60} Z" fill="{f}"/><path d="M{x} {y} L{x+70} {y+60}" stroke="#fff" stroke-width="4" opacity="0.5"/>'
b = (floor(380, 500) + f'<ellipse cx="420" cy="300" rx="320" ry="70" fill="{BOX}"/><ellipse cx="420" cy="290" rx="320" ry="70" fill="#e8c493"/>' +
     f'<rect x="200" y="330" width="22" height="120" rx="8" fill="{BOXD}"/><rect x="620" y="330" width="22" height="120" rx="8" fill="{BOXD}"/>' +
     napkin(200, 255, BLUSH) + spoon(220, 280, -10) + napkin(420, 245, '#e3eee6') + spoon(440, 270, 8) +
     f'<ellipse cx="640" cy="286" rx="52" ry="18" fill="{CARD}" stroke="{LINE}" stroke-width="5"/>' +
     shadow(790, 455, 70) + tunas('hore', 130, 152, 720, 300) + spoon(700, 250, -40))
svg('big-w2e-siapin-meja', 500, b)

autocrop(['hero-w2e-beresin', 'big-w2e-riset-fokus', 'big-w2e-mainan-kotak', 'big-w2e-baju-keranjang', 'big-w2e-lap-tumpahan', 'big-w2e-siapin-meja'])
print('ok')
