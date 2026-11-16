// Set pieces and page art for "Pentol Mau Imunisasi" (episode 1). Flat cut paper, TemanTumbuh palette.
// No red cross anywhere (UU 1/2018): every clinic sign uses the leaf-heart.
import { cut } from './art.js';
import { sh, crescent, blob, rr, INK, cv, GRAIN } from './paper.js';
import { TAU, mulberry } from './lib.js';
import { BW, BD } from './book.js';
import { drawTunas, drawAdult, drawPerson, TU_W, TU_H, AD_W, AD_H } from './chars.js';
const LW = 9, LW2 = 5;
const TERRA = '#e07856', TERRA_S = '#bf5b3c', SAGE = '#7fb08f', SAGE_S = '#5d8f70', SKY = '#8fc4ea', SKY_S = '#6aa4d0', PINK = '#ef93a8', SUN = '#f3c45f', LEAF = '#6fbf5a', CREAM = '#fffaf0', WOOD = '#c79a6d', WOOD_S = '#a07a58';

export const heartPath = (x, cx, cy, r) => { x.beginPath(); x.moveTo(cx, cy + r * .9); x.bezierCurveTo(cx - r * 1.4, cy, cx - r * .9, cy - r * 1.05, cx, cy - r * .35); x.bezierCurveTo(cx + r * .9, cy - r * 1.05, cx + r * 1.4, cy, cx, cy + r * .9); x.closePath(); };
const leafHeart = (x, cx, cy, r) => { heartPath(x, cx, cy, r); sh(x, LEAF, 4); x.beginPath(); x.moveTo(cx, cy + r * .7); x.lineTo(cx, cy - r * .2); x.lineWidth = 4; x.strokeStyle = CREAM; x.stroke(); };
const txt = (x, s, X, Y, px, col = INK, w = 700) => { x.font = `${w} ${Math.round(px)}px Fredoka`; x.fillStyle = col; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(s, X, Y); };

// ---------- bedroom ----------
export function bed(wm) {
  return cut(wm, wm * .42, (x, W, H) => {
    rr(x, W * .02, H * .05, W * .14, H * .95, 12); sh(x, WOOD, LW);                       // headboard post
    const blanket = () => { x.beginPath(); x.moveTo(W * .1, H * .35); x.quadraticCurveTo(W * .55, H * .12, W * .98, H * .4); x.lineTo(W * .98, H * .78); x.lineTo(W * .1, H * .78); x.closePath(); };
    crescent(x, blanket, '#cf6f86', 0, 22, PINK); blanket(); sh(x, null, LW);
    for (let i = 0; i < 6; i++) { x.beginPath(); x.arc(W * (.2 + i * .13), H * (.5 + (i % 2) * .1), W * .018, 0, TAU); x.fillStyle = CREAM; x.fill(); }
    rr(x, W * .08, H * .76, W * .9, H * .12, 8); sh(x, WOOD, LW);
    rr(x, W * .1, H * .86, W * .05, H * .14, 4); sh(x, WOOD_S, LW2); rr(x, W * .9, H * .86, W * .05, H * .14, 4); sh(x, WOOD_S, LW2);
  });
}
export function breakfastTable(wm) {
  return cut(wm, wm * .5, (x, W, H) => {
    rr(x, 0, H * .36, W, H * .12, 10); sh(x, WOOD, LW);
    rr(x, W * .08, H * .46, W * .07, H * .54, 4); sh(x, WOOD_S, LW2); rr(x, W * .85, H * .46, W * .07, H * .54, 4); sh(x, WOOD_S, LW2);
    for (const px of [.3, .68]) { x.beginPath(); x.ellipse(W * px, H * .34, W * .13, H * .05, 0, 0, TAU); sh(x, CREAM, LW2); }
    x.beginPath(); x.ellipse(W * .3, H * .29, W * .06, H * .05, 0, 0, TAU); sh(x, SUN, LW2);              // egg
    rr(x, W * .62, H * .1, W * .1, H * .22, 6); sh(x, SKY, LW2);                                        // cup
  });
}
export function frame(wm, night = false) {
  return cut(wm, wm * .8, (x, W, H) => { rr(x, 0, 0, W, H, 8); sh(x, night ? '#5a648a' : CREAM, LW); leafHeart(x, W / 2, H / 2, W * .22); });
}
export function bedWindow(wm, night = false) {
  return cut(wm, wm * .85, (x, W, H) => {
    x.beginPath(); x.roundRect(0, 0, W, H, 14); x.fillStyle = night ? '#2c3452' : '#bfe0f2'; x.fill(); x.lineWidth = 9; x.strokeStyle = INK; x.stroke();
    if (night) { for (const [sx, sy, r] of [[.2, .2, 6], [.75, .3, 5], [.3, .7, 4], [.8, .75, 6]]) { x.beginPath(); x.arc(W * sx, H * sy, r, 0, TAU); x.fillStyle = SUN; x.fill(); }
      x.beginPath(); x.arc(W * .6, H * .45, W * .16, 0, TAU); x.fillStyle = SUN; x.fill(); x.beginPath(); x.arc(W * .66, H * .4, W * .15, 0, TAU); x.fillStyle = '#2c3452'; x.fill(); }
    x.beginPath(); x.moveTo(W / 2, 0); x.lineTo(W / 2, H); x.moveTo(0, H / 2); x.lineTo(W, H / 2); x.lineWidth = 8; x.strokeStyle = INK; x.stroke();
  }, { ay: 0 });
}
export function curtain(wm) {
  return cut(wm, wm * 1.3, (x, W, H) => {
    rr(x, 0, 0, W, H * .05, 4); sh(x, WOOD_S, LW2);
    const c = () => { x.beginPath(); x.moveTo(W * .05, H * .04); x.lineTo(W * .95, H * .04); x.quadraticCurveTo(W * .8, H * .5, W * .95, H); x.lineTo(W * .05, H); x.quadraticCurveTo(W * .2, H * .5, W * .05, H * .04); x.closePath(); };
    crescent(x, c, TERRA_S, 18, 0, TERRA); c(); sh(x, null, LW);
    for (const fx of [.3, .5, .7]) { x.beginPath(); x.moveTo(W * fx, H * .08); x.lineTo(W * fx, H * .95); x.lineWidth = 5; x.strokeStyle = TERRA_S; x.stroke(); }
  }, { ay: 0 });
}

// ---------- the journey ----------
export function mountain(wm, hm, col, seed) {
  return cut(wm, hm, (x, W, H) => {
    const m = () => { x.beginPath(); x.moveTo(0, H); x.lineTo(W * .48, H * .04); x.lineTo(W * .56, H * .1); x.lineTo(W, H); x.closePath(); };
    crescent(x, m, '#4f8a62', 0, 30, col); m(); sh(x, null, LW + 1);
    x.beginPath(); x.moveTo(W * .36, H * .28); x.lineTo(W * .48, H * .04); x.lineTo(W * .56, H * .1); x.lineTo(W * .64, H * .3); x.lineTo(W * .56, H * .24); x.lineTo(W * .5, H * .32); x.lineTo(W * .43, H * .24); x.closePath(); sh(x, CREAM, LW2);
  });
}
export function cow(hm) {
  return cut(hm * 1.6, hm, (x, W, H) => {
    for (const lx of [.2, .32, .62, .74]) { rr(x, W * lx, H * .55, W * .07, H * .45, 6); sh(x, '#efe6da', LW2); }
    blob(x, W * .47, H * .45, W * .32, H * .24, .03, 3); sh(x, '#fbf6ee', LW);
    blob(x, W * .38, H * .38, W * .09, H * .09, .1, 5); x.fillStyle = INK; x.fill(); blob(x, W * .6, H * .52, W * .07, H * .07, .1, 6); x.fillStyle = INK; x.fill();
    blob(x, W * .84, H * .3, W * .12, H * .17, .03, 7); sh(x, '#fbf6ee', LW);
    x.beginPath(); x.ellipse(W * .88, H * .4, W * .07, H * .06, 0, 0, TAU); sh(x, PINK, LW2);
    x.beginPath(); x.arc(W * .82, H * .25, W * .016, 0, TAU); x.fillStyle = INK; x.fill();
    x.beginPath(); x.moveTo(W * .78, H * .14); x.lineTo(W * .74, H * .04); x.moveTo(W * .9, H * .14); x.lineTo(W * .94, H * .04); x.lineWidth = 8; x.strokeStyle = INK; x.stroke();
  });
}
export function chicken(hm) {
  return cut(hm, hm, (x, W, H) => {
    x.beginPath(); x.moveTo(W * .4, H * .85); x.lineTo(W * .4, H); x.moveTo(W * .56, H * .85); x.lineTo(W * .56, H); x.lineWidth = 6; x.strokeStyle = '#e08a2c'; x.stroke();
    blob(x, W * .45, H * .62, W * .34, H * .26, .04, 2); sh(x, CREAM, LW);
    blob(x, W * .72, H * .32, W * .17, H * .17, .04, 3); sh(x, CREAM, LW);
    x.beginPath(); x.moveTo(W * .66, H * .17); x.quadraticCurveTo(W * .72, H * .02, W * .8, H * .16); x.closePath(); sh(x, '#e05656', LW2);
    x.beginPath(); x.moveTo(W * .88, H * .3); x.lineTo(W, H * .35); x.lineTo(W * .88, H * .4); x.closePath(); sh(x, SUN, 4);
    x.beginPath(); x.arc(W * .76, H * .28, W * .03, 0, TAU); x.fillStyle = INK; x.fill();
  });
}
export function warung(wm) {
  return cut(wm, wm * .8, (x, W, H) => {
    rr(x, W * .05, H * .3, W * .9, H * .7, 6); sh(x, CREAM, LW);
    x.beginPath(); x.moveTo(0, H * .34); x.lineTo(W * .08, H * .08); x.lineTo(W * .92, H * .08); x.lineTo(W, H * .34); x.closePath(); sh(x, SKY, LW);
    for (let i = 0; i < 5; i++) { x.beginPath(); x.moveTo(W * (.08 + i * .18), H * .08); x.lineTo(W * (.04 + i * .19), H * .34); x.lineWidth = 6; x.strokeStyle = CREAM; x.stroke(); }
    txt(x, 'WARUNG', W / 2, H * .5, H * .13, INK);
    rr(x, W * .12, H * .64, W * .76, H * .1, 6); sh(x, WOOD, LW2);
    for (let i = 0; i < 4; i++) { rr(x, W * (.16 + i * .18), H * .56, W * .1, H * .08, 4); sh(x, [SUN, PINK, LEAF, SKY][i], 4); }
  });
}
export function hospital(wm, hm) {
  return cut(wm, hm, (x, W, H) => {
    const wall = () => { x.beginPath(); x.rect(W * .04, H * .16, W * .92, H * .84); };
    crescent(x, wall, '#d9d3c7', 30, 0, CREAM); wall(); sh(x, null, LW);
    rr(x, 0, H * .1, W, H * .08, 10); sh(x, SAGE, LW);
    rr(x, W * .16, 0, W * .68, H * .12, 14); sh(x, SAGE_S, LW2 + 1);
    leafHeart(x, W * .24, H * .06, H * .035);
    txt(x, 'RUMAH SAKIT', W * .55, H * .062, H * .07, CREAM);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) { if (r === 2 && (c === 1 || c === 2)) continue; rr(x, W * (.1 + c * .21), H * (.26 + r * .2), W * .14, H * .12, 8); sh(x, '#d9e7f5', LW2); }
    rr(x, W * .34, H * .7, W * .32, H * .3, 6); sh(x, '#cfe3f2', LW); x.beginPath(); x.moveTo(W * .5, H * .7); x.lineTo(W * .5, H); x.lineWidth = 6; x.strokeStyle = INK; x.stroke();
  });
}
// the family car: a side-on cut-out with three heads in the window
export function car(wm) {
  return cut(wm, wm * .55, (x, W, H) => {
    const cab = () => { x.beginPath(); x.moveTo(W * .2, H * .45); x.quadraticCurveTo(W * .24, H * .06, W * .42, H * .06); x.lineTo(W * .68, H * .06); x.quadraticCurveTo(W * .84, H * .06, W * .88, H * .45); x.closePath(); };
    cab(); sh(x, '#d9e7f5', LW);
    // heads: Papa, Mama (hijab), Pentol (sprout)
    x.beginPath(); x.arc(W * .34, H * .3, H * .1, 0, TAU); sh(x, '#f3c9a2', LW2); x.beginPath(); x.arc(W * .34, H * .26, H * .1, Math.PI, TAU); sh(x, '#3b2f2a', LW2);
    x.beginPath(); x.arc(W * .53, H * .29, H * .13, 0, TAU); sh(x, TERRA, LW2); x.beginPath(); x.arc(W * .53, H * .31, H * .08, 0, TAU); sh(x, '#f3c9a2', 4);
    x.beginPath(); x.arc(W * .72, H * .34, H * .08, 0, TAU); sh(x, '#f6c9a5', LW2);
    for (const sx of [-1, 1]) { x.beginPath(); x.ellipse(W * .72 + sx * H * .07, H * .2, H * .06, H * .03, sx * .5, 0, TAU); sh(x, LEAF, 3); }
    const body = () => { rr(x, W * .02, H * .42, W * .96, H * .36, H * .14); };
    crescent(x, body, SAGE_S, 0, 22, SAGE); body(); sh(x, null, LW + 1);
    x.beginPath(); x.arc(W * .94, H * .55, H * .05, 0, TAU); sh(x, SUN, 4);
    for (const wx of [.24, .78]) { x.beginPath(); x.arc(W * wx, H * .8, H * .17, 0, TAU); sh(x, '#3a2a24', LW); x.beginPath(); x.arc(W * wx, H * .8, H * .07, 0, TAU); sh(x, '#9aa8b6', 4); }
  }, { ay: .98 });
}

// ---------- waiting room ----------
export function chairs(wm) {
  return cut(wm, wm * .3, (x, W, H) => {
    for (let i = 0; i < 3; i++) { const cx = W * (.03 + i * .33); rr(x, cx, 0, W * .28, H * .55, 14); sh(x, SKY, LW); rr(x, cx, H * .52, W * .28, H * .16, 8); sh(x, SKY_S, LW); rr(x, cx + W * .03, H * .66, W * .03, H * .34, 3); sh(x, INK, 0); x.fillStyle = INK; x.fill(); rr(x, cx + W * .22, H * .66, W * .03, H * .34, 3); x.fillStyle = INK; x.fill(); }
  });
}
export function deskCounter(wm) {
  return cut(wm, wm * .3, (x, W, H) => {
    rr(x, 0, 0, W, H * .16, 10); sh(x, SAGE, LW);
    rr(x, W * .03, H * .14, W * .94, H * .86, 8); sh(x, '#e3eee6', LW);
    leafHeart(x, W * .18, H * .55, H * .14); txt(x, 'Pendaftaran', W * .58, H * .56, H * .17);
  });
}
export function display(wm, num) {
  return cut(wm, wm * .6, (x, W, H) => { rr(x, 0, 0, W, H, 12); sh(x, '#2c3452', LW); txt(x, 'Antrian', W / 2, H * .26, H * .18, '#c8ccde', 700); txt(x, num, W / 2, H * .64, H * .42, SUN); }, { ay: 0 });
}
export function poster(wm, lines, icon) {
  return cut(wm, wm * 1.25, (x, W, H) => {
    rr(x, 0, 0, W, H, 10); sh(x, CREAM, LW);
    lines.forEach((l, i) => txt(x, l, W / 2, H * (.2 + i * .16), H * .12));
    if (icon === 'hands') for (const yy of [.66, .8]) { x.beginPath(); x.moveTo(W * .25, H * yy); x.quadraticCurveTo(W * .5, H * (yy - .1), W * .75, H * yy); x.lineWidth = 14; x.strokeStyle = SKY; x.lineCap = 'round'; x.stroke(); }
  }, { ay: 0 });
}
export function clock(wm) { return cut(wm, wm, (x, W, H) => { x.beginPath(); x.arc(W / 2, H / 2, W * .46, 0, TAU); sh(x, CREAM, LW); x.beginPath(); x.moveTo(W / 2, H / 2); x.lineTo(W / 2, H * .18); x.moveTo(W / 2, H / 2); x.lineTo(W * .74, H * .6); x.lineWidth = 9; x.strokeStyle = INK; x.stroke(); }, { ay: 0 }); }
export function signBoard(wm, text) {
  return cut(wm, wm * .3, (x, W, H) => { rr(x, 0, 0, W, H, 16); sh(x, SAGE, LW); leafHeart(x, H * .55, H / 2, H * .24); txt(x, text, W * .58, H * .54, H * .42, CREAM); }, { ay: 0 });
}
export function shadowBird(wm, up) {
  return cut(wm, wm * .5, (x, W, H) => {
    x.fillStyle = 'rgba(58,42,36,.38)';
    x.beginPath(); if (up) { x.moveTo(W * .48, H * .55); x.quadraticCurveTo(W * .25, H * .05, W * .02, H * .2); x.quadraticCurveTo(W * .25, H * .4, W * .42, H * .7); } else { x.moveTo(W * .48, H * .55); x.quadraticCurveTo(W * .25, H * .9, W * .02, H * .9); x.quadraticCurveTo(W * .25, H * .66, W * .42, H * .55); } x.fill();
    x.beginPath(); if (up) { x.moveTo(W * .52, H * .55); x.quadraticCurveTo(W * .75, H * .05, W * .98, H * .2); x.quadraticCurveTo(W * .75, H * .4, W * .58, H * .7); } else { x.moveTo(W * .52, H * .55); x.quadraticCurveTo(W * .75, H * .9, W * .98, H * .9); x.quadraticCurveTo(W * .75, H * .66, W * .58, H * .55); } x.fill();
    x.beginPath(); x.ellipse(W * .5, H * .6, W * .12, H * .14, 0, 0, TAU); x.fill(); x.beginPath(); x.arc(W * .62, H * .48, H * .1, 0, TAU); x.fill();
  }, { ay: 0, border: 0, grain: false });
}

// ---------- doctor's room ----------
export function heightChart(hm) {
  return cut(hm * .18, hm, (x, W, H) => { rr(x, 0, 0, W, H, 6); sh(x, '#fbebc2', LW); for (let i = 1; i < 14; i++) { x.beginPath(); x.moveTo(0, H * i / 14); x.lineTo(W * (i % 2 ? .4 : .6), H * i / 14); x.lineWidth = 5; x.strokeStyle = INK; x.stroke(); } }, { ay: 0 });
}
export function examBed(wm) {
  return cut(wm, wm * .42, (x, W, H) => {
    rr(x, W * .02, H * .3, W * .96, H * .24, 12); sh(x, SKY, LW); rr(x, W * .06, H * .22, W * .6, H * .12, 6); sh(x, CREAM, LW2);
    x.beginPath(); x.moveTo(W * .7, H * .3); x.quadraticCurveTo(W * .84, H * .02, W * .98, H * .3); sh(x, SKY, LW);
    for (const lx of [.1, .86]) { rr(x, W * lx, H * .52, W * .04, H * .48, 4); sh(x, '#9aa8b6', LW2); }
  });
}
export function bubble(wm, text) { return cut(wm, wm * .38, (x, W, H) => { rr(x, 0, 0, W, H, H / 2); sh(x, CREAM, LW); txt(x, text, W / 2, H * .54, H * .48, TERRA_S); }, { ay: .5 }); }
export function sticker(wm) { return cut(wm, wm, (x, W, H) => { x.beginPath(); x.arc(W / 2, H / 2, W * .46, 0, TAU); sh(x, CREAM, LW); leafHeart(x, W / 2, H / 2, W * .26); }, { ay: .5 }); }

// ---------- inside the body ----------
export function penjaga(hm, brave = false) {
  return cut(hm, hm * 1.1, (x, W, H) => {
    x.beginPath(); x.ellipse(W * .36, H * .12, W * .16, W * .07, -.5, 0, TAU); sh(x, LEAF, LW2);
    x.beginPath(); x.arc(W * .46, H * .56, W * .4, 0, TAU); sh(x, CREAM, LW + 2); x.lineWidth = 12; x.strokeStyle = SAGE_S; x.stroke();
    for (const sx of [-1, 1]) { x.beginPath(); x.arc(W * .46 + sx * W * .13, H * .5, W * .045, 0, TAU); x.fillStyle = INK; x.fill(); }
    if (brave) { x.beginPath(); x.moveTo(W * .26, H * .38); x.lineTo(W * .38, H * .42); x.moveTo(W * .66, H * .38); x.lineTo(W * .54, H * .42); x.lineWidth = 8; x.strokeStyle = INK; x.stroke(); }
    x.beginPath(); x.moveTo(W * .36, H * .66); x.quadraticCurveTo(W * .46, H * .76, W * .56, H * .66); x.lineWidth = 8; x.strokeStyle = INK; x.lineCap = 'round'; x.stroke();
    x.beginPath(); x.ellipse(W * .86, H * .66, W * .12, H * .2, 0, 0, TAU); sh(x, SAGE, LW2);
  });
}
export function sleepyGerm(wm) {
  return cut(wm, wm, (x, W, H) => {
    const R = W * .4, pts = () => { x.beginPath(); for (let i = 0; i <= 14; i++) { const a = i / 14 * TAU, r = R * (i % 2 ? .8 : 1.05); x.lineTo(W / 2 + Math.cos(a) * r, H / 2 + Math.sin(a) * r); } x.closePath(); };
    crescent(x, pts, '#a796d6', 10, 10, '#d4c9ef'); pts(); sh(x, null, LW);
    for (const sx of [-1, 1]) { x.beginPath(); x.moveTo(W / 2 + sx * R * .45, H / 2); x.quadraticCurveTo(W / 2 + sx * R * .32, H / 2 + R * .12, W / 2 + sx * R * .19, H / 2); x.lineWidth = 6; x.strokeStyle = INK; x.stroke(); }
    txt(x, 'z', W * .86, H * .14, H * .26, '#5e4a96');
  }, { ay: .5, border: 12 });
}
export function posterIngat(wm, germCanvas) {
  return cut(wm, wm * .95, (x, W, H) => { rr(x, 0, 0, W, H, 10); sh(x, CREAM, LW); txt(x, 'INGAT!', W / 2, H * .18, H * .17, TERRA_S); x.drawImage(germCanvas, W * .25, H * .32, W * .5, W * .5); x.beginPath(); x.arc(W / 2, H * .03, W * .04, 0, TAU); sh(x, TERRA, 4); });
}
export function textCard(wm, text) { return cut(wm, wm * .34, (x, W, H) => { rr(x, 0, 0, W, H, 14); sh(x, CREAM, LW); txt(x, text, W / 2, H * .55, H * .44, INK, 600); }); }

// ---------- recap memory cards ----------
export function memoryCard(wm, i) {
  return cut(wm, wm * 1.15, (x, W, H) => {
    rr(x, 0, 0, W, H, 16); sh(x, CREAM, LW + 2); rr(x, W * .07, H * .07, W * .86, H * .86, 10); x.fillStyle = '#f7efe0'; x.fill();
    x.save(); x.beginPath(); x.rect(W * .07, H * .07, W * .86, H * .86); x.clip();
    const T = cv(TU_W, TU_H), A2 = cv(AD_W, AD_H);
    if (i === 1) { drawTunas(T.getContext('2d'), { expr: 'lega', plaster: 1 }); x.drawImage(T, W * .14, H * .2, W * .72, W * .72 * TU_H / TU_W); }
    if (i === 2) { drawAdult(A2.getContext('2d'), { hug: 1 }, 'mama'); x.drawImage(A2, W * .02, H * .1, W * .5, W * .5 * AD_H / AD_W);
      drawTunas(T.getContext('2d'), { expr: 'lega' }); x.drawImage(T, W * .12, H * .5, W * .32, W * .32 * TU_H / TU_W);
      const P = cv(AD_W, AD_H); drawPerson(P.getContext('2d'), { armL: .6 }, 'papa'); x.drawImage(P, W * .48, H * .1, W * .5, W * .5 * AD_H / AD_W); }
    if (i === 3) { rr(x, W * .3, H * .14, W * .4, H * .32, 6); sh(x, CREAM, 5); txt(x, 'INGAT!', W / 2, H * .22, H * .06, TERRA_S);
      const g = sleepyGerm(.02); x.drawImage(g.c, W * .4, H * .26, W * .2, W * .2);
      const p1 = penjaga(.02, true); x.drawImage(p1.c, W * .14, H * .52, W * .32, W * .36); x.drawImage(p1.c, W * .54, H * .52, W * .32, W * .36); }
    x.restore();
    x.beginPath(); x.arc(W * .14, H * .12, W * .1, 0, TAU); sh(x, TERRA, LW); txt(x, String(i), W * .14, H * .125, W * .13, CREAM);
  });
}

// ---------- page art: back wall (sky) and floor (ground) for every set ----------
const PW = 2048, PH = Math.round(2048 * BD / BW);
export const gx = xm => (xm / BW + .5) * PW, gz = zm => zm / BD * PH;
function page(fn) { const c = cv(PW, PH), x = c.getContext('2d'); fn(x); x.save(); x.globalAlpha = .7; x.fillStyle = x.createPattern(GRAIN, 'repeat'); x.fillRect(0, 0, PW, PH); x.restore(); return c; }
function grad(x, stops) { const g = x.createLinearGradient(0, 0, 0, PH); stops.forEach(([o, c]) => g.addColorStop(o, c)); x.fillStyle = g; x.fillRect(0, 0, PW, PH); }
const stripes = (x, col, n = 9) => { x.fillStyle = col; for (let i = 0; i < n; i++) x.fillRect(i * PW / n, 0, PW / (2 * n), PH); };
const planks = (x, col) => { x.strokeStyle = col; x.lineWidth = 6; for (let i = 0; i < 12; i++) { x.beginPath(); x.moveTo(0, i * PH / 12); x.lineTo(PW, i * PH / 12); x.stroke(); } };
const tiles = (x, col) => { x.strokeStyle = col; x.lineWidth = 5; for (let i = 0; i <= 16; i++) { x.beginPath(); x.moveTo(i * PW / 16, 0); x.lineTo(i * PW / 16, PH); x.stroke(); } for (let j = 0; j <= 10; j++) { x.beginPath(); x.moveTo(0, j * PH / 10); x.lineTo(PW, j * PH / 10); x.stroke(); } };

export function pages() {
  const R = mulberry(7), P = {};
  P.bedSky = page(x => { grad(x, [[0, '#e3f0e6'], [1, '#d3e7da']]); stripes(x, 'rgba(255,255,255,.35)'); x.fillStyle = '#c5dccd'; x.fillRect(0, PH * .86, PW, PH * .14); });
  P.bedGround = page(x => { grad(x, [[0, '#ecd5a8'], [1, '#f1ddb4']]); planks(x, 'rgba(150,110,60,.18)'); x.fillStyle = '#f2b8c3'; x.beginPath(); x.ellipse(gx(-.08), gz(.18), 520, 170, 0, 0, TAU); x.fill(); x.setLineDash([26, 18]); x.strokeStyle = '#cf6f86'; x.lineWidth = 10; x.stroke(); x.setLineDash([]); });
  P.nightSky = page(x => { grad(x, [[0, '#3a4468'], [1, '#2c3452']]); stripes(x, 'rgba(255,255,255,.05)'); x.fillStyle = '#262d47'; x.fillRect(0, PH * .86, PW, PH * .14); });
  P.nightGround = page(x => { grad(x, [[0, '#8f7a63'], [1, '#9c8770']]); planks(x, 'rgba(40,30,20,.18)'); x.fillStyle = '#a77b86'; x.beginPath(); x.ellipse(gx(-.08), gz(.18), 520, 170, 0, 0, TAU); x.fill(); });
  P.roadSky = page(x => { grad(x, [[0, '#8fc9ec'], [.7, '#d2edf7'], [1, '#eef7e6']]); for (let i = 0; i < 6; i++) { const cx = R() * PW, cy = PH * (.1 + R() * .3); x.fillStyle = 'rgba(255,255,255,.65)'; for (let k = 0; k < 4; k++) { x.beginPath(); x.arc(cx + k * 60, cy + (k % 2) * 20, 70, 0, TAU); x.fill(); } } });
  P.roadGround = page(x => {
    grad(x, [[0, '#8cc86a'], [1, '#a3d77f']]);
    x.fillStyle = '#b9b0a6'; x.fillRect(0, gz(.2) - 120, PW, 240); x.fillStyle = '#fffaf0'; for (let i = 0; i < 16; i++) x.fillRect(i * PW / 16 + 20, gz(.2) - 10, 70, 20);
    for (let i = 0; i < 160; i++) { const yy = R() * PH; if (Math.abs(yy - gz(.2)) < 140) continue; x.beginPath(); x.arc(R() * PW, yy, 5 + R() * 6, 0, TAU); x.fillStyle = ['#ffffff', '#ffe066', '#ff9ec1'][(R() * 3) | 0]; x.fill(); }
  });
  P.waitSky = page(x => { grad(x, [[0, '#e3eee6'], [1, '#d5e6db']]); x.fillStyle = '#c5dccd'; x.fillRect(0, PH * .8, PW, PH * .2); });
  P.waitGround = page(x => { grad(x, [[0, '#f1ece2'], [1, '#e9e2d4']]); tiles(x, 'rgba(120,110,95,.18)'); });
  P.docSky = page(x => { grad(x, [[0, '#fffaf0'], [1, '#f5efe2']]); x.fillStyle = '#d9e7f5'; x.fillRect(0, PH * .72, PW, PH * .28); x.fillStyle = '#b9cfe4'; x.fillRect(0, PH * .72, PW, 12); });
  P.docGround = page(x => { grad(x, [[0, '#e8f0f6'], [1, '#dde8f1']]); tiles(x, 'rgba(90,110,130,.16)'); });
  P.bodySky = page(x => { grad(x, [[0, '#fbe3d6'], [1, '#f8d6c6']]); for (let i = 0; i < 40; i++) { x.beginPath(); x.arc(R() * PW, R() * PH, 30 + R() * 110, 0, TAU); x.fillStyle = `rgba(239,182,163,${.25 + R() * .35})`; x.fill(); } x.strokeStyle = 'rgba(232,160,140,.5)'; x.lineWidth = 50; x.lineCap = 'round'; x.beginPath(); x.moveTo(0, PH * .3); x.bezierCurveTo(PW * .3, PH * .1, PW * .6, PH * .5, PW, PH * .25); x.stroke(); });
  P.bodyGround = page(x => { grad(x, [[0, '#f6cdbd'], [1, '#f3c2b0']]); for (let i = 0; i < 30; i++) { x.beginPath(); x.arc(R() * PW, R() * PH, 25 + R() * 80, 0, TAU); x.fillStyle = `rgba(239,182,163,${.3 + R() * .3})`; x.fill(); } });
  P.recapSky = page(x => { grad(x, [[0, '#fbebc2'], [1, '#f7e2ad']]); x.font = '700 230px Fredoka'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineWidth = 18; x.strokeStyle = '#fffaf0'; x.strokeText('INGAT YA!', PW / 2, PH * .17); x.fillStyle = '#c46040'; x.fillText('INGAT YA!', PW / 2, PH * .17); for (let i = 0; i < 14; i++) { x.beginPath(); x.arc(R() * PW, PH * (.05 + R() * .3), 8, 0, TAU); x.fillStyle = '#f3c45f'; x.fill(); } });
  P.recapGround = page(x => { grad(x, [[0, '#f4e3c2'], [1, '#f1ddb4']]); planks(x, 'rgba(150,110,60,.14)'); });
  return P;
}
