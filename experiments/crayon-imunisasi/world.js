// The page: outside (sun, tree, road, puskesmas) on the left, the clinic room on the right.
// One page, 4800 × 1800 world units. Each element draws on with a progress value d (0–1): outline first, then colour.
import { line, fill, dab, text, ellipse, handCircle, bez, smooth, CAM, sx, sy } from './crayon.js';
import { part } from './rig.js';
import { PAL } from './pal.js';
import { clamp, hash } from '/core/lib.js';
const K = PAL.crayon;
export const GROUND = 1340;
export const DOOR = { x0: 2330, x1: 2540 };
export const STOOL = { x: 3960, top: 1160 };
export const SHIELD = { x: 3960, y: 1010, r: 330 };

const pr = (d, a, b) => clamp((d - a) / (b - a));
const O = (d, seed, w = 6.5) => ({ col: K.ink, w, p: 0.9, seed, draw: pr(d, 0, 0.6) });
const F = (d, col, seed, x = {}) => pr(d, 0.45, 1) > 0 ? { col, p: 0.8, seed, draw: pr(d, 0.45, 1), ...x } : null;

export function outside(G, d) {
  const dSun = d.sun ?? 1, dTree = d.tree ?? 1, dHouse = d.house ?? 1, dGround = d.ground ?? 1, dDoor = d.door ?? 1;
  // sun with rays
  part(G, handCircle(560, 360, 90, 11, 0.08), F(dSun, K.yellow, 11, { gap: 9, w: 10 }), O(dSun, 11, 7));
  for (let i = 0; i < 9; i++) { const a = i / 9 * Math.PI * 2 + 0.2; line(G.l, [[560 + Math.cos(a) * 120, 360 + Math.sin(a) * 120], [560 + Math.cos(a) * 165, 360 + Math.sin(a) * 165]], { col: K.yellow, w: 8, p: 0.9, seed: 12 + i, draw: pr(dSun, 0.4, 1) }); }
  // ground line + grass tufts along the whole page
  line(G.l, [[-200, GROUND], [3100, GROUND + 6]], { col: K.ink, w: 7, p: 0.9, seed: 20, draw: dGround });
  part(G, [[-200, GROUND - 6], [3100, GROUND], [3100, GROUND + 46], [-200, GROUND + 40]], F(dGround, K.leaf, 21, { gap: 8, w: 9, ang: 1.4 }), null, { occ: false });
  for (let i = 0; i < 26; i++) { const x = -100 + i * 125 + 40 * hash(i); line(G.l, [[x - 14, GROUND], [x - 6, GROUND - 30], [x, GROUND - 4], [x + 8, GROUND - 34], [x + 14, GROUND]], { col: K.leaf, w: 5, p: 0.85, seed: 30 + i, draw: pr(dGround, 0.3, 1) }); }
  // tree
  const TXo = -330;
  part(G, [[230 + TXo, GROUND], [236 + TXo, GROUND - 260], [282 + TXo, GROUND - 260], [290 + TXo, GROUND]], F(dTree, K.brown, 40, { gap: 7, w: 8, ang: 1.5 }), O(dTree, 40));
  const crown = smooth([[260, 760], [370, 800], [420, 900], [380, 1020], [260, 1060], [140, 1020], [100, 900], [150, 800]].map(([x, y]) => [x + TXo, y]), 8);
  part(G, crown, F(dTree, K.leaf, 41, { gap: 10, w: 11, cross: true }), O(dTree, 41, 7));
  // puskesmas: walls, roof, sign, windows, door. No red cross (UU 1/2018); a leaf-heart sign instead.
  const wx0 = 1920, wx1 = 2900, wy = 820;
  part(G, [[wx0, GROUND], [wx0, wy], [wx1, wy], [wx1, GROUND]], F(dHouse, K.ochre, 50, { gap: 11, w: 12, p: 0.72 }), O(dHouse, 50, 7.5));
  part(G, [[wx0 - 90, wy + 10], [wx0 + 60, wy - 190], [wx1 - 60, wy - 190], [wx1 + 90, wy + 10]], F(dHouse, K.terra, 51, { gap: 10, w: 11, ang: 0.3 }), O(dHouse, 51, 8));
  for (const [x0, k] of [[1990, 0], [2640, 1]]) {
    const win = [[x0, 1000], [x0 + 190, 1000], [x0 + 190, 1160], [x0, 1160]];
    part(G, win, F(dHouse, K.sky, 52 + k, { gap: 8, w: 9 }), O(dHouse, 52 + k, 6));
    line(G.l, [[x0 + 95, 1000], [x0 + 95, 1160]], O(dHouse, 54 + k, 5)); line(G.l, [[x0, 1080], [x0 + 190, 1080]], O(dHouse, 56 + k, 5));
  }
  const sign = [[2080, 860], [2740, 860], [2740, 960], [2080, 960]];
  part(G, sign, null, O(dHouse, 58, 6), { occ: true });
  const heart = bez([[2150, 945], [2105, 915], [2100, 875], [2130, 872], [2140, 870], [2150, 880], [2150, 890], [2150, 880], [2160, 870], [2170, 872], [2200, 875], [2195, 915], [2150, 945]], 8);
  part(G, heart, F(dHouse, K.leaf, 59, { gap: 5, w: 6 }), O(dHouse, 59, 4.5));
  if (dHouse > 0.5) text(G.l, 'PUSKESMAS', sx(2450), sy(935), { size: 74 * CAM.s, col: K.ink, seed: 60, reveal: pr(dHouse, 0.5, 0.9) });
  // door (coloured on as its own beat)
  const door = [[DOOR.x0, GROUND], [DOOR.x0, 1040], [DOOR.x1, 1040], [DOOR.x1, GROUND]];
  part(G, door, pr(dDoor, 0.1, 1) > 0 ? { col: K.sage, p: 0.85, seed: 61, draw: pr(dDoor, 0.1, 1), gap: 9, w: 10 } : null, O(dHouse, 61, 7));
  line(G.l, [[(DOOR.x0 + DOOR.x1) / 2, 1040], [(DOOR.x0 + DOOR.x1) / 2, GROUND]], O(dHouse, 62, 5));
  dab(G.l, DOOR.x0 + 80, 1200, 9, { col: K.yellow, p: 1, seed: 63 }); dab(G.l, DOOR.x1 - 80, 1200, 9, { col: K.yellow, p: 1, seed: 64 });
}

export function room(G, d) {
  const x0 = 3200, x1 = 4900;
  line(G.l, [[x0, GROUND], [x1, GROUND + 4]], O(d, 70, 7));
  part(G, [[x0, GROUND], [x1, GROUND + 4], [x1, GROUND + 70], [x0, GROUND + 64]], F(d, K.ochre, 71, { gap: 9, w: 10, ang: 0.15, p: 0.6 }), null, { occ: false });
  // window with a cloud
  const win = [[4420, 600], [4700, 600], [4700, 860], [4420, 860]];
  part(G, win, F(d, K.sky, 72, { gap: 8, w: 9 }), O(d, 72));
  line(G.l, [[4560, 600], [4560, 860]], O(d, 73, 5)); line(G.l, [[4420, 730], [4700, 730]], O(d, 74, 5));
  // wall poster: a heart (kept simple, no words)
  part(G, [[3330, 560], [3570, 560], [3570, 820], [3330, 820]], null, O(d, 75, 5.5));
  const heart = bez([[3450, 780], [3380, 730], [3375, 650], [3420, 640], [3440, 636], [3450, 655], [3450, 670], [3450, 655], [3460, 636], [3480, 640], [3525, 650], [3520, 730], [3450, 780]], 8);
  part(G, heart, F(d, K.pink, 76, { gap: 6, w: 7 }), O(d, 76, 5));
  // stool
  const S = STOOL;
  part(G, [[S.x - 120, S.top], [S.x + 120, S.top], [S.x + 112, S.top + 34], [S.x - 112, S.top + 34]], F(d, K.brown, 77, { gap: 7, w: 8 }), O(d, 77));
  for (const [a, b] of [[-96, -120], [96, 120]]) part(G, [[S.x + a - 12, S.top + 30], [S.x + a + 12, S.top + 30], [S.x + b + 12, GROUND], [S.x + b - 12, GROUND]], F(d, K.brown, 78 + a, { gap: 6, w: 7, ang: 1.4 }), O(d, 78 + a, 5));
}

// white wax shield: a thick ring + small sparkles; invisible on paper, shows white under the wash
export function shield(G, d = 1) {
  if (d <= 0) return;
  const { x, y, r } = SHIELD;
  line(G.f, handCircle(x, y, r, 90, 0.04, 90), { col: K.white, w: 30, p: 1, seed: 90, draw: d, boil: 0.4 });
  line(G.f, handCircle(x, y, r - 30, 91, 0.04, 90), { col: K.white, w: 14, p: 0.9, seed: 91, draw: d, boil: 0.4 });
  for (let i = 0; i < 14; i++) {
    const a = i / 14 * Math.PI * 2 + 0.3, rr = r + 60 + 30 * hash(i * 3.1);
    const cx = x + Math.cos(a) * rr, cy = y + Math.sin(a) * rr, k = 18 + 10 * hash(i);
    line(G.f, [[cx - k, cy], [cx + k, cy]], { col: K.white, w: 8, p: 1, seed: 92 + i, boil: 0.3 });
    line(G.f, [[cx, cy - k], [cx, cy + k]], { col: K.white, w: 8, p: 1, seed: 120 + i, boil: 0.3 });
  }
}
