// TemanTumbuh characters as cut paper: Tunas (our mascot), Mama, the bidan, a germ. Posable, redrawn per quantised pose.
import * as THREE from 'three';
import { cv, finishCut, sh, blob, crescent, rr, INK } from './paper.js';
import { cut } from './art.js';
import { texOf } from './book.js';
import { blobShadow } from './cutmesh.js';
import { TAU } from './lib.js';

const LW = 10, LW2 = 6;
const PEACH = '#f6c9a5', PEACH_S = '#e8a983', TERRA = '#e07856', TERRA_S = '#bf5b3c', LEAF = '#6fbf5a', LEAF_S = '#4b9a3f';
const SAGE = '#7fb08f', SAGE_S = '#5d8f70', SKIN = '#f3c9a2', SKIN_S = '#dda67f', PINK = '#ef93a8', PINK_S = '#cf6f86', SKY = '#8fc4ea', SKY_S = '#6aa4d0';

function plane(c, h, ax, ay) {
  const t = texOf(c), w = h * c.width / c.height;
  const g = new THREE.PlaneGeometry(w, h); g.translate(w / 2 - ax * w, ay * h - h / 2, 0);
  const m = new THREE.MeshStandardMaterial({ map: t, alphaTest: .5, alphaToCoverage: true, roughness: .85, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(g, m); mesh.receiveShadow = true; mesh.castShadow = true;
  mesh.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: t, alphaTest: .5, side: THREE.DoubleSide });
  return { mesh, t };
}
function actor(W, H, h, drawFn, footY) {
  const c = cv(W, H); drawFn(c.getContext('2d'), {});
  const P = plane(c, h, .5, footY / H);
  const root = new THREE.Group(), body = new THREE.Group(); body.add(P.mesh); root.add(body);
  const shadow = blobShadow(h * .3, .45);
  let key = '';
  return {
    root, body, shadow, h,
    pose(p) { const k = JSON.stringify(p, (kk, v) => typeof v === 'number' ? Math.round(v * 30) / 30 : v); if (k === key) return; key = k; drawFn(c.getContext('2d'), p); P.t.needsUpdate = true; },
    head(v = new THREE.Vector3()) { return v.set(0, h * .95, 0).applyMatrix4(body.matrixWorld); },
  };
}
const line = (a, pts, w, col = INK) => { a.beginPath(); a.moveTo(...pts[0]); for (const p of pts.slice(1)) a.lineTo(...p); a.lineWidth = w; a.strokeStyle = col; a.lineCap = 'round'; a.lineJoin = 'round'; a.stroke(); };

// ———————— Tunas ————————
// pose: walk, stride (0/1), armL, armR (rad, + = outward-up), expr senang|cemas|meringis|lega, blink, plaster (0-1), tear (0-1), hold (left hand forward)
export const TU_W = 760, TU_H = 960;
export function drawTunas(x, p = {}) {
  const { walk = 0, stride = 0, armL = .35, armR = .35, expr = 'senang', blink = 0, plaster = 0, tear = 0 } = p;
  x.clearRect(0, 0, TU_W, TU_H);
  const C = cv(TU_W, TU_H), a = C.getContext('2d'), cx = 380, by = 880;
  const s = Math.sin(walk) * stride, bob = -Math.abs(Math.sin(walk)) * stride * 14;
  // feet
  for (const [fx, lift] of [[300, Math.max(0, s) * 22], [460, Math.max(0, -s) * 22]]) { blob(a, fx, by - 30 - lift, 62, 34, .04, fx); sh(a, TERRA, LW2 + 1); }
  a.save(); a.translate(0, bob);
  // arms (behind the body)
  const arm = (sx, ang, side) => { a.save(); a.translate(sx, 560); a.rotate(-ang * side); rr(a, -22, -10, 44, 150, 22); sh(a, PEACH, LW2 + 1); a.restore(); };
  arm(170, armL, -1); arm(590, armR, 1);
  // stem + leaves + seed
  line(a, [[cx, 300], [cx + 4, 240], [cx, 190]], 26); line(a, [[cx, 300], [cx + 4, 240], [cx, 190]], 14, LEAF_S);
  const leafL = () => { a.beginPath(); a.moveTo(cx, 196); a.bezierCurveTo(cx - 40, 110, cx - 150, 96, cx - 210, 150); a.bezierCurveTo(cx - 150, 200, cx - 70, 214, cx, 196); a.closePath(); };
  const leafR = () => { a.beginPath(); a.moveTo(cx, 196); a.bezierCurveTo(cx + 40, 110, cx + 150, 96, cx + 210, 150); a.bezierCurveTo(cx + 150, 200, cx + 70, 214, cx, 196); a.closePath(); };
  crescent(a, leafL, LEAF_S, 0, 18, LEAF); leafL(); sh(a, null, LW); crescent(a, leafR, LEAF_S, 0, 18, '#5aad48'); leafR(); sh(a, null, LW);
  a.beginPath(); a.arc(cx, 176, 26, 0, TAU); sh(a, '#f3c45f', LW2);
  // body
  const bodyP = () => blob(a, cx, 560, 240, 262, .025, 4);
  crescent(a, bodyP, PEACH_S, 34, 30, PEACH); bodyP(); sh(a, null, LW + 2);
  // cheeks
  a.fillStyle = 'rgba(232,110,110,.42)'; a.beginPath(); a.ellipse(cx - 150, 640, 46, 26, 0, 0, TAU); a.ellipse(cx + 150, 640, 46, 26, 0, 0, TAU); a.fill();
  // eyes
  const ey = 530, ex = 82;
  if (expr === 'meringis') { line(a, [[cx - ex - 30, ey - 26], [cx - ex + 18, ey], [cx - ex - 30, ey + 26]], 13); line(a, [[cx + ex + 30, ey - 26], [cx + ex - 18, ey], [cx + ex + 30, ey + 26]], 13); }
  else if (expr === 'lega' || blink > .8) { for (const sx of [-1, 1]) { a.beginPath(); a.moveTo(cx + sx * ex - 30, ey + 8); a.quadraticCurveTo(cx + sx * ex, ey + (expr === 'lega' ? -30 : 22), cx + sx * ex + 30, ey + 8); a.lineWidth = 13; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke(); } }
  else { for (const sx of [-1, 1]) { const up = expr === 'cemas' ? -8 : 0; a.beginPath(); a.ellipse(cx + sx * ex, ey + up, 22, 34, 0, 0, TAU); a.fillStyle = INK; a.fill(); a.beginPath(); a.ellipse(cx + sx * ex - 6, ey + up - 14, 8, 11, 0, 0, TAU); a.fillStyle = '#fff'; a.fill(); } }
  // glasses
  for (const sx of [-1, 1]) { a.beginPath(); a.arc(cx + sx * ex, ey, 64, 0, TAU); a.lineWidth = 11; a.strokeStyle = INK; a.stroke(); }
  line(a, [[cx - 20, ey - 6], [cx, ey - 18], [cx + 20, ey - 6]], 10);
  if (expr === 'cemas') { line(a, [[cx - 150, ey - 104], [cx - 60, ey - 128]], 11); line(a, [[cx + 150, ey - 104], [cx + 60, ey - 128]], 11); }
  // mouth
  const my = 680;
  if (expr === 'cemas') line(a, [[cx - 50, my], [cx - 25, my - 14], [cx, my], [cx + 25, my - 14], [cx + 50, my]], 11);
  else if (expr === 'meringis') { a.beginPath(); a.ellipse(cx, my, 40, 22, 0, 0, TAU); sh(a, '#8a2a2a', 9); }
  else if (expr === 'lega') { a.beginPath(); a.moveTo(cx - 60, my - 16); a.quadraticCurveTo(cx, my + 70, cx + 60, my - 16); a.closePath(); sh(a, '#8a2a2a', 9); a.save(); a.clip(); a.beginPath(); a.ellipse(cx, my + 34, 28, 16, 0, 0, TAU); a.fillStyle = '#ef6f6f'; a.fill(); a.restore(); }
  else { a.beginPath(); a.moveTo(cx - 50, my - 10); a.quadraticCurveTo(cx, my + 36, cx + 50, my - 10); a.lineWidth = 12; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke(); }
  // plaster on the right arm
  if (plaster > 0) { a.save(); a.globalAlpha = Math.min(1, plaster * 1.5); a.translate(640, 640); a.rotate(-.5); rr(a, -40, -18, 80, 36, 12); sh(a, '#f3d08a', LW2); a.fillStyle = '#c99a4c'; for (const d of [-14, 0, 14]) { a.beginPath(); a.arc(d, 0, 4, 0, TAU); a.fill(); } a.restore(); }
  // tear
  if (tear > 0 && tear < 1) { const ty = 580 + tear * 120; a.beginPath(); a.moveTo(cx - ex - 40, ty - 26); a.quadraticCurveTo(cx - ex - 62, ty + 4, cx - ex - 40, ty + 10); a.quadraticCurveTo(cx - ex - 18, ty + 4, cx - ex - 40, ty - 26); sh(a, SKY, 5); }
  a.restore();
  x.drawImage(finishCut(C, 16, { grainA: .7 }), 0, 0);
}

// ———————— adult (Mama / bidan) ————————
// pose: walk, stride, armL, armR (rad; 0 = hanging), reachL/reachR ([dx,dy] target from shoulder, overrides angle), hug (0-1), cotton, look
export const AD_W = 700, AD_H = 1500;
export function drawAdult(x, p = {}, kind = 'mama') {
  const { walk = 0, stride = 0, armL = .12, armR = .12, look = 0, hug = 0 } = p;
  const HIJ = kind === 'mama' ? TERRA : SKY, HIJ_S = kind === 'mama' ? TERRA_S : SKY_S, DR = kind === 'mama' ? SAGE : PINK, DR_S = kind === 'mama' ? SAGE_S : PINK_S;
  x.clearRect(0, 0, AD_W, AD_H);
  const C = cv(AD_W, AD_H), a = C.getContext('2d'), cx = 350, by = 1440;
  const s = Math.sin(walk) * stride, bob = -Math.abs(Math.sin(walk)) * stride * 12;
  for (const [fx, lift] of [[290, Math.max(0, s) * 20], [410, Math.max(0, -s) * 20]]) { blob(a, fx, by - 22 - lift, 56, 26, .04, fx); sh(a, '#8a5a3c', LW2); }
  a.save(); a.translate(0, bob);
  // gamis
  const dress = () => { a.beginPath(); a.moveTo(cx - 92, 560); a.lineTo(cx + 92, 560); a.bezierCurveTo(cx + 140, 900, cx + 190, 1200, cx + 196, by - 40); a.quadraticCurveTo(cx, by - 10, cx - 196, by - 40); a.bezierCurveTo(cx - 190, 1200, cx - 140, 900, cx - 92, 560); a.closePath(); };
  crescent(a, dress, DR_S, 40, 0, DR); dress(); sh(a, null, LW + 1);
  if (kind === 'bidan') { rr(a, cx - 60, 760, 120, 90, 16); sh(a, '#fffaf2', LW2); line(a, [[cx - 30, 790], [cx + 30, 790]], 6, PINK_S); }
  // hijab hood flowing over the shoulders
  const hood = () => { a.beginPath(); a.moveTo(cx, 120); a.bezierCurveTo(cx + 150, 120, cx + 190, 260, cx + 180, 400); a.bezierCurveTo(cx + 200, 520, cx + 230, 600, cx + 200, 660); a.quadraticCurveTo(cx, 720, cx - 200, 660); a.bezierCurveTo(cx - 230, 600, cx - 200, 520, cx - 180, 400); a.bezierCurveTo(cx - 190, 260, cx - 150, 120, cx, 120); a.closePath(); };
  crescent(a, hood, HIJ_S, 36, 26, HIJ); hood(); sh(a, null, LW + 1);
  // face
  const face = () => blob(a, cx, 350, 118, 134, .02, 9);
  crescent(a, face, SKIN_S, 24, 20, SKIN); face(); sh(a, null, LW);
  for (const sx of [-1, 1]) { a.beginPath(); a.ellipse(cx + sx * 46 + look * 14, 340, 13, 20, 0, 0, TAU); a.fillStyle = INK; a.fill(); }
  a.fillStyle = 'rgba(232,110,110,.4)'; a.beginPath(); a.ellipse(cx - 74, 400, 26, 15, 0, 0, TAU); a.ellipse(cx + 74, 400, 26, 15, 0, 0, TAU); a.fill();
  a.beginPath(); a.moveTo(cx - 36 + look * 10, 420); a.quadraticCurveTo(cx + look * 10, 452, cx + 36 + look * 10, 420); a.lineWidth = 10; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke();
  // arms: sleeve + hand; reach targets override angle
  const arm = (side, ang, reach) => {
    const sx = cx + side * 150, sy = 640;
    let hx, hy;
    if (reach) { hx = sx + reach[0]; hy = sy + reach[1]; } else { hx = sx + side * Math.sin(ang) * 400; hy = sy + Math.cos(ang) * 400; }
    a.beginPath(); a.moveTo(sx, sy); a.quadraticCurveTo((sx + hx) / 2 + side * 30, (sy + hy) / 2, hx, hy); a.lineWidth = 92; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke(); a.lineWidth = 76; a.strokeStyle = DR; a.stroke();
    a.beginPath(); a.arc(hx, hy, 44, 0, TAU); sh(a, SKIN, LW2 + 1);
    if (kind === 'bidan' && side === 1 && p.cotton) { blob(a, hx + 20, hy - 48, 34, 28, .1, 3); sh(a, '#ffffff', LW2); }
  };
  if (hug > 0) { arm(-1, 0, [ -60 + hug * 260, 120 + hug * 60]); arm(1, 0, [60 - hug * 260 + 0, 140 + hug * 60]); }
  else { arm(-1, armL, p.reachL); arm(1, armR, p.reachR); }
  a.restore();
  x.drawImage(finishCut(C, 16, { grainA: .7 }), 0, 0);
}

export function makeTunas(h = .034) { return actor(TU_W, TU_H, h, drawTunas, 880); }
export function makeAdult(kind, h = .062) { const f = ['papa', 'dokter', 'perawat'].includes(kind) ? drawPerson : drawAdult; return actor(AD_W, AD_H, h, (x, p) => f(x, p, kind), 1440); }

// ———————— Papa, Pak Dokter, Perawat (no hijab) ————————
// pose: walk, stride, armL, armR, reachL/reachR, look, blink, hug, sandals (Papa), steth (Dokter holds the chestpiece out)
const SUN = '#f3c45f', SUN_S = '#d6a53c', NAVY = '#2c3452', NAVY_S = '#1d2338', WHITE = '#fffdf7', WHITE_S = '#d9d3c7', HAIR = '#3b2f2a';
export function drawPerson(x, p = {}, kind = 'papa') {
  const { walk = 0, stride = 0, armL = .12, armR = .12, look = 0, hug = 0, blink = 0 } = p;
  x.clearRect(0, 0, AD_W, AD_H);
  const C = cv(AD_W, AD_H), a = C.getContext('2d'), cx = 350, by = 1440;
  const s = Math.sin(walk) * stride, bob = -Math.abs(Math.sin(walk)) * stride * 12;
  const shoe = kind === 'papa' ? null : '#8a5a3c';
  [[290, Math.max(0, s) * 20, p.sandals ? SKY : shoe || '#8a5a3c'], [410, Math.max(0, -s) * 20, p.sandals ? PINK : shoe || '#8a5a3c']].forEach(([fx, lift, col]) => { blob(a, fx, by - 22 - lift, 60, 26, .04, fx); sh(a, col, LW2); });
  a.save(); a.translate(0, bob);
  // legs
  const legCol = kind === 'perawat' ? SKIN : NAVY, legS = kind === 'perawat' ? SKIN_S : NAVY_S;
  for (const [lx, lift] of [[300, Math.max(0, s) * 20], [400, Math.max(0, -s) * 20]]) { rr(a, lx - 38, 960, 76, by - 40 - lift - 960, 30); sh(a, legCol, LW); }
  // torso: shirt (Papa), coat (Dokter), uniform dress (Perawat)
  const COL = kind === 'papa' ? SUN : WHITE, COL_S = kind === 'papa' ? SUN_S : WHITE_S, hem = kind === 'papa' ? 1010 : kind === 'dokter' ? 1250 : 1180;
  const torso = () => { a.beginPath(); a.moveTo(cx - 120, 540); a.lineTo(cx + 120, 540); a.bezierCurveTo(cx + 150, 700, cx + 170, 900, cx + 175, hem); a.quadraticCurveTo(cx, hem + 22, cx - 175, hem); a.bezierCurveTo(cx - 170, 900, cx - 150, 700, cx - 120, 540); a.closePath(); };
  crescent(a, torso, COL_S, 34, 0, COL); torso(); sh(a, null, LW + 1);
  if (kind === 'dokter') {
    a.beginPath(); a.moveTo(cx - 60, 540); a.lineTo(cx, 700); a.lineTo(cx + 60, 540); a.closePath(); sh(a, SKY, LW2 + 1);
    line(a, [[cx, 700], [cx, hem]], 6, WHITE_S); line(a, [[cx, 700], [cx, hem]], 0.1);
    rr(a, cx + 50, 760, 80, 40, 8); sh(a, SKY, LW2);
    if (!p.steth) { a.beginPath(); a.moveTo(cx - 70, 560); a.quadraticCurveTo(cx - 110, 760, cx - 20, 820); a.lineWidth = 14; a.strokeStyle = '#6b7a8a'; a.stroke(); a.beginPath(); a.arc(cx - 16, 830, 26, 0, TAU); sh(a, '#9aa8b6', LW2); }
  }
  if (kind === 'perawat') { line(a, [[cx, 560], [cx, hem]], 6, WHITE_S); rr(a, cx + 40, 700, 80, 40, 8); sh(a, SKY, LW2); }
  if (kind === 'papa') { a.beginPath(); a.moveTo(cx - 50, 540); a.lineTo(cx, 610); a.lineTo(cx + 50, 540); sh(a, null, LW2); for (const yy of [680, 780, 880]) { a.beginPath(); a.arc(cx, yy, 9, 0, TAU); a.fillStyle = INK; a.fill(); } }
  // neck + head
  rr(a, cx - 36, 450, 72, 110, 30); sh(a, SKIN, LW2);
  if (kind === 'perawat') { a.beginPath(); a.arc(cx + 104, 300, 62, 0, TAU); sh(a, HAIR, LW); }
  const face = () => blob(a, cx, 330, 124, 138, .02, 9);
  crescent(a, face, SKIN_S, 24, 20, SKIN); face(); sh(a, null, LW);
  // hair cap
  a.beginPath(); a.moveTo(cx - 128, 320); a.bezierCurveTo(cx - 140, 170, cx - 40, 150, cx + 10, 160); a.bezierCurveTo(cx + 120, 150, cx + 150, 230, cx + 128, 320); a.quadraticCurveTo(cx + 60, 230, cx - 20, 250); a.quadraticCurveTo(cx - 90, 260, cx - 128, 320); a.closePath(); sh(a, HAIR, LW);
  if (kind === 'perawat') { // nurse cap with a leaf-heart, never a red cross
    a.beginPath(); a.moveTo(cx - 110, 200); a.lineTo(cx + 110, 200); a.lineTo(cx + 80, 110); a.lineTo(cx - 80, 110); a.closePath(); sh(a, WHITE, LW);
    a.beginPath(); a.moveTo(cx, 182); a.bezierCurveTo(cx - 34, 160, cx - 22, 126, cx, 142); a.bezierCurveTo(cx + 22, 126, cx + 34, 160, cx, 182); sh(a, LEAF, 4);
  }
  // eyes (+ glasses for the doctor)
  for (const sx of [-1, 1]) { if (blink > .8) line(a, [[cx + sx * 46 - 16, 330], [cx + sx * 46 + 16, 330]], 10); else { a.beginPath(); a.ellipse(cx + sx * 46 + look * 14, 330, 13, 20, 0, 0, TAU); a.fillStyle = INK; a.fill(); } }
  if (kind === 'dokter') { for (const sx of [-1, 1]) { a.beginPath(); a.arc(cx + sx * 48, 330, 40, 0, TAU); a.lineWidth = 10; a.strokeStyle = INK; a.stroke(); } line(a, [[cx - 8, 330], [cx + 8, 330]], 10); }
  a.fillStyle = 'rgba(232,110,110,.4)'; a.beginPath(); a.ellipse(cx - 76, 392, 24, 14, 0, 0, TAU); a.ellipse(cx + 76, 392, 24, 14, 0, 0, TAU); a.fill();
  a.beginPath(); a.moveTo(cx - 36 + look * 10, 410); a.quadraticCurveTo(cx + look * 10, 442, cx + 36 + look * 10, 410); a.lineWidth = 10; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke();
  // arms
  const arm = (side, ang, reach) => {
    const sx = cx + side * 130, sy = 600;
    let hx, hy;
    if (reach) { hx = sx + reach[0]; hy = sy + reach[1]; } else { hx = sx + side * Math.sin(ang) * 400; hy = sy + Math.cos(ang) * 400; }
    a.beginPath(); a.moveTo(sx, sy); a.quadraticCurveTo((sx + hx) / 2 + side * 30, (sy + hy) / 2, hx, hy); a.lineWidth = 92; a.strokeStyle = INK; a.lineCap = 'round'; a.stroke(); a.lineWidth = 76; a.strokeStyle = COL; a.stroke();
    a.beginPath(); a.arc(hx, hy, 44, 0, TAU); sh(a, SKIN, LW2 + 1);
    if (kind === 'dokter' && p.steth && side === -1) { a.beginPath(); a.moveTo(cx - 70, 560); a.quadraticCurveTo((cx - 70 + hx) / 2 - 40, (560 + hy) / 2 - 60, hx, hy); a.lineWidth = 14; a.strokeStyle = '#6b7a8a'; a.stroke(); a.beginPath(); a.arc(hx - 10, hy + 10, 30, 0, TAU); sh(a, '#9aa8b6', LW2); }
    if (p.sticker && side === -1) { a.beginPath(); a.arc(hx - 10, hy - 40, 46, 0, TAU); sh(a, WHITE, LW2); a.beginPath(); a.moveTo(hx - 10, hy - 22); a.bezierCurveTo(hx - 50, hy - 46, hx - 36, hy - 84, hx - 10, hy - 64); a.bezierCurveTo(hx + 16, hy - 84, hx + 30, hy - 46, hx - 10, hy - 22); sh(a, LEAF, 4); }
  };
  if (hug > 0) { arm(-1, 0, [-60 + hug * 260, 120 + hug * 60]); arm(1, 0, [60 - hug * 260, 140 + hug * 60]); }
  else { arm(-1, armL, p.reachL); arm(1, armR, p.reachR); }
  a.restore();
  x.drawImage(finishCut(C, 16, { grainA: .7 }), 0, 0);
}

// germ: a small violet blob with a face (child logic, not scary)
export function germ(seed, oops = false) {
  return cut(.026, .026, (x, W, H) => {
    const R = Math.min(W, H) * .44, pts = () => { x.beginPath(); for (let i = 0; i <= 14; i++) { const ang = i / 14 * TAU, r = R * (i % 2 ? .8 : 1.05); x.lineTo(W / 2 + Math.cos(ang) * r, H / 2 + Math.sin(ang) * r); } x.closePath(); };
    crescent(x, pts, '#5e4a96', 10, 10, '#8a74c6'); pts(); sh(x, null, LW);
    for (const sx of [-1, 1]) { x.beginPath(); x.arc(W / 2 + sx * R * .32, H / 2 - R * .1, R * .1, 0, TAU); x.fillStyle = INK; x.fill(); }
    x.beginPath(); if (oops) x.arc(W / 2, H / 2 + R * .32, R * .12, 0, TAU); else { x.moveTo(W / 2 - R * .22, H / 2 + R * .28); x.quadraticCurveTo(W / 2, H / 2 + R * .4, W / 2 + R * .22, H / 2 + R * .28); } x.lineWidth = 8; x.strokeStyle = INK; x.stroke();
  }, { ay: .5, border: 12 });
}
