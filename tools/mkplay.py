# Generates the flat play-idea art strips in design/svg/food/ (d13, d06). Run: python tools/mkplay.py
import math, os
OUT='/home/claude/temantumbuh/design/svg/food'
INK='#4a3f35'; MUTED='#7a6c5f'; TERRA='#e07856'; TD='#c46040'; SAGE='#7fa98f'; SD='#5f8a70'; SUN='#f3c45f'
BLUSH='#f6cdbd'; SKY='#9cc3e6'; LAV='#9479b8'; CARD='#fffdf9'; BOX='#d9a874'; BOXD='#b9844f'; TAPE='#ecd9a6'; LINE='#e9dccb'
def svg(name, body):
    open(f'{OUT}/art-{name}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 260">{body}</svg>')
def arrow(x1,y,x2,col=MUTED):
    return f'<path d="M{x1} {y} L{x2} {y} M{x2-20} {y-18} L{x2} {y} L{x2-20} {y+18}" stroke="{col}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def ell(cx,cy,rx,ry,f,extra=''): return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{f}" {extra}/>'
def circ(cx,cy,r,f,extra=''): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" {extra}/>'
def rrect(x,y,w,h,r,f,extra=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" {extra}/>'
def pompom(cx,cy,r,f):
    # fluffy ball: circle + tufts
    t=''.join(circ(cx+r*0.92*math.cos(a),cy+r*0.92*math.sin(a),r*0.28,f) for a in [i*math.pi/5 for i in range(10)])
    return t+circ(cx,cy,r,f)+circ(cx-r*0.3,cy-r*0.35,r*0.25,'#ffffff',' opacity="0.35"')
def bowl(cx,cy,w,f):
    h=w*0.42
    return (f'<path d="M{cx-w/2} {cy} Q{cx-w/2} {cy+h} {cx} {cy+h} Q{cx+w/2} {cy+h} {cx+w/2} {cy} Z" fill="{f}"/>'
            + ell(cx,cy,w/2,w*0.09,'#ffffff',' opacity="0.45"') + rrect(cx-w*0.18,cy+h-6,w*0.36,16,8,f))

# --- d13 motorik halus ---
# 1 sobek kertas: sheet with torn edge + torn pieces + little collage
jag=' '.join(f'L{200+ (14 if i%2 else -6)} {40+i*18}' for i in range(11))
b=(f'<path d="M80 40 L200 40 {jag} L200 230 L80 230 Z" fill="{SKY}"/>'
   f'<path d="M226 52 L262 46 L270 92 L238 104 Z" fill="{SKY}" transform="rotate(12 250 75)"/>'
   f'<path d="M248 150 L290 142 L284 186 L252 182 Z" fill="{SUN}"/>'
   f'<path d="M300 92 L330 84 L338 118 L306 122 Z" fill="{TERRA}" transform="rotate(-10 320 100)"/>'
   + arrow(380,135,500)+
   rrect(560,40,240,190,18,CARD,f'stroke="{LINE}" stroke-width="6"')+
   f'<path d="M600 190 L640 120 L680 190 Z" fill="{SAGE}"/><path d="M650 190 L700 100 L750 190 Z" fill="{SD}"/>'
   f'<path d="M700 70 L730 64 L736 92 L706 98 Z" fill="{SUN}"/><path d="M612 70 L640 66 L644 92 L616 94 Z" fill="{SKY}"/>')
svg('sobek-kertas',b)

# 2 jepit jemuran on cardboard edge
def pin(x,col):
    return (rrect(x-14,48,28,120,10,col)+rrect(x-3,60,6,90,3,'#ffffff',' opacity="0.4"')+
            circ(x,120,11,'#c8c2b8')+circ(x,120,5,MUTED))
b=(rrect(90,130,700,110,14,BOX)+rrect(90,130,700,26,10,BOXD)+
   ''.join(pin(x,c) for x,c in zip([200,330,460,590],[TERRA,SAGE,SUN,SKY]))+
   pin(720,LAV).replace('48','20',1).replace('<rect','<rect transform="rotate(25 720 90)"',1))
svg('jepit-jemuran',b)

# 3 ronce sedotan: wavy lace with straw pieces
pts=[(70+i*10, 140+40*math.sin(i/7)) for i in range(75)]
lace='M'+' L'.join(f'{x:.0f} {y:.0f}' for x,y in pts)
straws=''
cols=[TERRA,SAGE,SUN,SKY,LAV,TERRA,SAGE]
for k,i in enumerate(range(6,60,8)):
    x,y=pts[i]; x2,y2=pts[i+1]; ang=math.degrees(math.atan2(y2-y,x2-x))
    straws+=f'<rect x="{x-26}" y="{y-15}" width="52" height="30" rx="8" fill="{cols[k]}" transform="rotate({ang:.1f} {x} {y})"/>'
b=(f'<path d="{lace}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'+straws+
   circ(pts[0][0],pts[0][1],16,INK)+
   f'<rect x="{pts[-1][0]-4}" y="{pts[-1][1]-8}" width="40" height="16" rx="6" fill="{MUTED}" transform="rotate({math.degrees(math.atan2(pts[-1][1]-pts[-2][1],pts[-1][0]-pts[-2][0])):.1f} {pts[-1][0]} {pts[-1][1]})"/>')
svg('ronce-sedotan',b)

# 4 playdough: ball, flattened with finger dents, rolled snake, plastic knife
b=(circ(160,150,72,TERRA)+circ(136,124,18,'#ffffff',' opacity="0.3"')+
   ell(390,190,110,38,SAGE)+ell(360,182,14,8,SD)+ell(400,196,14,8,SD)+ell(436,180,14,8,SD)+
   f'<path d="M560 200 C600 140 650 230 700 170 S780 150 800 190" stroke="{SUN}" stroke-width="34" fill="none" stroke-linecap="round"/>'+
   f'<g transform="rotate(-30 640 80)">{rrect(560,66,90,26,12,SKY)}<path d="M650 70 L740 74 Q752 79 740 88 L650 88 Z" fill="#d6e6f4"/></g>')
svg('playdough',b)

# 5 pompom pindah pakai sendok: bowl with pompoms -> spoon carrying -> bowl
b=(bowl(160,150,200,SKY)+pompom(120,138,20,TERRA)+pompom(165,128,20,SUN)+pompom(205,140,20,SAGE)+pompom(150,150,18,LAV)+
   f'<path d="M330 92 Q440 30 550 92" stroke="{MUTED}" stroke-width="7" fill="none" stroke-dasharray="4 18" stroke-linecap="round"/>'+
   f'<path d="M532 76 L552 94 L526 102" stroke="{MUTED}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'+
   f'<g transform="rotate(-12 440 120)">{rrect(470,112,150,18,9,"#c8c2b8")}{ell(430,121,44,26,"#d8d2c8")}</g>'+
   pompom(432,104,20,TERRA)+
   bowl(700,150,200,BLUSH)+pompom(690,138,20,SKY))
svg('pompom-sendok',b)

# --- d06 main pas hujan ---
# 1 tenda selimut: two chairs + blanket draped, flashlight glow, book
def chair(x):
    return rrect(x,60,18,180,8,BOXD)+rrect(x-6,150,90 if x<400 else -90,16,8,BOXD) if False else ''
b=(rrect(150,60,16,180,7,BOXD)+rrect(150,150,80,14,7,BOXD)+rrect(214,150,14,90,7,BOXD)+
   rrect(714,60,16,180,7,BOXD)+rrect(650,150,80,14,7,BOXD)+rrect(650,150,14,90,7,BOXD)+
   f'<path d="M158 62 Q440 20 722 62 L800 240 L80 240 Z" fill="{SAGE}"/>'+
   f'<path d="M158 62 Q440 20 722 62" stroke="{SD}" stroke-width="8" fill="none"/>'+
   f'<path d="M440 70 L360 240 L520 240 Z" fill="{SUN}" opacity="0.35"/>'+
   f'<path d="M330 240 Q440 120 550 240 Z" fill="#2c3452" opacity="0.85"/>'+
   f'<path d="M405 212 L440 190 L475 212 L475 232 L440 214 L405 232 Z" fill="{TERRA}"/>'+
   f'<g transform="rotate(-20 470 160)">{rrect(450,150,50,18,8,SKY)}<path d="M500 146 L516 140 L516 176 L500 170 Z" fill="{SKY}"/></g>'+
   f'<path d="M520 150 L600 120 L600 200 Z" fill="{SUN}" opacity="0.5"/>')
svg('tenda-selimut',b)

# 2 harta karun: map with dashed path to X, star prize
b=(f'<path d="M90 50 L330 40 L350 220 L110 232 Z" fill="{TAPE}"/>'+
   f'<path d="M140 190 Q170 110 230 140 T300 80" stroke="{TD}" stroke-width="7" fill="none" stroke-dasharray="14 14" stroke-linecap="round"/>'+
   f'<path d="M286 64 L314 92 M314 64 L286 92" stroke="{TD}" stroke-width="10" stroke-linecap="round"/>'+
   circ(140,192,10,SD)+
   arrow(400,135,520)+
   rrect(580,120,200,110,16,BOX)+rrect(580,120,200,34,12,BOXD)+rrect(664,142,32,40,8,SUN)+
   f'<path d="M680 30 L692 62 L726 64 L700 84 L708 116 L680 98 L652 116 L660 84 L634 64 L668 62 Z" fill="{SUN}"/>')
svg('harta-karun',b)

# 3 jalan lakban: tape road with dashed middle, toy car, parking box
b=(f'<path d="M70 200 L420 200 Q520 200 520 110 L520 40" stroke="{TAPE}" stroke-width="80" fill="none" stroke-linejoin="round"/>'+
   f'<path d="M70 200 L420 200 Q520 200 520 110 L520 40" stroke="#ffffff" stroke-width="6" fill="none" stroke-dasharray="24 22"/>'+
   f'<g>{rrect(200,166,120,44,16,TERRA)}{rrect(230,146,60,30,10,TERRA)}{rrect(238,152,44,18,5,"#d6e6f4")}{circ(232,212,14,INK)}{circ(292,212,14,INK)}</g>'+
   f'<rect x="640" y="50" width="160" height="110" rx="6" fill="none" stroke="{TAPE}" stroke-width="16"/>'+
   f'<text x="720" y="125" font-family="sans-serif" font-weight="800" font-size="64" text-anchor="middle" fill="{SD}">P</text>')
svg('jalan-lakban',b)

# 4 joget patung: speaker with notes -> pause -> statue (freeze) star
b=(rrect(90,70,110,140,18,INK)+circ(145,165,32,MUTED)+circ(145,165,14,INK)+circ(145,105,14,MUTED)+
   f'<path d="M240 80 L240 140" stroke="{SAGE}" stroke-width="8" stroke-linecap="round"/>'+ell(228,142,16,12,SAGE)+
   f'<path d="M290 60 L290 120 M290 60 L320 66 L320 110" stroke="{TERRA}" stroke-width="8" fill="none" stroke-linecap="round"/>'+ell(278,122,16,12,TERRA)+ell(308,112,16,12,TERRA)+
   arrow(380,140,490)+
   circ(640,135,92,BLUSH)+rrect(605,90,24,90,8,TD)+rrect(651,90,24,90,8,TD)+
   f'<text x="800" y="70" font-family="sans-serif" font-weight="800" font-size="40" fill="{SD}">diam!</text>')
svg('joget-patung',b)

# 5 lomba beresin: stopwatch 3 menit -> toys into box
b=(circ(170,145,82,CARD,f'stroke="{INK}" stroke-width="10"')+rrect(156,40,28,22,6,INK)+
   f'<path d="M170 145 L170 92" stroke="{TD}" stroke-width="9" stroke-linecap="round"/>'+
   f'<path d="M170 145 L170 63 A82 82 0 0 1 241 104 Z" fill="{TERRA}" opacity="0.35"/>'+
   f'<text x="170" y="200" font-family="sans-serif" font-weight="800" font-size="34" text-anchor="middle" fill="{INK}">3 mnt</text>'+
   arrow(300,140,410)+
   rrect(560,140,240,96,14,BOX)+rrect(548,128,264,30,10,BOXD)+
   circ(610,92,30,SKY)+rrect(660,60,52,52,8,SUN)+f'<path d="M740 110 L770 52 L800 110 Z" fill="{SAGE}"/>'+
   f'<path d="M620 30 L640 50 M690 20 L690 44 M760 30 L744 48" stroke="{MUTED}" stroke-width="6" stroke-linecap="round"/>')
svg('lomba-beresin',b)
print('ok')
