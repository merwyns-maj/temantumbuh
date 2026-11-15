// "Tunas Imunisasi": 40 s, one page, one camera. Timeline, camera, events, subtitles.
import { layer, clear, line, dab, text, handCircle, CAM, BOIL, WMUL, W, H, sx, sy } from './crayon.js';
import { group, clearGroup } from './rig.js';
import { tunas, adult, germ } from './chars.js';
import { outside, room, shield, GROUND, DOOR, STOOL, SHIELD } from './world.js';
import { PAL } from './pal.js';
import { clamp, lerp, hash, track, ss, eio, mulberry } from '/core/lib.js';
const K = PAL.crayon;
export const DUR = 40;
const BPM = 90, BEAT = 60 / BPM, BAR = BEAT * 4;
const seg = (t, a, b) => clamp((t - a) / (b - a));

// —— narration (placeholder voice durations from voices/dur.json) ——
const VD = { n1: 3.98, n2: 4.34, n3: 2.77, n4: 4.43, n5: 4.62, n6: 1.32 };
export const LINES = [
  { id: 'n1', t: 1.6, text: 'Hari ini, Tunas mau imunisasi.' },
  { id: 'n2', t: 11.6, text: 'Tunas agak deg-degan. Nggak apa-apa.' },
  { id: 'n3', t: 17.7, text: 'Mama pegang tangan Tunas.' },
  { id: 'n4', t: 23.7, text: 'Rasanya sakit sebentar. Boleh nangis.' },
  { id: 'n5', t: 29.6, text: 'Imunisasi bantu badan Tunas melawan kuman.' },
  { id: 'n6', t: 35.4, text: 'Tunas hebat!' },
].map(L => ({ ...L, d: VD[L.id] }));
export const SUBS = LINES.map((L, i) => { const t0 = L.t - 0.1; let t1 = Math.max(t0 + 1.8, L.t + L.d + 0.7); const nx = LINES[i + 1]; if (nx) t1 = Math.min(t1, nx.t - 0.25); else t1 = Math.min(t1, DUR - 0.3); return { t0, t1, text: L.text }; });

// —— timeline ——
const T = { drawT: [0.2, 2.6], mamaIn: [2.8, 3.9], walk: [4.1, 10.4], house: [6.2, 8.8], door: [8.9, 9.9],
  worry: [12.0, 13.2], hand: [17.2, 18.4], pan: [21.2, 22.3], roomOn: [21.0, 22.4], quiet: [22.3, 23.1], cus: 23.1, plaster: [23.4, 24.1],
  wash: [27.3, 29.7], germs: [30.2, 33.8], hug: [34.4, 35.3], pull: [37.4, 39.6] };
const TX0 = 520, TX1 = 2140;   // Tunas walks from TX0 to TX1 (in front of the door)

// —— camera [cx, cy, zoom] ——
const camT = track([
  [0, [540, 1150, 1.6]], [2.7, [540, 1150, 1.6]], [4.2, [640, 1040, 0.95]],
  [10.2, [TX1 + 60, 1040, 0.95]], [11.2, [TX1, 1200, 1.85]], [16.4, [TX1 + 6, 1205, 2.0]],
  [17.4, [TX1 - 110, 1120, 1.3]], [21.2, [TX1 - 110, 1120, 1.3]], [22.3, [3960, 1040, 1.2]], [26.9, [3970, 1050, 1.25]],
  [27.6, [4020, 960, 0.8]], [34.0, [4020, 960, 0.8]], [35.0, [3880, 1060, 1.3]], [37.4, [3880, 1060, 1.33]], [39.6, [2420, 900, 0.4]], [40, [2420, 900, 0.4]],
]);

// —— events for the mixer ——
export const EV = [];
const ev = (t, type, o = {}) => EV.push({ t: +t.toFixed(3), type, ...o });
LINES.forEach(L => ev(L.t, 'voice', { id: L.id }));
ev(0, 'paper'); ev(0.2, 'scratch', { dur: 2.2, pan: -0.3 }); ev(1.6, 'scribble', { dur: 1.0, pan: -0.2 });
ev(2.8, 'scratch', { dur: 1.1, pan: -0.5 });
for (let t = T.walk[0]; t < T.walk[1]; t += BEAT) ev(t, 'step', { pan: 0 });
ev(T.house[0], 'scratch', { dur: 2.6, pan: 0.5 }); ev(T.door[0], 'scribble', { dur: 1.0, pan: 0.3 }); ev(T.door[1] - 0.2, 'glint', { pan: 0.3 });
ev(T.worry[0], 'shaky', { dur: 1.2, pan: 0 });
ev(T.hand[0] + 0.6, 'swish', { pan: -0.2 }); ev(T.hand[1], 'glint', { pan: 0 });
ev(T.pan[0], 'whoosh', { dur: 1.0 }); ev(T.roomOn[0], 'scratch', { dur: 1.4, pan: 0.6 });
ev(T.quiet[0], 'silence', { dur: T.quiet[1] - T.quiet[0] }); ev(T.cus, 'cus', { pan: 0.2 }); ev(T.plaster[0], 'crinkle', { pan: 0.2 });
ev(T.wash[0], 'brush', { dur: T.wash[1] - T.wash[0], dir: 1 }); ev(T.wash[0] + 2.0, 'reveal');
[0, 1, 2].forEach(i => ev(T.germs[0] + 0.5 + i * 0.55 + 0.9, 'boing', { pan: 0.4 - i * 0.2 }));
ev(T.hug[0] + 0.5, 'puff'); ev(T.pull[0], 'page', { dur: 1.4 });
[['A', 0], ['B', 4.1], ['C', 10.7], ['D', 17.2], ['E', 22.3], ['F', 27.3], ['G', 34.4]].forEach(([id, t]) => ev(t, 'cue', { id }));

// —— layers ——
const BG = group(), WASH = layer(), MA = group(), TU = group(), BI = group(), ARMS = group(), FX = group(), SUBK = layer(), SUBT = layer();

function walkPose(t, a, b, x0, x1, ph0 = 0) {
  const u = seg(t, a, b), x = lerp(x0, x1, eio(u));
  const moving = t > a && t < b - 0.1;
  const ph = (t - a) / (BEAT * 2) * Math.PI * 2 + ph0;
  const k = moving ? Math.min(1, (t - a) * 3, (b - t) * 3) : 0;
  return { x, liftL: Math.max(0, Math.sin(ph)) * 14 * k, liftR: Math.max(0, -Math.sin(ph)) * 14 * k, bob: -Math.abs(Math.sin(ph)) * 8 * k, swing: Math.sin(ph) * 0.35 * k };
}

function drawScene(t) {
  // —— the page ——
  outside(BG, { sun: seg(t, 0.4, 2.0), tree: seg(t, 2.6, 4.4), ground: seg(t, 1.6, 4.0), house: seg(t, ...T.house), door: seg(t, ...T.door) });
  if (t > T.roomOn[0]) room(BG, seg(t, ...T.roomOn));
  if (t > T.roomOn[0]) shield(BG, 1);
  const outsideScene = t < T.pan[0] + 0.7, inRoom = t > T.pan[0] + 0.4;
  if (outsideScene) {
    const w = walkPose(t, ...T.walk, TX0, TX1);
    const mw = walkPose(t, T.walk[0] + 0.1, T.walk[1] - 0.2, TX0 - 260, TX1 - 280, Math.PI);
    const worried = t > T.worry[0] && t < T.hand[1] + 0.3;
    const holding = t > T.hand[0] + 0.5;
    const reach = seg(t, T.hand[0], T.hand[0] + 0.8);
    BOIL.amp = worried && !holding ? lerp(1, 2.2, seg(t, T.worry[0], T.worry[1])) : holding ? lerp(2.2, 0.9, seg(t, T.hand[0] + 0.5, T.hand[1] + 0.6)) : 1;
    // Mama: drawn on beside Tunas, walks, then reaches down for his hand
    const mhand = holding || reach > 0 ? [lerp(130, 196, ss(reach)), lerp(-200, -140, ss(reach))] : null;
    adult(MA, { x: mw.x, y: GROUND, s: 0.82, liftL: mw.liftL, liftR: mw.liftR, bob: mw.bob, aL: 0.2 - mw.swing * 0.5, aR: 0.2 + mw.swing * 0.5,
      handR: mhand, draw: seg(t, ...T.mamaIn), col: seg(t, T.mamaIn[0] + 0.5, T.mamaIn[1] + 0.6), look: t > T.hand[0] ? 6 : 0, seed: 300 });
    tunas(TU, { x: w.x, y: GROUND, s: 1, liftL: w.liftL, liftR: w.liftR, bob: w.bob, aL: 0.35 + w.swing * 0.6, aR: 0.35 - w.swing * 0.6,
      handL: holding ? [-120, -96] : null, expr: holding && t > T.hand[1] ? 'senang' : worried ? 'cemas' : 'senang',
      cheek: holding ? lerp(1, 1.5, seg(t, T.hand[0] + 0.5, T.hand[1])) : 1,
      draw: seg(t, ...T.drawT), col: seg(t, T.drawT[0] + 1.2, T.drawT[1] + 0.9), seed: 100 });
    // worry scribble above his head (a tangled blue line), rubbed away when Mama holds his hand
    const wq = seg(t, T.worry[0] + 0.3, T.worry[1]) * (1 - seg(t, T.hand[0] + 0.5, T.hand[1]));
    if (wq > 0) {
      const R = mulberry(77), pts = []; for (let i = 0; i < 26; i++) { const a = i * 0.9; pts.push([w.x + 120 + Math.cos(a) * (46 + 30 * R()), GROUND - 300 + Math.sin(a) * (34 + 20 * R()) - i * 0.8]); }
      line(FX.l, pts, { col: K.sky, w: 9, p: 0.9 * Math.min(1, wq * 2), seed: 78, draw: wq, boil: 2 });
    }
    // pink warmth spreading between their hands
    const pk = seg(t, T.hand[0] + 0.6, T.hand[1] + 0.4);
    if (pk > 0) { const hx = w.x - 125, hy = GROUND - 100; dab(FX.f, hx, hy - 20, 34 * pk, { col: K.pink, p: 0.6, seed: 79 }); for (let i = 0; i < 3; i++) { const a = -1.9 + i * 0.5; line(FX.l, [[hx + Math.cos(a) * 60, hy - 20 + Math.sin(a) * 60], [hx + Math.cos(a) * (60 + 40 * pk), hy - 20 + Math.sin(a) * (60 + 40 * pk)]], { col: K.pink, w: 6, p: 0.9, seed: 80 + i, draw: pk }); } }
  }
  if (inRoom) {
    const sitY = STOOL.top + 20;
    const hugU = seg(t, ...T.hug);
    const shot = seg(t, T.cus - 0.05, T.cus + 0.1), sting = t > T.cus && t < T.cus + 2.2;
    BOIL.amp = t > T.pull[0] ? lerp(1, 0.5, seg(t, ...T.pull)) : sting ? 1.4 : 1;
    // Mama stands at his left, holding his hand; for the hug she steps in and wraps her arms around him
    const mx = lerp(3700, 3770, ss(hugU));
    adult(MA, { x: mx, y: GROUND, s: 0.82, handR: hugU > 0 ? null : [180, -275], aR: 0.2, arms: hugU > 0.01 ? 'none' : 'all', seed: 300, look: 6 });
    // bidan at his right with a cotton ball; leaves the frame before the hug
    const bx = lerp(4240, 4560, ss(seg(t, 31.5, 33.5)));
    if (t < 34.0) adult(BI, { x: bx, y: GROUND, s: 0.8, flip: true, hijab: K.sky, dress: K.pink, handR: t < T.cus + 0.6 ? [lerp(260, 300, shot), -390] : [180, -330], cotton: true, seed: 400, look: 6 });
    const expr = t < T.cus ? 'cemas' : t < T.cus + 1.6 ? 'meringis' : hugU > 0 ? 'lega' : 'senang';
    tunas(TU, { x: STOOL.x, y: sitY, s: 0.95, expr, handL: hugU > 0 ? null : [-118, -70], aR: 0.45, plaster: seg(t, ...T.plaster),
      tear: t > T.cus + 0.4 ? seg(t, T.cus + 0.4, T.cus + 3.4) : 0, cheek: hugU > 0 ? 1.4 : 1, seed: 100 });
    // "cus": a small crayon star at his arm, then gone
    const cs = clamp(1 - Math.abs(t - T.cus - 0.12) / 0.35);
    if (cs > 0) { const cx = STOOL.x + 96, cy = sitY - 110; for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2; line(FX.l, [[cx + Math.cos(a) * 18, cy + Math.sin(a) * 18], [cx + Math.cos(a) * (18 + 42 * cs), cy + Math.sin(a) * (18 + 42 * cs)]], { col: K.yellow, w: 7, p: 1, seed: 200 + i }); } }
    if (hugU > 0.01) adult(ARMS, { x: mx, y: GROUND, s: 0.82, arms: 'only', handL: [lerp(-60, 170, ss(hugU)), lerp(-180, -150, ss(hugU))], handR: [lerp(120, 300, ss(hugU)), lerp(-200, -170, ss(hugU))], seed: 300 });
    // germs float in from the right, bump the shield, and drift away
    if (t > T.germs[0] && t < T.germs[1] + 0.6) {
      for (let i = 0; i < 3; i++) {
        const t0 = T.germs[0] + i * 0.55, u = seg(t, t0, t0 + 1.0), back = seg(t, t0 + 1.0, t0 + 2.6);
        const a = -0.6 + i * 0.6, far = SHIELD.r + 520, near = SHIELD.r + 80;
        const r = lerp(far, near, ss(u)) + lerp(0, 380, ss(back)) + Math.sin((t - t0) * 9) * 6 * (1 - back);
        const gx = SHIELD.x + Math.cos(a) * r, gy = SHIELD.y + Math.sin(a) * r + Math.sin(t * 3 + i) * 10;
        germ(FX, { x: gx, y: gy, s: 1.5, seed: 500 + i * 10, oops: back > 0 });
      }
    }
  }
}

// rose wash: one band sweeping left → right over the room
function drawWash(t) {
  const u = seg(t, ...T.wash); if (u <= 0) return;
  const g = WASH.g; g.save();
  g.setTransform(CAM.s, 0, 0, CAM.s, W / 2 - CAM.x * CAM.s, H / 2 - CAM.y * CAM.s);
  const X0 = 3150, X1 = 4950, y0 = 470, y1 = 1440, e = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2, f = lerp(X0, X1, 0.15 * u + 0.85 * e);
  const front = y => f + 80 * Math.sin(clamp((y - y0) / (y1 - y0)) * Math.PI) + 14 * Math.sin(y * 0.05);
  g.beginPath(); g.moveTo(X0 - 60, y0 - 220); for (let y = y0 - 220; y <= y1 + 220; y += 20) g.lineTo(front(y), y); g.lineTo(X0 - 60, y1 + 220); g.closePath(); g.clip();
  const shape = new Path2D(); for (let x = X0; x <= X1 + 60; x += 40) shape.lineTo(x, y0 + 14 * Math.sin(x * 0.006) + 12 * hash(x * 0.37)); for (let x = X1 + 60; x >= X0; x -= 40) shape.lineTo(x, y1 + 16 * Math.sin(x * 0.005 + 2) + 14 * hash(x * 0.71)); shape.closePath();
  g.fillStyle = '#000'; g.globalAlpha = 0.72; g.fill(shape);
  g.save(); g.clip(shape); const R = mulberry(31);
  for (let i = 0; i < 22; i++) { const yy = lerp(y0, y1, R()), wd = 6 + R() * 28, dark = R() < 0.55; g.beginPath(); for (let x = X0; x <= X1 + 60; x += 60) { const y = yy + 12 * Math.sin(x * 0.002 + i); x === X0 ? g.moveTo(x, y) : g.lineTo(x, y); } g.lineWidth = dark ? wd : wd * 0.5; g.globalCompositeOperation = dark ? 'source-over' : 'destination-out'; g.globalAlpha = dark ? 0.12 + R() * 0.1 : 0.05 + R() * 0.06; g.strokeStyle = '#000'; g.stroke(); }
  g.globalCompositeOperation = 'source-over';
  const moving = u < 1; g.beginPath(); for (let y = y0 - 80; y <= y1 + 80; y += 16) { const x = front(y) - 14; y === y0 - 80 ? g.moveTo(x, y) : g.lineTo(x, y); }
  g.lineWidth = moving ? 34 : 20; g.globalAlpha = moving ? 0.3 : 0.12; g.stroke();
  g.restore(); g.restore();
}

function subTo(t) {
  const S = SUBS.find(s => t >= s.t0 && t < s.t1); if (!S) return;
  const rv = clamp((t - S.t0) / 0.35);
  const g = SUBK.g; g.save(); g.font = '400 56px "Patrick Hand"'; const tw = g.measureText(S.text).width;
  const cx = 960, cy = 1002, hw = tw / 2 + 46, hh = 44;
  g.fillStyle = '#000'; g.beginPath();
  for (let i = 0; i <= 60; i++) { const a = i / 60 * Math.PI * 2; const px = Math.cos(a), py = Math.sin(a); const sq = Math.pow(Math.abs(px), 0.3) * Math.sign(px); const n = 1 + 0.06 * Math.sin(a * 7 + 1.3) + 0.03 * Math.sin(a * 17); const X = cx + sq * hw * n, Y = cy + py * hh * n; i ? g.lineTo(X, Y) : g.moveTo(X, Y); }
  g.closePath(); g.fill(); g.restore();
  text(SUBT, S.text, cx, cy + 18, { size: 56, col: K.ink, reveal: rv, seed: 11 + S.t0 * 3, p: 1, stroke: 1.2 });
}

export function frame(comp, t) {
  const [cx, cy, cs] = camT(t); CAM.x = cx; CAM.y = cy; CAM.s = cs;
  [BG, MA, TU, BI, ARMS, FX].forEach(clearGroup); [WASH, SUBK, SUBT].forEach(clear);
  BOIL.amp = 1;
  drawScene(t); drawWash(t); subTo(t);
  comp.paperCam(CAM.x * 0.6, CAM.y * 0.6, CAM.s / 0.6);
  comp.begin(PAL.paper);
  comp.group(BG);
  if (t > T.wash[0]) comp.wash(WASH.c, { color: PAL.wash, resist: 0.95 });
  comp.group(MA); comp.group(BI); comp.group(TU); comp.group(ARMS); comp.group(FX);
  comp.knock(SUBK.c); comp.crayon(SUBT.c);
  comp.finish({ vig: 0.3 });
}

// model sheet: Tunas in four expressions, Mama, the bidan, a germ
export function modelSheet(comp) {
  CAM.x = 960; CAM.y = 540; CAM.s = 1;
  [BG, MA, TU, BI, ARMS, FX].forEach(clearGroup); [WASH, SUBK, SUBT].forEach(clear);
  ['senang', 'cemas', 'meringis', 'lega'].forEach((e, i) => tunas(TU, { x: 170 + i * 250, y: 480, s: 0.78, expr: e, seed: 100, plaster: i === 3 ? 1 : 0, tear: i === 2 ? 0.4 : 0 }));
  adult(MA, { x: 1220, y: 1010, s: 0.85, seed: 300 });
  adult(BI, { x: 1560, y: 1010, s: 0.85, hijab: K.sky, dress: K.pink, flip: true, cotton: true, handR: [180, -330], seed: 400 });
  germ(FX, { x: 1800, y: 300, s: 1.2, seed: 500 });
  tunas(TU, { x: 420, y: 1010, s: 1.2, expr: 'senang', aL: 0.9, aR: 0.2, liftL: 12, seed: 100 });
  text(SUBT, 'Tunas · Mama · Bidan · Kuman', 760, 640, { size: 48, col: K.ink, seed: 3 });
  comp.paperCam(576, 324, 1 / 0.6); comp.begin(PAL.paper);
  comp.group(BG); comp.group(MA); comp.group(BI); comp.group(TU); comp.group(FX); comp.crayon(SUBT.c); comp.finish({ vig: 0.25 });
}
