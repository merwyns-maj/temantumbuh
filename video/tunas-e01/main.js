// "Tunas Mau Imunisasi", episode 1 (paper pop-up book; engine: Lemo-Opuscar paper-popup, MIT).
import * as THREE from 'three';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { clamp, lerp, seg, ss, eio, eo, back, spring, track, TAU } from './lib.js';
import * as A from './art.js';
import { makeBook, coverCanvases, texOf, PG } from './book.js';
import { cutMesh, thread } from './cutmesh.js';
import { makePost } from './post.js';
import { makeTunas, makeAdult, germ, drawTunas, TU_W, TU_H } from './chars.js';
import * as P2 from './props2.js';
import * as PR from './props.js';
import { cv } from './paper.js';

const W = 1920, H = 1080, Q = new URLSearchParams(location.search);
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setSize(W, H); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.NeutralToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('stage').appendChild(renderer.domElement);
const ov = document.getElementById('ov'), OX = ov.getContext('2d');
const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(30, W / H, .004, 30);
const post = makePost(renderer, scene, cam, W, H);

await Promise.all(['600 40px Fredoka', '700 40px Fredoka', '40px "Lilita One"'].map(f => document.fonts.load(f)));
// room light: a synthetic warm room HDRI (no Poly Haven download needed)
const hdr = await new RGBELoader().loadAsync('assets/room_2k.hdr'); hdr.mapping = THREE.EquirectangularReflectionMapping;
scene.environment = hdr; scene.background = hdr; scene.backgroundBlurriness = .35;
const tl = new THREE.TextureLoader();
const wt = n => { const t = tl.load(`assets/walnut_${n}.jpg`); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(2.2, 1.4); return t; };
const wd = wt('diff'); wd.colorSpace = THREE.SRGBColorSpace;
const desk = new THREE.Mesh(new THREE.BoxGeometry(2.6, .04, 1.7), new THREE.MeshStandardMaterial({ map: wd, normalMap: wt('nor'), roughnessMap: wt('rough'), color: '#c9a88a', envMapIntensity: .8 }));
desk.position.set(0, -.02, .25); desk.receiveShadow = true; scene.add(desk);
const gl = new GLTFLoader();
async function prop(name, x, z, s, ry) { const m = (await gl.loadAsync(`assets/${name}/${name}.gltf`)).scene; m.position.set(x, 0, z); m.scale.setScalar(s); m.rotation.y = ry; m.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; }); scene.add(m); return m; }
const lamp = await prop('desk_lamp_arm_01', -.347, .51, .55, -.76);
lamp.traverse(o => { if (o.isMesh && o.material.name.includes('light')) { o.material = o.material.clone(); o.material.emissive = new THREE.Color('#ffd9a0'); o.material.emissiveIntensity = 6; } });
const tea = await prop('tea_set_01', 0, 0, 1, 0);
{ const keep = { tea_set_01_cup_small_01: [.36, .5, 2.2], tea_set_01_saucer_circular_04: [.36, .5, 0] }, dead = [];
  tea.traverse(o => { if (!o.name.startsWith('tea_set_01_')) return; const k = keep[o.name]; if (!k) dead.push(o); else { o.position.x = k[0]; o.position.z = k[1]; o.rotation.y = k[2]; } });
  dead.forEach(o => o.parent && o.parent.remove(o)); }
{ // pencil
  const g = new THREE.Group(), M = c => new THREE.MeshStandardMaterial({ color: c, roughness: .5 });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(.0038, .0038, .15, 6), M('#7fb08f')), wood = new THREE.Mesh(new THREE.CylinderGeometry(.0038, .0008, .018, 6), M('#e8c79a'));
  wood.position.y = .084; g.add(body, wood); g.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; });
  g.rotation.set(0, .5, Math.PI / 2); g.position.set(-.1, .0038, .52); scene.add(g);
}

// ---------- book ----------
const cover = coverCanvases((x, px, py, w, h) => { const c = cv(TU_W, TU_H); drawTunas(c.getContext('2d'), { expr: 'senang' }); x.drawImage(c, px + w * .05, py + h * .1, w * .9, h * .9 * TU_H / TU_W * .8); });
const book = makeBook(cover); scene.add(book.root);
const S = book.stage, K = book.sky;
const PGS = P2.pages(), PT = {}; for (const k in PGS) PT[k] = texOf(PGS[k]);

// ---------- timeline: one segment per spread; turns, white flashes, open and close between them ----------
const OPEN = [3.0, 5.2], CLOSE = [198, 201], DUR = 206;
const SEG = [
  { k: 'bed', sky: PT.bedSky, ground: PT.bedGround, t0: 0, t1: 52, exit: 'turn' },
  { k: 'road', sky: PT.roadSky, ground: PT.roadGround, t0: 54.6, t1: 74, exit: 'turn' },
  { k: 'wait', sky: PT.waitSky, ground: PT.waitGround, t0: 76.6, t1: 92, exit: 'turn' },
  { k: 'doc', sky: PT.docSky, ground: PT.docGround, t0: 94.6, t1: 122, exit: 'flash' },
  { k: 'body', sky: PT.bodySky, ground: PT.bodyGround, t0: 122, t1: 150, enter: 'flash', exit: 'flash' },
  { k: 'docB', sky: PT.docSky, ground: PT.docGround, t0: 150, t1: 160, enter: 'flash', exit: 'turn' },
  { k: 'night', sky: PT.nightSky, ground: PT.nightGround, t0: 162.6, t1: 170, exit: 'turn' },
  { k: 'recap', sky: PT.recapSky, ground: PT.recapGround, t0: 172.6, t1: 194.5, exit: 'close' },
];
const SI = Object.fromEntries(SEG.map((s, i) => [s.k, i]));
const TURNS = []; SEG.forEach((s, i) => { if (s.exit === 'turn') TURNS.push({ from: i, to: i + 1, a: s.t1, b: SEG[i + 1].t0 }); });
const FLASH = [121.4, 149.4];   // white peaks at +0.6
function segAt(t) { let i = 0; for (let j = 0; j < SEG.length; j++) { const s = SEG[j], prev = SEG[j - 1]; const start = j === 0 ? -1 : (prev.exit === 'turn' ? prev.t1 + .45 : s.t0); if (t >= start) i = j; } return i; }

// ---------- pop-up pieces ----------
const POPS = [];
function popper(seg, parent, item, x, y, z, o = {}) {
  const g = new THREE.Group(); g.position.set(x, y, z); const m = cutMesh(item, o); g.add(m); parent.add(g);
  const r = { g, m, seg: SI[seg], x, y, z, d: o.d ?? (.3 - z) * 1.1, dir: o.dir ?? 1, sway: o.sway || 0, ph: x * 40, t0: o.t0, tf: o.tf, rise: o.rise };
  POPS.push(r); return r;
}
function riseOf(r, t) {
  const s = SEG[r.seg];
  if (r.rise) return r.rise(t);
  const enterFlash = s.enter === 'flash';
  const t0 = r.t0 ?? (enterFlash ? s.t0 - 1 : (r.seg === 0 ? 5.4 : s.t0 + .2) + r.d * .9);
  const tf = r.tf ?? (s.exit === 'flash' ? 1e9 : s.t1 - .5 + (.3 - r.z) * .6);
  const end = s.exit === 'flash' ? s.t1 : 1e9;
  if (t < (enterFlash ? s.t0 : -1) || t >= end) return 0;
  return Math.min(back(seg(t, t0, t0 + .55), 1.7), 1 - ss(seg(t, tf, tf + .4)));
}
const nf = { tf: 1e9 };

// bedroom
popper('bed', K, P2.bedWindow(.08), .06, .25, .004, { d: .2 });
const CURT = popper('bed', K, P2.curtain(.045), .04, .255, .007, { d: .25 });
popper('bed', K, P2.frame(.04), -.12, .14, .004, { d: .3 });
popper('bed', K, A.flower(.03, '#ff9ec1', 41), .19, .02, .004, { d: .3 });
popper('bed', S, P2.bed(.13), -.12, 0, .125);
popper('bed', S, P2.breakfastTable(.1), .14, 0, .085);
popper('bed', S, A.bush(.045, .022, '#7cc35e', '#5aa543', 33), .19, 0, .2, { dir: -1 });
const WORRY = popper('bed', S, PR.worry(.03), 0, 0, 0, { t0: 28.2, tf: 35.0 });
const HEART = popper('bed', S, PR.heart(.015), 0, 0, 0, { t0: 48.7, tf: 51.2 });

// the journey: pieces pop up just ahead of the car and fold flat once it has passed
const CAR_T = [55.4, 68.0], CAR_X = [-.27, .06];
const carX = t => lerp(CAR_X[0], CAR_X[1], eio(seg(t, ...CAR_T))) + (t > 68.6 ? lerp(0, .03, ss(seg(t, 68.6, 69.6))) : 0);
const ahead = (x, keep) => t => { const cx = carX(t), up = cx > x - .12 ? back(seg(cx, x - .12, x - .06), 1.6) : 0, dn = keep ? 0 : ss(seg(cx, x + .1, x + .16)); return t < SEG[1].t0 + .1 || t > SEG[1].t1 - .3 ? Math.min(up, 1 - ss(seg(t, SEG[1].t1 - .5, SEG[1].t1 - .1))) * (t < SEG[1].t0 + .1 ? 0 : 1) : Math.min(up, 1 - dn); };
for (const [x, z, h, col] of [[-.17, .03, .13, '#9fd18a'], [-.09, .045, .1, '#b5e39a'], [.02, .03, .12, '#a9dd8c']]) popper('road', S, P2.mountain(h * 1.4, h, col, x * 100), x, 0, z, { rise: ahead(x) });
popper('road', S, P2.cow(.04), -.13, 0, .13, { rise: ahead(-.13) });
popper('road', S, P2.chicken(.025), -.06, 0, .14, { rise: ahead(-.06) });
popper('road', S, P2.chicken(.02), -.04, 0, .15, { rise: ahead(-.04) });
popper('road', S, PR.rumah(.06), .0, 0, .08, { rise: ahead(.0) });
popper('road', S, P2.warung(.07), .07, 0, .09, { rise: ahead(.07) });
popper('road', S, A.lolliTree(.07, '#5cbf4a', '#3f9934', 21), -.02, 0, .06, { rise: ahead(-.02), sway: .03 });
popper('road', S, A.lolliTree(.06, '#6fcc55', '#4ea93e', 22), .11, 0, .07, { rise: ahead(.11), sway: .03 });
popper('road', S, P2.hospital(.15, .17), .145, 0, .04, { rise: t => (t > 68.6 && t < SEG[1].t1) ? Math.min(back(seg(t, 68.6, 69.3), 1.7), 1 - ss(seg(t, SEG[1].t1 - .5, SEG[1].t1 - .1))) : 0 });
for (const [cx, cy, w] of [[-.12, .24, .07], [.06, .26, .055]]) popper('road', K, A.cloud(w, cx * 100), cx, cy, .006, { d: 1 });
const CAR = popper('road', S, P2.car(.075), -.27, 0, .2, { rise: t => (t > SEG[1].t0 + .3 && t < SEG[1].t1) ? Math.min(back(seg(t, SEG[1].t0 + .3, SEG[1].t0 + .8)), 1 - ss(seg(t, SEG[1].t1 - .5, SEG[1].t1 - .1))) : 0 });

// waiting room
popper('wait', K, P2.poster(.05, ['Cuci', 'tangan'], 'hands'), -.16, .24, .004, { d: .2 });
popper('wait', K, P2.clock(.035), -.03, .26, .004, { d: .25 });
popper('wait', K, P2.signBoard(.1, 'Poli Anak'), .1, .275, .004, { d: .2 });
const DISP = [popper('wait', K, P2.display(.05, 'A07'), .12, .2, .006, { d: .3, tf: 87.0 }), popper('wait', K, P2.display(.05, 'A08'), .12, .2, .007, { t0: 87.0 })];
popper('wait', S, P2.chairs(.14), -.13, 0, .075);
popper('wait', S, P2.deskCounter(.11), .12, 0, .1);
const BIRD = [true, false].map(up => { const g = new THREE.Group(); g.add(cutMesh(P2.shadowBird(.07, up), { shadow: false })); g.visible = false; K.add(g); return g; });

// doctor's room (twice: before and after the body world)
for (const k of ['doc', 'docB']) {
  popper(k, K, P2.heightChart(.17), -.17, .21, .004, { d: .2 });
  popper(k, K, P2.bedWindow(.07), .1, .25, .004, { d: .25 });
  popper(k, K, P2.signBoard(.11, 'Dokter Anak'), -.04, .275, .004, { d: .2 });
  popper(k, S, P2.examBed(.12), .13, 0, .075);
}
const DUG = popper('doc', S, P2.bubble(.05, 'dug… dug…'), .015, .07, .17, { t0: 99.0, tf: 102.4 });
const STK = popper('docB', S, P2.sticker(.008), .016, .014, .172, { t0: 151.4 });

// body world
const PJ = [[-.05, .14], [.01, .16], [.06, .13], [.12, .155]].map(([x, z], i) => {
  const r = popper('body', S, P2.penjaga(.032), x, 0, z); const brave = cutMesh(P2.penjaga(.032, true)); brave.visible = false; r.g.add(brave); r.brave = brave; r.base = [x, z]; return r; });
const SGERM = [[.06, -.12, .14], [.075, -.17, .12]].map(([y, x, z], i) => { const g = new THREE.Group(); g.add(cutMesh(P2.sleepyGerm(.03))); g.position.set(-.35, y, z); S.add(g); return { g, y, x, z, i }; });
const POST = popper('body', K, P2.posterIngat(.07, P2.sleepyGerm(.03).c), 0, .12, .006, { t0: 135.0 });
const SIGN = popper('body', S, P2.textCard(.06, 'suatu hari…'), -.02, 0, .215, { t0: 140.5, tf: 145.0, dir: -1 });
const RGERM = (() => { const g = new THREE.Group(); g.add(cutMesh(germ(7))); g.position.set(.35, .03, .15); S.add(g); return g; })();

// night bedroom
popper('night', K, P2.bedWindow(.08, true), .06, .25, .004, { d: .2 });
popper('night', K, P2.frame(.04, true), -.12, .14, .004, { d: .3 });
popper('night', S, P2.bed(.13), -.12, 0, .125);

// recap: three memory cards on the INGAT YA! wall
const MEM = [1, 2, 3].map((i, k) => popper('recap', K, P2.memoryCard(.075, i), (k - 1) * .13, .118, .006, { t0: [173.6, 180.6, 187.6][k] }));

// ---------- characters ----------
const pen = makeTunas(.036), mama = makeAdult('mama', .064), papa = makeAdult('papa', .066), dok = makeAdult('dokter', .066), per = makeAdult('perawat', .066);
const CAST = { pen, mama, papa, dok, per };
for (const c of Object.values(CAST)) S.add(c.root, c.shadow);
function walkAt(t, a, b, x0, x1) { const u = seg(t, a, b), x = lerp(x0, x1, u); const moving = t > a && t < b; return { x, walk: (x - x0) / .012 * Math.PI, stride: moving ? 1 : 0 }; }
const blink = (t, o = 0) => ((t + o) % 3.7) < .13 ? 1 : 0;
const hop = (t, a, h = .006) => t > a && t < a + .4 ? Math.sin(Math.PI * (t - a) / .4) * h : 0;
const sway = (w, k = .25) => [Math.sin(w.walk) * k * w.stride, -Math.sin(w.walk) * k * w.stride];

function castAt(t) {
  const s = SEG[segAt(t)].k, out = {};
  if (s === 'bed') {
    if (t > 5.6) {   // Tunas: asleep behind the bed, wakes, hops out, walks to the table
      const asleep = t < 11.6, w = walkAt(t, 13.6, 15.2, -.04, .07);
      const x = t < 12 ? -.12 : t < 13 ? lerp(-.12, -.04, ss(seg(t, 12, 13))) : w.x, z = t < 12 ? .108 : t < 13 ? lerp(.108, .165, ss(seg(t, 12, 13))) : .165;
      const y = t < 12 ? .03 : t < 13 ? .03 * (1 - seg(t, 12, 13)) + Math.sin(Math.PI * seg(t, 12, 13)) * .015 : hop(t, 19.4) + hop(t, 19.9, .004) + hop(t, 48.6, .008);
      const expr = t < 28 ? 'senang' : t < 48.5 ? 'cemas' : 'lega';
      out.pen = { x, z, y, p: { walk: w.walk, stride: w.stride, ...(() => { const [l, r] = sway(w); return { armL: .35 + l, armR: .35 + r }; })(), expr, blink: asleep ? 1 : blink(t), hold: false } };
    }
    if (t > 6.2) {   // Papa: in from the right, opens the curtain, to the table, laughs at his odd sandals, back for the brave pose
      const w1 = walkAt(t, 6.4, 9.4, .27, .1), w2 = walkAt(t, 13.4, 14.8, .1, .17), w3 = walkAt(t, 42.6, 43.6, .17, .12);
      const w = t < 13 ? w1 : t < 42 ? w2 : w3, [l, r] = sway(w, .2);
      const up = (t > 9.4 && t < 10.8) || (t > 18.0 && t < 20.4) || (t > 43.6 && t < 47.5);
      out.papa = { x: w.x, z: .15, y: hop(t, 18.4, .005) + hop(t, 19.0, .004) + hop(t, 43.8, .005), p: { walk: w.walk, stride: w.stride, armL: up ? 2.4 : .12 + l, armR: up ? 2.4 : .12 + r, sandals: true, blink: blink(t, 1.3), look: t > 21 && t < 42 ? -.6 : 0 } };
    }
    if (t > 20.6) {  // Mama: in from the left, says it plainly, then the hug
      const w = walkAt(t, 20.8, 23.4, -.26, .02), hugU = ss(seg(t, 35.2, 36.2));
      out.mama = { x: lerp(w.x, .062, hugU), z: lerp(.15, .156, hugU), p: { walk: w.walk + Math.PI, stride: w.stride, armL: .12, armR: .12, reachR: t > 23.6 && hugU === 0 ? [lerp(80, 260, seg(t, 23.6, 24.4)), lerp(380, 460, seg(t, 23.6, 24.4))] : null, hug: hugU, look: .6, blink: blink(t, 2.1) } };
    }
  }
  if (s === 'wait') {
    const call = t > 87.4;
    out.per = { x: .12, z: .088, p: { armL: .12, armR: call ? 2.2 : .12, blink: blink(t, .7), look: -.5 } };
    out.mama = { x: -.05, z: .158, p: { reachL: [-150, 330], armR: .12, look: call ? .7 : -.4, blink: blink(t, 2.1) }, y: hop(t, 89.6, .003) };
    out.pen = { x: -.092, z: .17, y: hop(t, 81.2) + hop(t, 82.2, .004), p: { armL: .35, armR: 1.0, expr: t > 79.6 && t < 88.6 ? 'senang' : 'cemas', blink: blink(t) } };
    const up = t > 79.6 && t < 85.6;
    out.papa = { x: .02, z: .15, p: { armL: up ? 2.3 : .12, armR: up ? 2.3 : .12, blink: blink(t, 1.3), sandals: false } };
  }
  if (s === 'doc') {
    const re = ss(seg(t, 102.6, 104.0));
    out.dok = { x: lerp(.035, .13, re), z: lerp(.15, .12, re), p: { steth: re < .5, reachL: re < .5 ? [-200, 240] : null, armL: .12, armR: .12, blink: blink(t, .4), look: -.4 } };
    const cus = 112.0, expr = t < 103 ? (t > 99 && t < 103 ? 'lega' : 'senang') : t < cus ? 'cemas' : t < cus + 2.2 ? 'meringis' : t < 117.8 ? 'cemas' : 'lega';
    out.pen = { x: -.02, z: .166, y: hop(t, 99.4, .004), p: { armL: .35, armR: .35, expr, blink: blink(t), plaster: seg(t, 113.0, 113.5), tear: t > cus + .3 ? seg(t, cus + .3, cus + 3) : 0 } };
    out.mama = { x: lerp(-.08, -.024, re), z: lerp(.14, .156, re), p: { hug: ss(seg(t, 103.6, 104.4)), look: .6, blink: blink(t, 2.1) } };
    out.papa = { x: lerp(-.135, .028, re), z: lerp(.13, .15, re), p: { reachL: re > .9 ? [-210, 300] : null, armL: .12, armR: .12, blink: blink(t, 1.3), look: re > .5 ? -.6 : .4 } };
  }
  if (s === 'docB') {
    out.dok = { x: .1, z: .13, p: { sticker: t < 151.4, reachL: t < 151.6 ? [-180, 200] : null, armL: .12, armR: .12, blink: blink(t, .4), look: -.4 } };
    out.pen = { x: 0, z: .168, y: hop(t, 152.8, .008) + hop(t, 153.4, .005), p: { armL: t > 152.6 && t < 154 ? 2.0 : .35, armR: t > 152.6 && t < 154 ? 2.0 : .35, expr: 'lega', plaster: 1, blink: 0 } };
    out.mama = { x: -.006, z: .157, p: { hug: 1, look: .6, blink: blink(t, 2.1) } };
    out.papa = { x: .045, z: .15, p: { reachL: [-200, 300], armR: .12, blink: blink(t, 1.3), look: -.6 } };
  }
  if (s === 'night') {
    out.pen = { x: -.05, z: .165, y: hop(t, 163.6, .005), p: { armL: .35, armR: 1.2, expr: 'lega', plaster: 1, blink: 0 } };
    out.mama = { x: .025, z: .152, p: { reachL: [-150, 330], armR: .12, look: -.6, blink: blink(t, 2.1) } };
  }
  if (s === 'recap') {
    out.mama = { x: -.065, z: .13, y: hop(t, 174.0, .004), p: { armL: .12, armR: t > 174 && t < 176 ? 1.6 : .12, look: .3, blink: blink(t, 2.1) } };
    out.papa = { x: .065, z: .13, y: hop(t, 181.0, .004), p: { armL: t > 181 && t < 183 ? 1.6 : .12, armR: .12, look: -.3, blink: blink(t, 1.3), sandals: false } };
    out.pen = { x: 0, z: .15, y: hop(t, 188.0, .006) + hop(t, 192.4, .01), p: { armL: t > 192.2 ? 2.2 : .35, armR: t > 192.2 ? 2.2 : .35, expr: 'senang', plaster: 1, blink: blink(t) } };
  }
  return out;
}

// ---------- lights ----------
const sun = new THREE.DirectionalLight('#fff3e0', 2.4); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -.0001; sun.shadow.normalBias = .0004; sun.shadow.radius = 4;
Object.assign(sun.shadow.camera, { left: -.3, right: .3, top: .3, bottom: -.3, near: .1, far: 3 }); sun.position.set(-.35, .55, .75); sun.target.position.set(0, .05, .12); scene.add(sun, sun.target);
const hemi = new THREE.HemisphereLight('#cfe6ff', '#caa27a', .5); scene.add(hemi);
const lampLight = new THREE.PointLight('#ffcf94', .25, .8, 2); lampLight.position.set(-.28, .36, .44); scene.add(lampLight);

// ---------- camera: [t, px,py,pz, tx,ty,tz, fov, aperture]; a new list = a hard cut ----------
const WIDE = (t, f = 30) => [t, 0, .14, .62, 0, .08, .1, f, 2.2];
const roadKeys = []; for (let t = 55.4; t <= 68.01; t += 1.4) { const cx = Math.max(-.15, carX(t)); roadKeys.push([t, cx + .01, .075, .44, cx + .02, .045, .14, 30, 2.3]); }
const SH = [
  [[0, 0, .74, .16, 0, 0, .15, 32, 3], [3.0, 0, .72, .16, 0, 0, .15, 32, 3], [5.2, 0, .7, .18, 0, .02, .14, 32, 3], [9.0, .02, .12, .56, .02, .07, .11, 30, 2.3], [11.6, -.05, .07, .42, -.05, .045, .13, 30, 2.4], [13.4, .05, .07, .42, .05, .045, .14, 30, 2.4]],
  [[15.2, .11, .06, .4, .11, .042, .15, 30, 2.4], [20.4, .1, .06, .38, .1, .042, .15, 30, 2.4]],
  [[20.6, -.03, .075, .46, -.02, .045, .14, 30, 2.4], [24.0, .03, .065, .4, .04, .042, .155, 30, 2.4], [28.6, .05, .06, .37, .06, .04, .16, 30, 2.5]],
  [[28.8, .07, .036, .31, .07, .022, .165, 30, 2.8], [34.8, .07, .035, .295, .07, .022, .165, 30, 2.8]],
  [[35.0, .06, .058, .37, .06, .04, .16, 30, 2.5], [42.4, .07, .058, .37, .07, .04, .16, 30, 2.5]],
  [[42.6, .1, .062, .41, .1, .043, .155, 30, 2.4], [48.0, .09, .062, .41, .09, .043, .155, 30, 2.4], [51.4, ...WIDE(0).slice(1)]],
  [[52.0, 0, .14, .64, 0, .08, .1, 30, 1.8], [54.6, 0, .12, .58, 0, .07, .11, 30, 1.8], ...roadKeys],
  [[68.4, .13, .045, .42, .14, .085, .07, 30, 2.2], [73.6, .13, .042, .39, .14, .09, .07, 30, 2.2], [74.4, 0, .14, .64, 0, .08, .1, 30, 1.8], [76.6, 0, .12, .58, 0, .07, .11, 30, 1.8]],
  [[76.8, 0, .12, .56, 0, .07, .11, 30, 2.2], [79.4, -.05, .085, .45, -.05, .06, .12, 30, 2.3], [85.8, -.04, .085, .45, -.04, .06, .12, 30, 2.3], [87.2, .02, .08, .47, .04, .055, .12, 30, 2.3], [91.6, .02, .08, .47, .04, .055, .12, 30, 2.3]],
  [[92.0, 0, .14, .64, 0, .08, .1, 30, 1.8], [94.6, 0, .12, .58, 0, .07, .11, 30, 1.8], [96.4, -.005, .062, .39, -.005, .042, .155, 30, 2.4], [102.6, -.005, .062, .39, -.005, .042, .155, 30, 2.4], [104.6, -.01, .066, .41, -.01, .045, .15, 30, 2.4], [109.8, -.01, .066, .41, -.01, .045, .15, 30, 2.4]],
  [[110.0, -.02, .036, .31, -.02, .022, .166, 30, 2.8], [119.2, -.02, .035, .295, -.02, .022, .166, 30, 2.8], [121.6, -.006, .03, .205, -.009, .027, .17, 30, 3.2]],
  [[122.0, -.04, .05, .3, -.04, .03, .15, 30, 2.6], [124.6, 0, .09, .46, 0, .05, .12, 30, 2.3], [127.0, -.07, .07, .42, -.07, .05, .13, 30, 2.3], [133.8, -.04, .07, .42, -.04, .05, .13, 30, 2.3], [135.4, 0, .1, .47, 0, .085, .1, 30, 2.3], [140.0, 0, .1, .47, 0, .085, .1, 30, 2.3], [141.2, .05, .07, .44, .05, .05, .13, 30, 2.3], [149.6, .07, .07, .44, .07, .05, .13, 30, 2.3]],
  [[150.0, .0, .045, .28, .0, .033, .166, 30, 2.8], [152.4, .025, .062, .4, .025, .045, .15, 30, 2.4], [159.6, .02, .062, .4, .02, .045, .15, 30, 2.4]],
  [[160.0, 0, .14, .64, 0, .08, .1, 30, 1.8], [162.6, 0, .12, .58, 0, .07, .11, 30, 1.8], [164.0, -.03, .06, .38, -.03, .042, .15, 30, 2.4], [169.6, -.03, .06, .37, -.03, .042, .15, 30, 2.4]],
  [[170.0, 0, .14, .64, 0, .08, .1, 30, 1.8], [172.6, 0, .15, .62, 0, .13, .06, 30, 2.0], [173.8, -.03, .09, .44, -.03, .085, .06, 30, 2.4], [180.4, 0, .09, .44, 0, .085, .06, 30, 2.4], [187.4, .03, .09, .44, .03, .085, .06, 30, 2.4], [193.4, 0, .15, .62, 0, .13, .06, 30, 2.2], [198.0, 0, .72, .17, 0, 0, .15, 32, 3], [206, 0, .72, .17, 0, 0, .15, 32, 3]],
];
const SHOTS = SH.map(k => ({ t0: k[0][0], f: track(k.map(r => [r[0], r.slice(1)])) }));
function camAt(t) { let s = SHOTS[0]; for (const x of SHOTS) if (t >= x.t0) s = x; return s.f(t); }
cam.up.set(0, .7, -.7);

// ---------- lines (subtitles; voice comes later) ----------
const LINES = [
  [10.8, 'Pagi, Tunas!'], [15.8, 'Lho, kok sandalnya beda?'], [24.6, 'Hari ini, Tunas mau imunisasi.'], [30.4, 'Imunisasi... sakit nggak?'],
  [36.6, 'Sakit sebentar. Deg-degan, nggak apa-apa.'], [44.4, 'Papa dulu juga deg-degan, lho.'],
  [60.0, 'Wah, ada sapi!'], [70.2, 'Ini rumah sakit.'],
  [81.4, 'Ada burung!'], [87.6, 'Tunas!'],
  [95.8, 'Halo, Tunas. Mau dengar jantungmu?'], [104.6, 'Mama peluk Tunas. Papa pegang tangan Tunas.'], [113.6, 'Rasanya sakit sebentar. Boleh nangis.'],
  [123.4, 'Di dalam badan Tunas, ada penjaga.'], [128.4, 'Obatnya bawa kuman yang lemah. Penjaga belajar.'], [137.0, 'Kami ingat kamu!'], [142.6, 'Kuman datang? Penjaga sudah kenal. Badan Tunas kuat.'],
  [152.6, 'Tunas hebat!'], [164.0, 'Tadi Tunas berani.'],
  [174.2, 'Ingat ya! Imunisasi sakitnya sebentar. Boleh nangis.'], [181.2, 'Mama dan Papa selalu ada di dekatmu.'], [188.2, 'Imunisasi bantu penjaga kenal kuman. Badan jadi kuat!'],
];
const SUBS = LINES.map(([t0, s], i) => { let t1 = t0 + Math.max(2.0, s.length * .075 + 1.0); const nx = LINES[i + 1]; if (nx) t1 = Math.min(t1, nx[0] - .2); return { t0, t1, s }; });
function drawSubs(t, top = false) {
  const Y = top ? 120 : 1010;
  for (const { t0, t1, s } of SUBS) {
    const a = Math.min(seg(t, t0 - .15, t0 + .15), 1 - seg(t, t1, t1 + .3)); if (a <= 0) continue;
    OX.save(); OX.globalAlpha = a; OX.textAlign = 'center'; OX.font = '600 46px Fredoka'; OX.lineJoin = 'round';
    const w = OX.measureText(s).width + 70; OX.fillStyle = 'rgba(251,244,234,.88)'; OX.beginPath(); OX.roundRect(960 - w / 2, Y - 52, w, 76, 38); OX.fill();
    OX.fillStyle = '#4a3f35'; OX.fillText(s, 960, Y); OX.restore();
  }
}

// ---------- sound events (for mix.py later) ----------
const EV = [{ t: OPEN[0], type: 'creak' }, { t: OPEN[1] - .2, type: 'thump' }, { t: CLOSE[0], type: 'creak' }, { t: CLOSE[1] - .1, type: 'thump' }];
for (const tr of TURNS) EV.push({ t: tr.a + .45, type: 'page', d: tr.b - tr.a - .7 });
for (const f of FLASH) EV.push({ t: f, type: 'whoosh' });
LINES.forEach(([t0], i) => EV.push({ t: t0, type: 'voice', id: 'l' + i }));
EV.sort((a, b) => a.t - b.t);
window.EV = EV; window.DUR = DUR;

// ---------- render ----------
function place(c, st) {
  c.root.visible = c.shadow.visible = !!st; if (!st) return;
  c.pose(st.p); c.root.position.set(st.x, st.y || 0, st.z); c.shadow.position.set(st.x, .0004, st.z);
}
function setSpread(i, back) { book.groundMat.map = SEG[i].ground; book.groundMat.needsUpdate = true; book.backMat.map = SEG[back ?? i].sky; book.backMat.needsUpdate = true; }
window.render = t => {
  const open = t < CLOSE[0] ? eio(seg(t, ...OPEN)) : 1 - eio(seg(t, ...CLOSE));
  book.setOpen(Math.PI / 2 * open);
  const si = segAt(t), tr = TURNS.find(x => t >= x.a + .45 && t < x.b - .3);
  if (tr) {
    setSpread(tr.to, tr.from);
    book.leafFront.material.map = book.leafFront.material.emissiveMap = SEG[tr.from].ground; book.leafBack.material.map = book.leafBack.material.emissiveMap = SEG[tr.to].sky;
    book.leafFront.material.needsUpdate = book.leafBack.material.needsUpdate = true; book.setLeaf(eio(seg(t, tr.a + .45, tr.b - .3)));
  } else { setSpread(si); book.setLeaf(0); }
  for (const r of POPS) { const k = riseOf(r, t); r.g.visible = k > .002; if (!r.g.visible) continue; r.g.rotation.x = r.dir * (Math.PI / 2) * (1 - k); if (r.sway) r.m.rotation.z = Math.sin(t * 1.6 + r.ph) * r.sway * k; }
  // moving pieces
  CURT.g.position.x = lerp(.04, .095, ss(seg(t, 9.6, 10.8)));
  CAR.g.position.x = carX(t); CAR.g.position.y = Math.abs(Math.sin(t * 9)) * .0012 * (t > CAR_T[0] && t < CAR_T[1] ? 1 : 0);
  const ps = castAt(t).pen;
  if (ps) { WORRY.g.position.set(ps.x + .02, .05, ps.z - .004); HEART.g.position.set(ps.x - .013, .022, ps.z + .008); }
  // shadow bird on the waiting-room wall
  const bOn = t > 80.0 && t < 85.8, flap = Math.floor(t * 3) % 2;
  BIRD.forEach((g, i) => { g.visible = bOn && i === flap; g.position.set(lerp(-.13, .01, seg(t, 80, 85.8)), .14 + Math.sin(t * 3) * .006, .003); g.children[0].children.forEach(m => m.material.opacity = 1); });
  // body world: sleepy germs float in and away, the guards learn, then push the real germ out
  for (const g of SGERM) { const inn = eo(seg(t, 127 + g.i * .3, 131 + g.i * .3)), away = ss(seg(t, 135.6, 139)); g.g.visible = si === SI.body && t > 126.8 && t < 139.5; g.g.position.set(lerp(-.35, g.x, inn), g.y + Math.sin(t * 2 + g.i) * .004 + away * .2, g.z); }
  const gather = ss(seg(t, 129.6, 131.6)), line = ss(seg(t, 135.4, 136.6)), surround = ss(seg(t, 144.0, 145.4)), push = ss(seg(t, 146.0, 148.0));
  PJ.forEach((r, i) => {
    let [x, z] = r.base;
    x = lerp(x, [-.11, -.08, -.1, -.06][i], gather); z = lerp(z, [.12, .15, .17, .14][i], gather);
    x = lerp(x, [-.06, -.02, .02, .06][i], line); z = lerp(z, .15, line);
    x = lerp(x, [.06, .08, .14, .12][i], surround); z = lerp(z, [.13, .17, .13, .17][i], surround);
    x += push * .12; r.g.position.set(x, hop(t, 124.4 + i * .2, .006) + hop(t, 133 + i * .1, .008) + hop(t, 148.2 + i * .1, .01), z);
    r.brave.visible = t > 135.8; r.m.visible = !r.brave.visible;
  });
  RGERM.visible = si === SI.body && t > 141.8 && t < 148.4; RGERM.position.set(lerp(lerp(.35, .1, eo(seg(t, 142, 144))), .36, ss(seg(t, 146.2, 148.2))), .03 + Math.sin(t * 3) * .004, .15); RGERM.rotation.z = Math.sin(t * 4) * .2;
  // characters
  const cs = castAt(t), turning = TURNS.some(x => t >= x.a + .2 && t < x.b - .2);
  for (const [n, c] of Object.entries(CAST)) place(c, turning || t > 194.6 ? null : cs[n]);
  // camera
  const c = camAt(t); cam.position.set(c[0], c[1], c[2]); cam.fov = c[6]; cam.lookAt(c[3], c[4], c[5]); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  post.dof.focus = Math.hypot(c[0] - c[3], c[1] - c[4], c[2] - c[5]); post.dof.aper = c[7]; post.dof.maxCoc = 14;
  post.vig.uniforms.fade.value = 1; post.vig.uniforms.warm.value = SEG[si].k === 'night' ? .02 : .12;
  scene.environmentIntensity = SEG[si].k === 'night' ? .3 : .45; scene.backgroundIntensity = .75;
  scene.updateMatrixWorld(true); post.composer.render();
  OX.clearRect(0, 0, W, H); drawSubs(t, SEG[si].k === 'recap');
  for (const f of FLASH) { const a = Math.min(seg(t, f, f + .6), 1 - seg(t, f + .6, f + 1.4)); if (a > 0) { OX.fillStyle = `rgba(255,253,247,${a})`; OX.fillRect(0, 0, W, H); } }
  if (t > 201.2) { const a = ss(seg(t, 201.2, 202.2)); OX.save(); OX.globalAlpha = a; OX.fillStyle = 'rgba(251,244,234,.92)'; OX.beginPath(); OX.roundRect(1240, 800, 600, 200, 40); OX.fill(); OX.textAlign = 'center'; OX.fillStyle = '#7a6c5f'; OX.font = '700 40px Fredoka'; OX.fillText('Cerita berikutnya', 1540, 870); OX.fillStyle = '#c46040'; OX.font = '700 70px Fredoka'; OX.fillText('Tunas Sikat Gigi', 1540, 950); OX.restore(); }
  if (t > DUR - 1.2) { OX.fillStyle = `rgba(0,0,0,${seg(t, DUR - 1.2, DUR)})`; OX.fillRect(0, 0, W, H); }
};
window.render(Number(Q.get('t') || 0));
window.__dbg = () => { const b = new THREE.Box3().setFromObject(book.root); return { per: [per.root.visible, per.root.position.toArray(), per.body.children[0].material.map.image.width], cam: cam.position.toArray(), up: cam.up.toArray(), fov: cam.fov, aspect: cam.aspect, bmin: b.min.toArray(), bmax: b.max.toArray() }; };
window.READY = true;
