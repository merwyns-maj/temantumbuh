# Art strips for d10 rotasi mainan; reuses helpers from mkplay.py. Run: python tools/mkplay2.py
import math
exec(open(__file__.replace('mkplay2.py','mkplay.py')).read().split('# --- d13')[0])
def blocks(x,y,s):
    return rrect(x,y,s,s,6,SUN)+rrect(x+s+6,y,s,s,6,SKY)+rrect(x+s/2+3,y-s-6,s,s,6,TERRA)
def book(cx,cy,w,col):
    return (f'<path d="M{cx-w} {cy+30} L{cx-w} {cy-20} Q{cx-w/2} {cy-30} {cx} {cy-18} L{cx} {cy+40} Q{cx-w/2} {cy+26} {cx-w} {cy+30} Z" fill="{col}"/>'
            f'<path d="M{cx+w} {cy+30} L{cx+w} {cy-20} Q{cx+w/2} {cy-30} {cx} {cy-18} L{cx} {cy+40} Q{cx+w/2} {cy+26} {cx+w} {cy+30} Z" fill="{col}" opacity="0.8"/>')
# 1 simpan setengah: shelf with 3 toys | arrow | closed box with toys peeking
b=(rrect(80,80,300,14,6,BOXD)+rrect(80,190,300,14,6,BOXD)+rrect(80,80,14,160,6,BOXD)+rrect(366,80,14,160,6,BOXD)+
   circ(150,160,28,SKY)+blocks(220,150,30)+book(320,150,34,SAGE)+
   arrow(430,140,540)+
   rrect(600,110,220,120,14,BOX)+rrect(588,96,244,30,10,BOXD)+
   f'<text x="710" y="190" font-family="sans-serif" font-weight="800" font-size="30" text-anchor="middle" fill="{CARD}">SIMPAN</text>')
svg('simpan-setengah',b)
# 2 tukar tiap minggu: two boxes with circular swap arrows and a calendar
b=(rrect(90,120,180,110,14,BOX)+rrect(80,106,200,28,10,BOXD)+circ(180,175,22,SKY)+
   rrect(610,120,180,110,14,BOX)+rrect(600,106,200,28,10,BOXD)+rrect(680,155,40,40,6,SUN)+
   f'<path d="M320 120 Q440 30 560 120" stroke="{SD}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M540 96 L562 122 L532 132" stroke="{SD}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'+
   f'<path d="M560 200 Q440 260 320 200" stroke="{TD}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M340 224 L318 198 L348 190" stroke="{TD}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'+
   rrect(390,110,100,90,12,CARD,f'stroke="{LINE}" stroke-width="5"')+rrect(390,110,100,26,10,TERRA)+
   f'<text x="440" y="180" font-family="sans-serif" font-weight="800" font-size="30" text-anchor="middle" fill="{INK}">MGG</text>')
svg('tukar-minggu',b)
# 3 campur jenis: ball (gerak), blocks (nyusun), teacup (pura-pura), book
b=(circ(150,150,62,TERRA)+f'<path d="M92 140 Q150 110 208 140 M150 88 L150 212" stroke="{CARD}" stroke-width="6" fill="none" opacity="0.6"/>'+
   blocks(300,170,50)+
   f'<path d="M520 120 L610 120 L600 200 Q565 215 530 200 Z" fill="{BLUSH}"/><path d="M610 140 Q645 145 630 175 Q622 185 604 182" stroke="{BLUSH}" stroke-width="12" fill="none"/>'+ell(565,210,70,12,LINE)+
   book(760,150,64,SAGE))
svg('campur-jenis',b)
# 4 banyak cara: kardus -> car, house, drum
def kardus(x,y,w,h): return rrect(x,y,w,h,8,BOX)+f'<path d="M{x} {y} L{x+w*0.3} {y-24} M{x+w} {y} L{x+w*0.7} {y-24}" stroke="{BOXD}" stroke-width="8" stroke-linecap="round"/>'
b=(kardus(80,110,150,110)+
   f'<path d="M260 120 L330 70 M260 160 L330 160 M260 200 L330 250" stroke="{MUTED}" stroke-width="7" stroke-linecap="round"/>'+
   rrect(380,40,130,60,10,BOX)+circ(410,104,14,INK)+circ(480,104,14,INK)+rrect(440,22,50,28,6,BOX)+
   rrect(560,130,110,80,6,BOX)+f'<path d="M550 132 L615 80 L680 132 Z" fill="{TD}"/>'+rrect(600,165,30,45,4,BOXD)+
   rrect(720,170,110,70,10,BOX)+ell(775,170,55,12,BOXD)+f'<path d="M740 120 L770 160 M820 120 L790 160" stroke="{MUTED}" stroke-width="7" stroke-linecap="round"/>'+circ(740,118,9,TERRA)+circ(820,118,9,TERRA))
svg('banyak-cara',b)
print('ok')
