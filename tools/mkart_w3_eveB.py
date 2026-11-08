# Scenes for the week-3 evening group B posts:
#   w3e-kata-pertama (speech stages), w3e-main-nunggu-masak (kitchen-side play), w3e-jawaban-sopan-2 (polite replies).
# Run: python tools/mkart_w3_eveB.py [contact-sheet.png]
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import *

H, T = 520, 440

def spark(x, y, s=1, col=SUN):
    return f'<path d="M{x} {y-16*s} L{x+5*s} {y-5*s} L{x+16*s} {y} L{x+5*s} {y+5*s} L{x} {y+16*s} L{x-5*s} {y+5*s} L{x-16*s} {y} L{x-5*s} {y-5*s} Z" fill="{col}"/>'
def heart(x, y, s, col=TERRA):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 8 C-14 -8 -30 6 0 30 C30 6 14 -8 0 8 Z" fill="{col}"/>'
def ball(cx, cy, r, f):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}"/><circle cx="{cx-r*0.35}" cy="{cy-r*0.35}" r="{r*0.3}" fill="#fff" opacity="0.4"/>'
def waves(x, y, s=1, col=MUTED, flip=False):
    k = -1 if flip else 1
    return ''.join(f'<path d="M{x+k*i*16*s} {y-(14+i*8)*s} Q{x+k*(10+i*16)*s} {y} {x+k*i*16*s} {y+(14+i*8)*s}" stroke="{col}" stroke-width="{5*s}" fill="none" stroke-linecap="round" opacity="0.6"/>' for i in range(3))
def basket(x, y, w=190, h=120, col=BOX, cold=BOXD):
    weave = ''.join(f'<path d="M{x+14} {y+22+i*22} L{x+w-14} {y+22+i*22}" stroke="{cold}" stroke-width="5" opacity="0.5"/>' for i in range(int((h - 20) / 22)))
    return f'<path d="M{x} {y} L{x+w} {y} L{x+w-16} {y+h} L{x+16} {y+h} Z" fill="{col}"/>' + weave + f'<rect x="{x-8}" y="{y-10}" width="{w+16}" height="20" rx="10" fill="{cold}"/>'
def carrot(x, y, s=1, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M-14 -40 Q0 -48 14 -40 L3 40 Q0 46 -3 40 Z" fill="{TERRA}"/>'
            f'<path d="M-8 -20 L2 -20 M-6 0 L4 0 M-4 18 L3 18" stroke="{TD}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M0 -44 Q-14 -66 -18 -60 M0 -44 Q0 -70 4 -68 M0 -44 Q14 -64 18 -58" stroke="{SAGE}" stroke-width="6" fill="none" stroke-linecap="round"/></g>')
def potato(x, y, s=1):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{34*s}" ry="{24*s}" fill="#d9b27c"/><ellipse cx="{x+8*s}" cy="{y+8*s}" rx="{22*s}" ry="{12*s}" fill="#c49a62" opacity="0.5"/>'
            f'<circle cx="{x-12*s}" cy="{y-6*s}" r="{3*s}" fill="#a87f4a"/><circle cx="{x+10*s}" cy="{y-10*s}" r="{3*s}" fill="#a87f4a"/>')
def orange(x, y, r=28):
    return ball(x, y, r, '#f2a54a') + f'<path d="M{x} {y-r} q6 -12 16 -10" stroke="{SAGE}" stroke-width="5" fill="none" stroke-linecap="round"/>'
def apple(x, y, r=28, col='#d9604a'):
    return (f'<path d="M{x} {y-r*0.7} Q{x+r*1.1} {y-r*1.2} {x+r} {y+r*0.2} Q{x+r*0.8} {y+r} {x} {y+r*0.85} Q{x-r*0.8} {y+r} {x-r} {y+r*0.2} Q{x-r*1.1} {y-r*1.2} {x} {y-r*0.7} Z" fill="{col}"/>'
            f'<path d="M{x} {y-r*0.7} L{x+3} {y-r*1.15}" stroke="{BOXD}" stroke-width="5" stroke-linecap="round"/><ellipse cx="{x+r*0.35}" cy="{y-r*1.05}" rx="{r*0.3}" ry="{r*0.14}" fill="{SAGE}"/>'
            f'<circle cx="{x-r*0.4}" cy="{y-r*0.15}" r="{r*0.2}" fill="#fff" opacity="0.35"/>')
def fridge(x, y, w=230, h=420):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#e6eef5"/><rect x="{x+w*0.6}" y="{y}" width="{w*0.4}" height="{h}" rx="22" fill="#d5e2ee"/>'
            f'<rect x="{x}" y="{y+h*0.36}" width="{w}" height="8" fill="#c3d3e2"/>'
            f'<rect x="{x+w-36}" y="{y+40}" width="12" height="70" rx="6" fill="#b5c7d8"/><rect x="{x+w-36}" y="{y+h*0.36+30}" width="12" height="90" rx="6" fill="#b5c7d8"/>')
def tape(x, y, w=70, rot=0, col='#f3e3b4', peel=False):
    end = f'<path d="M{x+w} {y} l18 -16 l6 8 l-16 22 Z" fill="{col}" opacity="0.9"/>' if peel else ''
    return f'<g transform="rotate({rot} {x+w/2} {y+11})"><rect x="{x}" y="{y}" width="{w}" height="22" rx="3" fill="{col}"/><rect x="{x}" y="{y}" width="{w}" height="22" rx="3" fill="none" stroke="#e2cf96" stroke-width="2"/>{end}</g>'
def stove_safe(x, y, w=230):
    """Stove with the pot handle turned to the back (AAP)."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="10" fill="#c8c2b8"/><rect x="{x}" y="{y+40}" width="{w}" height="150" rx="10" fill="{BOX}"/>'
            f'<rect x="{x+16}" y="{y+60}" width="{w-32}" height="110" rx="8" fill="{BOXD}" opacity="0.4"/>'
            f'<path d="M{x+50} {y} L{x+50} {y-60} Q{x+50} {y-70} {x+60} {y-70} L{x+170} {y-70} Q{x+180} {y-70} {x+180} {y-60} L{x+180} {y} Z" fill="{SKYD}"/>'
            f'<rect x="{x+40}" y="{y-80}" width="150" height="16" rx="8" fill="{SKY}"/>'
            f'<rect x="{x+100}" y="{y-92}" width="30" height="14" rx="7" fill="{INK}" opacity="0.7"/>'
            f'<path d="M{x+90} {y-100} q-12 -20 0 -40 M{x+140} {y-100} q-12 -20 0 -40" stroke="{MUTED}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.45"/>')
def paperball(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eceae4"/><path d="M{cx-r*0.7} {cy-r*0.2} L{cx-r*0.1} {cy+r*0.1} L{cx+r*0.5} {cy-r*0.5} M{cx-r*0.3} {cy+r*0.6} L{cx+r*0.2} {cy+r*0.2}" stroke="#c9c5bb" stroke-width="3" fill="none"/>'
            f'<path d="M{cx-r} {cy+r*0.15} Q{cx} {cy+r*0.45} {cx+r} {cy+r*0.15} L{cx+r*0.96} {cy+r*0.42} Q{cx} {cy+r*0.72} {cx-r*0.96} {cy+r*0.42} Z" fill="#f3e3b4"/>')
def tissuebox(x, y, w=200, h=120):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{SKY}"/><rect x="{x+w*0.6}" y="{y}" width="{w*0.4}" height="{h}" rx="14" fill="{SKYD}" opacity="0.5"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+18}" rx="{w*0.3}" ry="12" fill="{SKYD}"/>'
            + ''.join(f'<circle cx="{x+30+i*36}" cy="{y+h*0.62}" r="8" fill="{CARD}" opacity="0.6"/>' for i in range(4)))
def cloth(x0, y0, x1, y1, col, wid=46):
    return f'<path d="M{x0-wid/2} {y0} Q{(x0+x1)/2-30} {(y0+y1)/2} {x1-wid/2} {y1} L{x1+wid/2} {y1+8} Q{(x0+x1)/2+30} {(y0+y1)/2+10} {x0+wid/2} {y0} Z" fill="{col}"/>'
def car(x, y, s=1, col=TERRA):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-70 0 L-70 -30 Q-66 -40 -50 -40 L-30 -40 L-14 -66 L36 -66 L56 -40 L66 -38 Q74 -36 74 -26 L74 0 Z" fill="{col}"/>'
            f'<path d="M-8 -60 L32 -60 L46 -42 L-18 -42 Z" fill="#d6e6f4"/><circle cx="-38" cy="2" r="18" fill="{INK}"/><circle cx="44" cy="2" r="18" fill="{INK}"/>'
            f'<circle cx="-38" cy="2" r="7" fill="#c8c2b8"/><circle cx="44" cy="2" r="7" fill="#c8c2b8"/></g>')
def cat(x, y, s=1):
    c = '#e8a65a'
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="40" rx="62" ry="40" fill="{c}"/><circle cx="-48" cy="-6" r="38" fill="{c}"/>'
            f'<path d="M-80 -24 L-76 -64 L-56 -38 Z M-40 -40 L-24 -64 L-16 -26 Z" fill="{c}"/>'
            f'<circle cx="-62" cy="-8" r="5" fill="{INK}"/><circle cx="-36" cy="-8" r="5" fill="{INK}"/><path d="M-54 6 q5 6 10 0" stroke="{INK}" stroke-width="3" fill="none"/>'
            f'<path d="M58 30 Q100 10 90 -30" stroke="{c}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<path d="M-20 20 L-6 50 M10 14 L20 46" stroke="#cf8a40" stroke-width="6" stroke-linecap="round"/></g>')
def walker_steps(x, y):
    return ''.join(f'<ellipse cx="{x+i*70}" cy="{y-(i%2)*24}" rx="18" ry="11" fill="{BOXD}" opacity="{0.25+i*0.15}"/>' for i in range(4))

# ---------------- POST 1: w3e-kata-pertama ----------------
# HERO: Mama and Adek face to face, taking turns: "aaa" / "ooo?"
m = seat('mama', 1.42, T); a = seat('adek', 1.4, T)
b = (person('mama', 250, m, 1.42, 'senang', 'none') + person('adek', 640, a, 1.4, 'senang', 'none') + table(T, H) +
     bubble(470, 0, 250, ['aaa!'], 'br', size=46) + bubble(60, 10, 250, ['ooo?'], 'br', size=46) +
     heart(450, 330, 1.1) + spark(800, 120, 1.0) + spark(70, 230, 0.8, SAGE))
svg('hero-w3e-ocehan', H, b)

# 1: 2-4 months: baby coos, Mama answers then waits (pause dots)
m = seat('mama', 1.38, T); a = seat('adek', 1.05, T)
b = (person('mama', 260, m, 1.38, 'lembut', 'none') + person('adek', 640, a, 1.05, 'senang', 'none') + table(T, H) +
     bubble(560, 30, 230, ['ooo'], 'bl', size=44) + bubble(40, 0, 330, ['aaa, gitu ya?'], 'br', size=38) +
     ''.join(f'<circle cx="{410+i*30}" cy="230" r="9" fill="{MUTED}" opacity="0.55"/>' for i in range(3)))
svg('big-w3e-aaa-ooo', H, b)

# 2: 6 months: raspberries, Ayah copies (the dad is the clown)
y = seat('ayah', 1.4, T); a = seat('adek', 1.12, T)
b = (person('ayah', 270, y, 1.4, 'kaget', 'none') + person('adek', 640, a, 1.12, 'senang', 'none') + table(T, H) +
     bubble(520, 10, 240, ['brrr!'], 'bl', size=46) + bubble(60, 0, 290, ['brrrr?'], 'br', size=46) +
     ''.join(f'<circle cx="{c}" cy="{cy}" r="{r}" fill="{SKY}" opacity="0.7"/>' for c, cy, r in ((400, 250, 7), (420, 225, 5), (520, 255, 6), (500, 230, 4))))
svg('big-w3e-brrr', H, b)

# 3: 9 months: "bababa" -> Mama turns it into a word with a ball
m = seat('mama', 1.38, T); a = seat('adek', 1.2, T)
b = (person('mama', 250, m, 1.38, 'senang', 'none') + person('adek', 650, a, 1.2, 'kaget', 'none') + table(T, H) +
     bubble(520, 0, 300, ['bababa'], 'bl', size=44) + bubble(40, 10, 300, ['ba... bola!'], 'br', size=42) +
     ball(450, T - 50, 50, TERRA))
svg('big-w3e-bababa', H, b)

# 4: 12-18 months: first word, Ayah names what Adek looks at
y = seat('ayah', 1.36, T); a = seat('adek', 1.25, T)
b = (person('adek', 230, a, 1.25, 'kaget', 'none') + person('ayah', 520, y, 1.36, 'senang', 'none') + table(T, H) +
     cat(760, T - 60, 0.9) + bubble(80, 10, 220, ['cing!'], 'br', size=46) + bubble(390, 0, 330, ['Itu kucing.'], 'bl', size=40) +
     f'<path d="M330 330 Q500 250 650 360" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>')
svg('big-w3e-kata-pertama', H, b)

# 5: 18-24 months: two words, Mama adds one more
m = seat('mama', 1.38, T); a = seat('adek', 1.3, T, True)
b = (person('adek', 640, a, 1.3, 'senang', 'pegang') + person('mama', 230, m, 1.38, 'senang', 'none') + table(T, H) +
     car(430, T + 44, 0.9) + bubble(520, 0, 330, ['mobil jalan'], 'bl', size=40) + bubble(10, 10, 420, ['jalan cepat ya!'], 'br', size=40))
svg('big-w3e-dua-kata', H, b)

# ---------------- POST 2: w3e-main-nunggu-masak ----------------
# HERO: fridge with paper tape, Tunas peeling a strip, stove far away with a safe-distance marker
b = (floor(330, 420) + fridge(60, 20, 210, 370) + tape(90, 90, 70, -8) + tape(170, 140, 70, 12, '#f6cdbd') + tape(95, 200, 80, 4, '#d6e6f4') +
     tape(150, 270, 70, -14, '#e3eee6') + shadow(370, 400, 80) + tunas('hore', 140, 162, 300, 236) +
     tape(250, 240, 64, -30, '#f3e3b4') + stove_safe(620, 210, 220) +
     f'<path d="M470 360 L600 360" stroke="{TERRA}" stroke-width="6" stroke-dasharray="4 14" stroke-linecap="round"/>' +
     text(535, 340, 'jauh', 30, TD) + spark(470, 150, 0.9) + spark(560, 90, 0.7, SAGE))
svg('hero-w3e-masak-main', 420, b)

# 1: paper tape on the fridge door
b = (floor(380, 500) + fridge(330, 10, 230, 440) + tape(360, 90, 80, -10) + tape(450, 150, 70, 14, '#f6cdbd') + tape(370, 220, 90, 6, '#d6e6f4') +
     tape(450, 300, 70, -16, '#e3eee6') + tape(370, 360, 70, 10, '#f3e3b4', True) + shadow(250, 460, 80) + tunas('hore', 150, 174, 160, 290) +
     tape(110, 430, 60, -20, '#f6cdbd') + spark(640, 120, 1.0) +
     f'<g opacity="0.9"><circle cx="720" cy="300" r="34" fill="{CARD}" stroke="{TERRA}" stroke-width="6"/><circle cx="720" cy="300" r="12" fill="{TERRA}"/>'
     f'<path d="M694 274 L746 326" stroke="{TD}" stroke-width="8" stroke-linecap="round"/></g>' + text(720, 372, 'magnet', 26, TD))
svg('big-w3e-lakban-kulkas', 500, b)

# 2: newspaper + tape balls into a laundry basket (balls about orange size, never small)
b = (floor(380, 500) + shadow(620, 465, 140) + basket(500, 320, 250, 140) + paperball(575, 300, 46) + paperball(675, 306, 42) +
     shadow(250, 465, 90) + tunas('hore', 170, 197, 165, 272) + paperball(390, 190, 48) +
     f'<path d="M440 175 Q530 120 600 270" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="3 16" stroke-linecap="round"/>' +
     paperball(100, 430, 40) + orange(820, 440, 34))
svg('big-w3e-bola-koran', 500, b)

# 3: sorting whole carrots, potatoes, oranges, apples into two baskets by colour
b = (floor(380, 500) + basket(80, 330, 190, 110, '#f6d7b8', '#e2b48a') + carrot(130, 300, 0.8, -20) + orange(190, 312, 26) + carrot(230, 300, 0.75, 15) +
     basket(600, 330, 190, 110, '#e3eee6', SAGE) + apple(650, 310, 26, SAGE) + potato(720, 316, 1.0) +
     shadow(440, 460, 80) + tunas('mikir', 150, 174, 365, 280) + orange(330, 448, 26) + apple(560, 452, 24) +
     text(175, 480, 'oranye', 28, TD) + text(695, 480, 'lainnya', 28, SD))
svg('big-w3e-sortir-sayur', 520, b)

# 4: pulling cloths out of an empty tissue box
b = (floor(380, 500) + shadow(560, 465, 120) + tissuebox(460, 340, 200, 120) + cloth(560, 350, 460, 250, BLUSH) + cloth(580, 350, 690, 270, SUN) +
     cloth(545, 350, 520, 180, '#e3eee6') + shadow(270, 465, 90) + tunas('hore', 170, 197, 185, 270) + cloth(390, 300, 340, 450, SAGE, 44) +
     f'<path d="M760 360 l40 0 M780 340 l0 40" stroke="{TD}" stroke-width="6" stroke-linecap="round" opacity="0"/>' + spark(720, 160, 1.0) + spark(400, 140, 0.7, TERRA))
svg('big-w3e-kotak-tisu', 500, b)

# 5: live cooking commentary: Adek in the high chair far from the stove, Mama narrates while cutting carrots
m = seat('mama', 1.3, T, True)
b = (stove_safe(620, T - 120, 220) + person('mama', 470, m, 1.3, 'senang', 'pegang') + table(T, H) +
     carrot(440, T + 20, 0.7, 80) + carrot(520, T + 30, 0.6, 95) +
     f'<rect x="20" y="{T-150}" width="190" height="20" rx="10" fill="{SKY}"/>' + person('adek', 120, T - 250, 0.95, 'senang', 'none') +
     f'<rect x="20" y="{T-140}" width="200" height="22" rx="10" fill="{SKY}"/><rect x="40" y="{T-118}" width="20" height="{H-T+118}" fill="{BOXD}"/><rect x="180" y="{T-118}" width="20" height="{H-T+118}" fill="{BOXD}"/>' +
     bubble(230, 0, 400, ['Wortelnya Mama potong.'], 'br', size=34))
svg('big-w3e-siaran-masak', H, b)

# ---------------- POST 3: w3e-jawaban-sopan-2 ----------------
# relative's comment arrives as a bubble from off-frame (no relative drawn), the family answers calmly
def off_bubble(x, y, w, lines, size=34):
    return bubble(x, y, w, lines, 'none', size=size, col='#f3e8da')

def badge(cx, cy, label, w=170):
    return f'<rect x="{cx-w/2}" y="{cy-34}" width="{w}" height="68" rx="34" fill="{SAGE}"/>' + text(cx, cy + 12, label, 36, CARD)
RB = dict(x=540, y=40, w=330)   # where the off-frame comment sits: upper right, beside the faces

# HERO: Mama holding Adek close, comment bubble "Nanti bau tangan lho", hearts
m = seat('mama', 1.62, T); a = seat('adek', 1.3, T)
b = (person('adek', 470, a, 1.3, 'senang', 'none') + person('mama', 230, m, 1.62, 'lembut', 'peluk') + table(T, H) +
     off_bubble(RB['x'] + 20, RB['y'], 310, ['"Nanti bau', 'tangan lho."'], 36) + heart(700, 250, 1.4) + heart(780, 320, 0.9, SUN) + heart(620, 330, 0.8, BLUSH))
svg('hero-w3e-bau-tangan', H, b)

# 1: "kok belum bisa jalan?" Mama relaxed, Adek happy, range badge
m = seat('mama', 1.55, T); a = seat('adek', 1.45, T)
b = (person('mama', 180, m, 1.55, 'senang', 'none') + person('adek', 420, a, 1.45, 'senang', 'none') + table(T, H) +
     off_bubble(RB['x'], RB['y'], RB['w'], ['"Kok belum', 'bisa jalan?"'], 36) + badge(705, 290, '8-18 bln', 190))
svg('big-w3e-belum-jalan', H, b)

# 2: "digendong terus?" Ayah holding Adek happily
y = seat('ayah', 1.6, T); a = seat('adek', 1.3, T)
b = (person('adek', 460, a, 1.3, 'senang', 'none') + person('ayah', 220, y, 1.6, 'senang', 'peluk') + table(T, H) +
     off_bubble(RB['x'], RB['y'], RB['w'], ['"Kok digendong', 'terus?"'], 36) + heart(690, 260, 1.3) + heart(780, 330, 0.9, SUN))
svg('big-w3e-digendong', H, b)

# 3: "kok pendiam?" Adek peeking from behind Ayah, Ayah laughing at himself
y = seat('ayah', 1.6, T); a = seat('adek', 1.2, T)
b = (person('adek', 400, a, 1.2, 'lembut', 'none') + person('ayah', 210, y, 1.6, 'senang', 'none') + table(T, H) +
     off_bubble(RB['x'], RB['y'], RB['w'], ['"Kok pendiam', 'banget?"'], 36) +
     bubble(560, 240, 250, ['ngamatin', 'dulu'], 'bl', size=32, think=True))
svg('big-w3e-pendiam', H, b)

# 4: "emang kenyang cuma ASI?" Mama cuddling a small baby, 0-6 months badge
m = seat('mama', 1.6, T); a = seat('adek', 1.05, T)
b = (person('adek', 440, a, 1.05, 'lembut', 'none') + person('mama', 220, m, 1.6, 'lembut', 'peluk') + table(T, H) +
     off_bubble(RB['x'], RB['y'], RB['w'], ['"Emang kenyang', 'cuma ASI?"'], 36) + badge(705, 300, '0-6 bln', 180))
svg('big-w3e-asi-kenyang', H, b)

# 5: "kok belum disapih?" Mama and toddler Adek, a "2 tahun+" badge
m = seat('mama', 1.5, T); a = seat('adek', 1.45, T)
b = (person('mama', 180, m, 1.5, 'senang', 'none') + person('adek', 420, a, 1.45, 'senang', 'none') + table(T, H) +
     off_bubble(RB['x'], RB['y'], RB['w'], ['"Kok belum', 'disapih?"'], 36) +
     f'<circle cx="705" cy="310" r="78" fill="{SUN}"/><circle cx="705" cy="310" r="64" fill="none" stroke="{CARD}" stroke-width="4" stroke-dasharray="6 8"/>' +
     text(705, 308, '2 thn', 40, INK) + text(705, 346, 'atau +', 28, INK))
svg('big-w3e-sapih', H, b)

names = ['hero-w3e-ocehan', 'big-w3e-aaa-ooo', 'big-w3e-brrr', 'big-w3e-bababa', 'big-w3e-kata-pertama', 'big-w3e-dua-kata',
         'hero-w3e-masak-main', 'big-w3e-lakban-kulkas', 'big-w3e-bola-koran', 'big-w3e-sortir-sayur', 'big-w3e-kotak-tisu', 'big-w3e-siaran-masak',
         'hero-w3e-bau-tangan', 'big-w3e-belum-jalan', 'big-w3e-digendong', 'big-w3e-pendiam', 'big-w3e-asi-kenyang', 'big-w3e-sapih']
autocrop(names)
if len(sys.argv) > 1:
    import cairosvg
    from PIL import Image
    ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(OUT, n + '.svg'), output_width=440))).convert('RGBA') for n in names]
    h = max(i.size[1] for i in ims); cols = 6; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (440 * cols, h * rows), '#fbf4ea')
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 440, (k // cols) * h), im)
    sheet.save(sys.argv[1])
print('ok')
