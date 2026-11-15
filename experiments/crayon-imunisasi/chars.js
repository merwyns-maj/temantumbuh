// Characters in crayon: Tunas (our mascot, redrawn as a child would), Mama, the bidan, a germ.
// Every function draws into a group {k, f, l} from rig.js. Coordinates are local (feet at 0,0), scaled by o.s, placed at o.x, o.y.
import { line, fill, dab, ellipse, handCircle, bez, smooth } from './crayon.js';
import { part, tube } from './rig.js';
import { PAL } from './pal.js';
import { clamp, lerp } from '/core/lib.js';
const K = PAL.crayon;

const mk = o => { const s = o.s ?? 1, X = o.x ?? 0, Y = o.y ?? 0, fl = o.flip ? -1 : 1; return pts => pts.map(([x, y]) => [X + x * s * fl, Y + y * s]); };
const LO = (o, seed, w = 6.5) => ({ col: K.ink, w, p: 0.9, seed, draw: o.draw ?? 1 });
const FO = (o, col, seed, extra = {}) => (o.col ?? 1) > 0 ? { col, p: 0.8, seed, draw: o.col ?? 1, ...extra } : null;

// arm: shoulder → hand at angle a (radians from straight down, + = outward), length len, small bend
function armPts(sh, a, len, side, bend = 0.25) {
  const hx = sh[0] + side * Math.sin(a) * len, hy = sh[1] + Math.cos(a) * len;
  const mx = (sh[0] + hx) / 2 + side * Math.cos(a) * len * bend * 0.3, my = (sh[1] + hy) / 2 - Math.sin(a) * len * bend * 0.1;
  return [sh, [mx, my], [hx, hy]];
}
// arm reaching a local target point
function armTo(sh, tgt) { const mx = (sh[0] + tgt[0]) / 2, my = (sh[1] + tgt[1]) / 2 + 10; return [sh, [mx, my], tgt]; }

// ———————— Tunas ————————
// o: x, y, s, expr (senang|cemas|meringis|lega), aL, aR (arm angles), handL/handR (local targets, override angle),
// liftL, liftR (feet), bob, draw (outline progress), col (colour progress), plaster, tear (0–1), cheek (1 = normal), seed
export function tunas(C, o = {}) {
  const P = mk(o), sd = o.seed ?? 100, bob = o.bob ?? 0;
  const B = pts => P(pts.map(([x, y]) => [x, y + bob]));
  // feet
  part(C, P(ellipse(-38, -15 - (o.liftL ?? 0), 30, 16)), FO(o, K.terra, sd + 1, { gap: 7, w: 8 }), LO(o, sd + 1, 5));
  part(C, P(ellipse(38, -15 - (o.liftR ?? 0), 30, 16)), FO(o, K.terra, sd + 2, { gap: 7, w: 8 }), LO(o, sd + 2, 5));
  // arms (behind the body)
  const shL = [-78, -140 + bob], shR = [78, -140 + bob];
  const aL = o.handL ? armTo(shL, o.handL) : armPts(shL, o.aL ?? 0.35, 72, -1);
  const aR = o.handR ? armTo(shR, o.handR) : armPts(shR, o.aR ?? 0.35, 72, 1);
  part(C, P(tube(aL, 24, 22)), FO(o, K.peach, sd + 3, { gap: 6, w: 7 }), LO(o, sd + 3, 5));
  part(C, P(tube(aR, 24, 22)), FO(o, K.peach, sd + 4, { gap: 6, w: 7 }), LO(o, sd + 4, 5));
  // stem and leaves
  line(C.l, B([[0, -205], [2, -230], [0, -252]]), { col: K.leaf, w: 9, p: 0.95, seed: sd + 5, draw: o.draw ?? 1 });
  const leafL = [[0, -250], [-18, -292], [-62, -300], [-88, -278], [-62, -258], [-26, -248], [0, -250]];
  part(C, B(bez(leafL, 10)), FO(o, K.leaf, sd + 6, { gap: 7, w: 8, ang: 1.1 }), LO(o, sd + 6, 5));
  part(C, B(bez(leafL.map(([x, y]) => [-x, y]), 10)), FO(o, K.leaf, sd + 7, { gap: 7, w: 8, ang: -1.1 }), LO(o, sd + 7, 5));
  part(C, B(handCircle(0, -256, 11, sd + 8, 0.05, 24)), FO(o, K.yellow, sd + 8, { gap: 4, w: 6 }), LO(o, sd + 8, 4));
  // body
  part(C, B(ellipse(0, -122, 96, 102, 60)), FO(o, K.peach, sd + 9, { gap: 9, w: 10, p: 0.72 }), LO(o, sd + 9, 7.5));
  if ((o.draw ?? 1) < 0.6) return;
  face(C, B, o, sd);
  if (o.plaster) {
    const [hx, hy] = aR[2]; const mx = lerp(aR[1][0], hx, 0.3), my = lerp(aR[1][1], hy, 0.3);
    const pl = [[mx - 16, my - 10], [mx + 16, my - 14], [mx + 18, my + 6], [mx - 14, my + 10]];
    part(C, P(pl), { col: K.ochre, p: 0.95 * clamp(o.plaster), seed: sd + 30, gap: 4, w: 6 }, { col: K.ink, w: 3.5, p: 0.9 * clamp(o.plaster), seed: sd + 30 }, { occ: false });
  }
  if ((o.tear ?? 0) > 0) {
    const u = clamp(o.tear), ty = -112 + 34 * u;
    dab(C.f, ...P([[-44, ty + bob]])[0], 8 * (o.s ?? 1), { col: K.sky, p: 0.95 * Math.min(1, (1 - u) * 3), seed: sd + 31, sq: 1.3 });
  }
}

function face(C, B, o, sd) {
  const e = o.expr ?? 'senang', s = o.s ?? 1, cheek = o.cheek ?? 1;
  // cheeks
  dab(C.f, ...B([[-64, -98]])[0], 15 * s * cheek, { col: K.pink, p: 0.8, seed: sd + 10, sq: 0.6 });
  dab(C.f, ...B([[64, -98]])[0], 15 * s * cheek, { col: K.pink, p: 0.8, seed: sd + 11, sq: 0.6 });
  // eyes
  if (e === 'meringis') {
    line(C.l, B([[-50, -150], [-30, -139], [-50, -128]]), { col: K.ink, w: 5.5, p: 0.95, seed: sd + 12 });
    line(C.l, B([[50, -150], [30, -139], [50, -128]]), { col: K.ink, w: 5.5, p: 0.95, seed: sd + 13 });
  } else if (e === 'lega') {
    line(C.l, B([[-50, -134], [-37, -148], [-24, -134]]), { col: K.ink, w: 5.5, p: 0.95, seed: sd + 12 });
    line(C.l, B([[24, -134], [37, -148], [50, -134]]), { col: K.ink, w: 5.5, p: 0.95, seed: sd + 13 });
  } else {
    const up = e === 'cemas' ? -4 : 0;
    dab(C.l, ...B([[-36, -138 + up]])[0], 7.5 * s, { col: K.ink, p: 1, seed: sd + 12 });
    dab(C.l, ...B([[36, -138 + up]])[0], 7.5 * s, { col: K.ink, p: 1, seed: sd + 13 });
  }
  // glasses
  line(C.l, B(handCircle(-36, -138, 25, sd + 14, 0.1, 40)), { col: K.ink, w: 5, p: 0.95, seed: sd + 14 });
  line(C.l, B(handCircle(36, -138, 25, sd + 15, 0.1, 40)), { col: K.ink, w: 5, p: 0.95, seed: sd + 15 });
  line(C.l, B([[-11, -140], [0, -146], [11, -140]]), { col: K.ink, w: 4.5, p: 0.9, seed: sd + 16 });
  // worried brows
  if (e === 'cemas') {
    line(C.l, B([[-58, -174], [-22, -184]]), { col: K.ink, w: 5, p: 0.9, seed: sd + 17 });
    line(C.l, B([[58, -174], [22, -184]]), { col: K.ink, w: 5, p: 0.9, seed: sd + 18 });
  }
  // mouth
  if (e === 'cemas') line(C.l, B([[-22, -84], [-11, -90], [0, -84], [11, -90], [22, -84]]), { col: K.ink, w: 5, p: 0.95, seed: sd + 19 });
  else if (e === 'meringis') part(C, B(ellipse(0, -84, 16, 9, 24)), { col: K.ink, p: 0.9, seed: sd + 19, gap: 3, w: 5 }, { col: K.ink, w: 4, p: 0.9, seed: sd + 19 }, { occ: false });
  else if (e === 'lega') part(C, B(bez([[-26, -92], [-16, -66], [16, -66], [26, -92], [10, -88], [-10, -88], [-26, -92]], 8)), { col: K.ink, p: 0.85, seed: sd + 19, gap: 3, w: 5 }, { col: K.ink, w: 4.5, p: 0.95, seed: sd + 19 }, { occ: false });
  else line(C.l, B(bez([[-24, -92], [-12, -74], [12, -74], [24, -92]], 10)), { col: K.ink, w: 5.5, p: 0.95, seed: sd + 19 });
}

// ———————— Mama / bidan (same build, different crayons) ————————
// o: x, y, s, hijab, dress, handL/handR (local targets) or aL/aR, liftL/liftR, bob, draw, col, arms ('all'|'none'|'only'), cotton (bidan), seed, look (eye dx)
export function adult(C, o = {}) {
  const P = mk(o), sd = o.seed ?? 300, bob = o.bob ?? 0;
  const B = pts => P(pts.map(([x, y]) => [x, y + bob]));
  const hij = o.hijab ?? K.terra, dr = o.dress ?? K.sage;
  const shL = [-70, -350 + bob], shR = [70, -350 + bob];
  const aL = o.handL ? armTo(shL, o.handL) : armPts(shL, o.aL ?? 0.18, 175, -1, 0.3);
  const aR = o.handR ? armTo(shR, o.handR) : armPts(shR, o.aR ?? 0.18, 175, 1, 0.3);
  const arms = () => {
    for (const [a, k] of [[aL, 0], [aR, 1]]) {
      part(C, P(tube(a, 46, 38)), FO(o, dr, sd + 20 + k, { gap: 8, w: 9 }), LO(o, sd + 20 + k, 6));
      part(C, P(handCircle(a[2][0], a[2][1] + 4, 21, sd + 22 + k, 0.06, 28)), FO(o, K.peach, sd + 22 + k, { gap: 5, w: 6 }), LO(o, sd + 22 + k, 5));
    }
    if (o.cotton) { const h = aR[2]; part(C, P(handCircle(h[0] + 10, h[1] - 14, 16, sd + 40, 0.05, 24)), null, { col: K.ink, w: 3.5, p: 0.9, seed: sd + 40 }); }
  };
  if (o.arms === 'only') { arms(); return; }
  // shoes
  part(C, P(ellipse(-34, -12 - (o.liftL ?? 0), 30, 14)), FO(o, K.brown, sd + 1, { gap: 6, w: 7 }), LO(o, sd + 1, 5));
  part(C, P(ellipse(34, -12 - (o.liftR ?? 0), 30, 14)), FO(o, K.brown, sd + 2, { gap: 6, w: 7 }), LO(o, sd + 2, 5));
  // long dress (gamis)
  const dress = smooth([[-62, -372], [62, -372], [96, -200], [124, -28], [0, -18], [-124, -28], [-96, -200]].map(([x, y]) => [x, y + bob * (1 + y / 400)]), 6);
  part(C, P(dress), FO(o, dr, sd + 3, { gap: 11, w: 12, p: 0.78 }), LO(o, sd + 3, 7));
  // hijab: rounded hood flowing over the shoulders
  const hood = smooth([[0, -540], [70, -520], [96, -456], [102, -380], [118, -318], [0, -296], [-118, -318], [-102, -380], [-96, -456], [-70, -520]], 7);
  part(C, B(hood), FO(o, hij, sd + 4, { gap: 9, w: 10, p: 0.85 }), LO(o, sd + 4, 7));
  // face
  part(C, B(ellipse(0, -440, 58, 64, 40)), FO(o, K.peach, sd + 5, { gap: 8, w: 9, p: 0.7 }), LO(o, sd + 5, 6));
  if ((o.draw ?? 1) >= 0.6) {
    const s = o.s ?? 1, lk = o.look ?? 0;
    dab(C.l, ...B([[-22 + lk, -446]])[0], 6.5 * s, { col: K.ink, p: 1, seed: sd + 6 });
    dab(C.l, ...B([[22 + lk, -446]])[0], 6.5 * s, { col: K.ink, p: 1, seed: sd + 7 });
    dab(C.f, ...B([[-36, -414]])[0], 11 * s, { col: K.pink, p: 0.75, seed: sd + 8, sq: 0.6 });
    dab(C.f, ...B([[36, -414]])[0], 11 * s, { col: K.pink, p: 0.75, seed: sd + 9, sq: 0.6 });
    line(C.l, B(bez([[-18, -412], [-8, -398], [8, -398], [18, -412]], 8)), { col: K.ink, w: 4.5, p: 0.95, seed: sd + 10 });
  }
  if (o.arms !== 'none') arms();
}

// ———————— germ (child logic: a small blob with a face, not scary) ————————
export function germ(C, o = {}) {
  const P = mk(o), sd = o.seed ?? 500, r = 46;
  const pts = []; for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2, rr = r * (i % 2 ? 0.78 : 1.05); pts.push([Math.cos(a) * rr, Math.sin(a) * rr]); }
  part(C, P(smooth(pts, 5)), { col: K.violet, p: 0.85, seed: sd, gap: 7, w: 8 }, { col: K.ink, w: 5, p: 0.9, seed: sd });
  dab(C.l, ...P([[-14, -6]])[0], 5.5 * (o.s ?? 1), { col: K.ink, p: 1, seed: sd + 1 });
  dab(C.l, ...P([[14, -6]])[0], 5.5 * (o.s ?? 1), { col: K.ink, p: 1, seed: sd + 2 });
  line(C.l, P(o.oops ? handCircle(0, 14, 6, sd + 3, 0.05, 16) : [[-10, 14], [0, 18], [10, 14]]), { col: K.ink, w: 4, p: 0.9, seed: sd + 3 });
}
