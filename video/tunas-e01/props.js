// Set pieces for Tunas Imunisasi (all flat cut paper; no red cross anywhere, UU 1/2018)
import { cut, PPM } from './art.js';
import { sh, crescent, blob, rr, INK, cv, paperFill, GRAIN } from './paper.js';
import { TAU, mulberry } from './lib.js';
import { BW, BD } from './book.js';
const LW = 9, LW2 = 5;

const heartPath = (x, cx, cy, r) => { x.beginPath(); x.moveTo(cx, cy + r * .9); x.bezierCurveTo(cx - r * 1.4, cy, cx - r * .9, cy - r * 1.05, cx, cy - r * .35); x.bezierCurveTo(cx + r * .9, cy - r * 1.05, cx + r * 1.4, cy, cx, cy + r * .9); x.closePath(); };

export function rumah(hm) {
  return cut(hm * 1.05, hm, (x, W, H) => {
    const wall = () => { x.beginPath(); x.rect(W * .12, H * .42, W * .76, H * .58); };
    crescent(x, wall, '#e9d3a6', 26, 0, '#fbe8c1'); wall(); sh(x, null, LW);
    const roof = () => { x.beginPath(); x.moveTo(W * .02, H * .46); x.lineTo(W * .5, H * .02); x.lineTo(W * .98, H * .46); x.closePath(); };
    crescent(x, roof, '#bf5b3c', 0, 24, '#e07856'); roof(); sh(x, null, LW + 1);
    rr(x, W * .42, H * .64, W * .18, H * .36, 10); sh(x, '#7fb08f', LW2 + 1);
    rr(x, W * .18, H * .56, W * .16, W * .16, 8); sh(x, '#bfe0f2', LW2); rr(x, W * .66, H * .56, W * .16, W * .16, 8); sh(x, '#bfe0f2', LW2);
  });
}
export function puskesmas(wm, hm) {
  return cut(wm, hm, (x, W, H) => {
    const wall = () => { x.beginPath(); x.rect(W * .04, H * .3, W * .92, H * .7); };
    crescent(x, wall, '#e6c891', 30, 0, '#f6dfae'); wall(); sh(x, null, LW);
    const roof = () => { x.beginPath(); x.moveTo(0, H * .34); x.lineTo(W * .1, H * .14); x.lineTo(W * .9, H * .14); x.lineTo(W, H * .34); x.closePath(); };
    crescent(x, roof, '#bf5b3c', 0, 22, '#e07856'); roof(); sh(x, null, LW + 1);
    // sign board with a leaf-heart (never a red cross)
    rr(x, W * .2, H * .02, W * .6, H * .13, 14); sh(x, '#6fa064', LW2 + 1);
    heartPath(x, W * .27, H * .085, H * .04); sh(x, '#fffaf0', 4);
    x.font = `700 ${Math.round(H * .085)}px Fredoka`; x.fillStyle = '#fffaf0'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('PUSKESMAS', W * .54, H * .088);
    // windows + door opening
    for (const u of [.1, .72]) { rr(x, W * u, H * .46, W * .18, H * .2, 8); sh(x, '#8fc4ea', LW2); x.beginPath(); x.moveTo(W * (u + .09), H * .46); x.lineTo(W * (u + .09), H * .66); x.lineWidth = 5; x.strokeStyle = INK; x.stroke(); }
    rr(x, W * .39, H * .52, W * .22, H * .48, 10); sh(x, '#5d8f70', LW2 + 1);
    x.beginPath(); x.arc(W * .57, H * .78, 9, 0, TAU); x.fillStyle = '#f3c45f'; x.fill();
  });
}
export function stool(wm) {
  return cut(wm, wm * .7, (x, W, H) => {
    rr(x, 0, 0, W, H * .2, 10); sh(x, '#b9824f', LW);
    for (const u of [.1, .8]) { rr(x, W * u, H * .18, W * .1, H * .82, 6); sh(x, '#8a5a3c', LW2); }
  });
}
export function poster(wm) {
  return cut(wm, wm * 1.2, (x, W, H) => {
    rr(x, 0, 0, W, H, 12); sh(x, '#fffaf2', LW2 + 1);
    heartPath(x, W / 2, H * .45, W * .28); sh(x, '#ee8ea4', LW2 + 1);
    for (const v of [.78, .86]) { x.beginPath(); x.moveTo(W * .2, H * v); x.lineTo(W * .8, H * v); x.lineWidth = 6; x.strokeStyle = '#c9b9a4'; x.stroke(); }
  }, { ay: 0 });
}
export function shield(hm) {
  return cut(hm * .86, hm, (x, W, H) => {
    const p = () => { x.beginPath(); x.moveTo(W / 2, H * .02); x.quadraticCurveTo(W * .78, H * .1, W * .98, H * .1); x.bezierCurveTo(W * .98, H * .55, W * .8, H * .82, W / 2, H * .98); x.bezierCurveTo(W * .2, H * .82, W * .02, H * .55, W * .02, H * .1); x.quadraticCurveTo(W * .22, H * .1, W / 2, H * .02); x.closePath(); };
    crescent(x, p, '#6aa4d0', 30, 30, '#9fd0f2'); p(); sh(x, null, LW + 2);
    heartPath(x, W / 2, H * .48, W * .2); sh(x, '#fffaf0', LW2 + 1);
  });
}
export function heart(wm, col = '#ee8ea4') { return cut(wm, wm, (x, W, H) => { heartPath(x, W / 2, H * .52, W * .32); sh(x, col, LW); }, { ay: .5 }); }
export function worry(wm) {
  return cut(wm, wm * .7, (x, W, H) => {
    blob(x, W / 2, H / 2, W * .46, H * .42, .08, 6); sh(x, '#eaf3fb', LW2 + 1);
    x.beginPath(); const R = mulberry(5); for (let i = 0; i < 18; i++) { const a = i * 1.1; x.lineTo(W / 2 + Math.cos(a) * W * (.1 + R() * .2), H / 2 + Math.sin(a) * H * (.1 + R() * .2)); } x.lineWidth = 9; x.strokeStyle = '#6aa4d0'; x.lineJoin = 'round'; x.stroke();
  }, { ay: .5 });
}
export function burst(wm) {
  return cut(wm, wm, (x, W, H) => { x.beginPath(); for (let i = 0; i < 16; i++) { const a = i / 16 * TAU, r = i % 2 ? W * .2 : W * .47; x.lineTo(W / 2 + Math.cos(a) * r, H / 2 + Math.sin(a) * r); } x.closePath(); sh(x, '#ffd84a', LW); }, { ay: .5 });
}

// ---------- page art ----------
const PW = 2048, PH = Math.round(2048 * BD / BW);
export const gx = xm => (xm / BW + .5) * PW, gz = zm => zm / BD * PH;
function page(fn) { const c = cv(PW, PH), x = c.getContext('2d'); fn(x); x.save(); x.globalAlpha = .7; x.fillStyle = x.createPattern(GRAIN, 'repeat'); x.fillRect(0, 0, PW, PH); x.restore(); return c; }
function grad(x, stops) { const g = x.createLinearGradient(0, 0, 0, PH); stops.forEach(([o, c]) => g.addColorStop(o, c)); x.fillStyle = g; x.fillRect(0, 0, PW, PH); }
export function pages() {
  const R = mulberry(3), P = {};
  P.sky0 = page(x => { grad(x, [[0, '#8fc9ec'], [.7, '#d2edf7'], [1, '#eef7e6']]); for (let i = 0; i < 6; i++) { const cx = R() * PW, cy = PH * (.1 + R() * .35), w = 200 + R() * 220; x.fillStyle = 'rgba(255,255,255,.6)'; for (let k = 0; k < 5; k++) { x.beginPath(); x.ellipse(cx + (k - 2) * w * .22, cy - Math.sin(k / 4 * Math.PI) * w * .12, w * .2, w * .13, 0, 0, TAU); x.fill(); } } });
  P.ground0 = page(x => {
    grad(x, [[0, '#8cc86a'], [1, '#a3d77f']]);
    x.lineCap = 'round'; x.lineJoin = 'round';
    const path = [[gx(-.24), gz(.17)], [gx(-.1), gz(.16)], [gx(.04), gz(.17)], [gx(.13), gz(.15)], [gx(.13), gz(.1)]];
    for (const [w, c] of [[170, '#d6b877'], [150, '#ecd49a']]) { x.beginPath(); x.moveTo(...path[0]); for (const p of path.slice(1)) x.lineTo(...p); x.lineWidth = w; x.strokeStyle = c; x.stroke(); }
    for (let i = 0; i < 150; i++) { x.beginPath(); x.arc(R() * PW, R() * PH, 5 + R() * 6, 0, TAU); x.fillStyle = ['#ffffff', '#ffe066', '#ff9ec1'][(R() * 3) | 0]; x.fill(); }
  });
  P.sky1 = page(x => {
    grad(x, [[0, '#e3f0e6'], [1, '#d3e7da']]);
    x.fillStyle = 'rgba(255,255,255,.35)'; for (let i = 0; i < 9; i++) x.fillRect(i * PW / 9, 0, PW / 18, PH);
    x.fillStyle = '#c5dccd'; x.fillRect(0, PH * .82, PW, PH * .18);
  });
  P.ground1 = page(x => {
    grad(x, [[0, '#ecd5a8'], [1, '#f1ddb4']]);
    x.strokeStyle = 'rgba(150,110,60,.18)'; x.lineWidth = 6; for (let i = 0; i < 12; i++) { x.beginPath(); x.moveTo(0, i * PH / 12); x.lineTo(PW, i * PH / 12); x.stroke(); }
    x.fillStyle = '#e8a3b2'; x.beginPath(); x.ellipse(gx(.0), gz(.18), 420, 150, 0, 0, TAU); x.fill(); x.strokeStyle = '#cf6f86'; x.lineWidth = 10; x.stroke();
  });
  return P;
}
export { PPM };
