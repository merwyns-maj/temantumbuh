# Art strips for d25 lempar makanan, d16 lauk MPASI pasar, d17 main 5 menit; reuses helpers from mkplay.py.
import math
exec(open(__file__.replace('mkplay3.py','mkplay.py')).read().split('# --- d13')[0])
def text(x,y,s,size,col,anchor='middle'):
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-weight="800" font-size="{size}" text-anchor="{anchor}" fill="{col}">{s}</text>'
def plate(cx,cy,w): return ell(cx,cy,w/2,w*0.16,CARD,f'stroke="{LINE}" stroke-width="6"')
def steam(x,y): return ''.join(f'<path d="M{x+i*26} {y} q-10 -18 0 -34 q10 -16 0 -32" stroke="{MUTED}" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>' for i in range(3))
# ---- d25 lempar makanan
b=(rrect(80,70,330,26,12,SKY)+rrect(110,96,20,150,8,'#c8c2b8')+
   f'<g transform="rotate(28 330 60)">{bowl(330,60,110,TERRA)}</g>'+
   f'<path d="M380 90 Q470 100 520 200" stroke="{MUTED}" stroke-width="6" fill="none" stroke-dasharray="4 16" stroke-linecap="round"/>'+
   circ(450,120,12,SUN)+circ(490,160,10,SAGE)+circ(470,150,9,SUN)+
   ell(560,226,90,16,SUN,' opacity="0.7"')+circ(520,214,10,SUN)+circ(600,218,8,SAGE)+
   text(720,200,'plok!',56,TD))
svg('lempar-jatuh',b)
def bubble(x,y,w,h,f): return rrect(x,y,w,h,30,f)+f'<path d="M{x+40} {y+h-2} L{x+30} {y+h+34} L{x+80} {y+h-2} Z" fill="{f}"/>'
b=(bubble(80,40,330,120,BLUSH)+text(245,122,'JANGAN!!',58,TD)+
   f'<path d="M110 60 L380 150 M380 60 L110 150" stroke="{TD}" stroke-width="10" stroke-linecap="round" opacity="0.55"/>'+
   arrow(450,120,560)+
   bubble(610,60,190,96,'#e3eee6')+text(705,124,'oke',52,SD)+
   circ(800,60,26,SD)+f'<path d="M789 60 L797 68 L811 52" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
svg('reaksi-tenang',b)
b=(plate(440,160,640)+
   ''.join(f'<rect x="{x}" y="{y}" width="120" height="26" rx="12" fill="{TERRA}" transform="rotate({r} {x+60} {y+13})"/>' for x,y,r in [(170,130,-8),(190,170,6),(210,108,-14)])+
   ''.join(f'<rect x="{x}" y="{y}" width="110" height="34" rx="16" fill="{TAPE}" transform="rotate({r} {x+55} {y+17})"/>' for x,y,r in [(390,120,10),(400,165,-6)])+
   circ(640,140,30,SD)+circ(670,120,26,SD)+circ(690,150,26,SD)+rrect(650,150,22,50,8,SAGE))
svg('jari-latihan',b)
b=(rrect(140,214,600,30,14,SKY)+''.join(rrect(160+i*80,214,40,30,4,'#d6e6f4') for i in range(7))+
   rrect(480,0,34,170,12,BOXD)+rrect(350,110,164,54,14,BOX)+rrect(300,84,130,20,10,BOXD)+rrect(360,90,16,30,6,BOXD)+
   f'<path d="M370 164 L330 216 M490 164 L530 216" stroke="{BOXD}" stroke-width="14" stroke-linecap="round"/>'+
   circ(250,200,10,SUN)+circ(620,204,9,SAGE)+text(780,120,'aman',40,SD))
svg('alas-kursi',b)
# ---- d16 lauk mpasi
def egg(cx,cy,s=1): return ell(cx,cy,48*s,62*s,CARD,f'stroke="{LINE}" stroke-width="5"')
b=(egg(150,130)+egg(260,140)+
   ell(420,170,70,24,CARD,f'stroke="{LINE}" stroke-width="5"')+circ(420,166,26,SUN)+
   arrow(520,140,620)+bowl(740,140,190,SKY)+steam(714,110)+circ(740,150,20,SUN,' opacity="0.8"'))
svg('lauk-telur',b)
def fish(cx,cy,col): return (ell(cx,cy,110,50,col)+f'<path d="M{cx+100} {cy} L{cx+160} {cy-44} L{cx+160} {cy+44} Z" fill="{col}"/>'+circ(cx-66,cy-12,9,INK))
b=(fish(220,130,SKY)+
   f'<path d="M150 130 L310 130 M190 110 L200 150 M230 108 L240 152 M270 110 L280 150" stroke="{CARD}" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'+
   arrow(440,130,540)+bowl(700,140,190,BLUSH)+steam(674,110)+ell(700,148,60,14,CARD))
svg('lauk-ikan',b)
b=(''.join(f'<path d="M{x} {y} q40 -46 80 -6 q30 30 -10 50 q-40 20 -70 -4 q-20 -16 0 -40 Z" fill="#9a4a3a"/>' for x,y in [(110,140),(200,170),(150,190)])+
   arrow(380,140,480)+rrect(560,110,220,110,24,'#c8c2b8')+rrect(540,98,260,24,12,MUTED)+rrect(800,140,40,16,8,MUTED)+steam(630,80))
svg('lauk-hati',b)
b=(''.join(circ(x,y,26,'#a8634a') for x,y in [(130,170),(190,180),(160,130),(220,140)])+
   f'<path d="M320 170 Q330 90 400 90 Q460 96 450 150 Q440 200 380 200 L350 214 Z" fill="#d9a874"/>'+rrect(330,196,30,40,12,CARD)+
   arrow(500,140,600)+bowl(740,140,190,SKY)+circ(720,148,16,'#a8634a')+circ(760,150,16,'#a8634a'))
svg('lauk-daging',b)
# ---- d17 main 5 menit
def duck(cx,cy,col=SUN): return ell(cx,cy+30,80,52,col)+circ(cx+50,cy-30,40,col)+f'<path d="M{cx+86} {cy-30} L{cx+122} {cy-20} L{cx+86} {cy-12} Z" fill="{TERRA}"/>'+circ(cx+60,cy-40,7,INK)
b=(duck(200,140)+f'<path d="M80 60 Q200 20 320 70 L340 250 Q200 230 70 250 Z" fill="{SAGE}" opacity="0.92"/>'+
   arrow(400,140,510)+duck(660,140)+text(780,70,'ba!',52,TD))
svg('cilukba-kain',b)
b=(rrect(330,110,220,120,20,SKY)+ell(440,110,110,22,'#d6e6f4')+
   f'<g transform="rotate(-30 200 120)">{rrect(130,108,140,22,11,BOXD)}{ell(110,119,34,22,BOX)}</g>'+
   f'<path d="M660 150 L720 150 L712 220 L668 220 Z" fill="{TERRA}"/><path d="M740 120 L800 120 L792 190 L748 190 Z" fill="{SUN}"/>'+
   f'<path d="M270 90 Q320 40 380 80 M380 80 L360 60 M380 80 L352 88" stroke="{SD}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   f'<path d="M520 80 Q590 40 640 110 M640 110 L614 102 M640 110 L640 84" stroke="{TD}" stroke-width="7" fill="none" stroke-linecap="round"/>')
svg('masuk-keluar',b)
b=(''.join(f'<path d="M{x} {y} q30 -24 60 0 q-10 30 -30 30 q-20 0 -30 -30 Z" fill="{CARD}" stroke="{LINE}" stroke-width="4" transform="rotate({r} {x+30} {y})"/>' for x,y,r in [(420,90,-20),(520,150,15),(620,80,30),(700,160,-10)])+
   ''.join(f'<path d="M{100} {y} Q{220} {y-30} {340} {y}" stroke="{SKY}" stroke-width="8" fill="none" stroke-linecap="round"/>' for y in [100,140,180])+
   rrect(60,230,760,14,7,BOX))
svg('tiup-tisu',b)
b=(f'<path d="M150 80 L150 170" stroke="{SAGE}" stroke-width="9" stroke-linecap="round"/>'+ell(134,172,22,16,SAGE)+
   f'<path d="M250 60 L250 150 M250 60 L300 70 L300 140" stroke="{TERRA}" stroke-width="9" fill="none" stroke-linecap="round"/>'+ell(234,152,22,16,TERRA)+ell(284,142,22,16,TERRA)+
   arrow(380,130,480)+
   ''.join(rrect(540+i*90,90,70,70,18,c)+text(575+i*90,140,n,40,CARD) for i,(c,n) in enumerate([(SKY,'1'),(SUN,'2'),(SD,'3')])))
svg('nyanyi-gerak',b)
b=(circ(130,80,34,TERRA)+circ(130,170,34,SKY)+
   f'<path d="M190 80 L300 80 M280 66 L300 80 L280 94" stroke="{MUTED}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   f'<path d="M190 170 L300 170 M280 156 L300 170 L280 184" stroke="{MUTED}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   circ(380,84,40,TERRA)+f'<path d="M380 44 Q392 24 410 22" stroke="{SD}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   f'<path d="M346 140 L414 140 L406 214 L354 214 Z" fill="{SKY}"/>'+
   circ(620,84,34,SUN)+circ(620,170,34,SAGE)+
   f'<path d="M680 84 L790 84 M770 70 L790 84 L770 98" stroke="{MUTED}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   f'<path d="M680 170 L790 170 M770 156 L790 170 L770 184" stroke="{MUTED}" stroke-width="7" fill="none" stroke-linecap="round"/>'+
   f'<path d="M820 60 Q850 90 830 120" stroke="{SUN}" stroke-width="22" fill="none" stroke-linecap="round"/>'+
   f'<path d="M810 150 L860 150 L860 200 L810 200 Z" fill="{SAGE}"/>'+
   f'<path d="M500 30 L500 230" stroke="{LINE}" stroke-width="5" stroke-dasharray="10 12"/>')
svg('cari-warna',b)
print('ok')
