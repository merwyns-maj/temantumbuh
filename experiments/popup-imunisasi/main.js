// "Tunas Mau Imunisasi" in the paper pop-up book style (engine: Lemo-Opuscar paper-popup, MIT). 42 s, two spreads.
import * as THREE from 'three';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { clamp, lerp, seg, ss, eio, back, spring, track, TAU } from './lib.js';
import * as A from './art.js';
import { makeBook, coverCanvases, texOf, PG } from './book.js';
import { cutMesh, thread } from './cutmesh.js';
import { makePost } from './post.js';
import { makeTunas, makeAdult, germ, drawTunas, TU_W, TU_H } from './chars.js';
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
const PGS = PR.pages(), PT = {}; for (const k in PGS) PT[k] = texOf(PGS[k]);
const SPREAD = [{ sky: PT.sky0, ground: PT.ground0 }, { sky: PT.sky1, ground: PT.ground1 }];
const OPEN = [2.4, 4.6], TURN = [22.6, 25.2], DUR = 42;
const RISE = [5.0, TURN[1] - .7], FOLD = [TURN[0], 1e9];

// pop-up pieces: rise back to front with overshoot, fold before the turn
const POPS = [];
function popper(spread, parent, item, x, y, z, o = {}) {
  const g = new THREE.Group(); g.position.set(x, y, z); const m = cutMesh(item, o); g.add(m); parent.add(g);
  const r = { g, m, spread, d: o.d ?? (.3 - z) * 1.1, dir: o.dir ?? 1, sway: o.sway || 0, ph: x * 40, t0: o.t0, tf: o.tf, pop: true };
  POPS.push(r); return r;
}
function riseOf(r, t) {
  const t0 = r.t0 ?? RISE[r.spread] + r.d, tf = r.tf ?? FOLD[r.spread] + (.3 - r.g.position.z) * .6;
  return Math.min(back(seg(t, t0, t0 + .55), 1.7), 1 - ss(seg(t, tf, tf + .4)));
}
const S = book.stage, K = book.sky;
// spread 0: home on the left, path, puskesmas on the right
popper(0, S, A.hill(.24, .06, '#b5e39a', '#93cc78', 11, { bumps: 2 }), -.12, 0, .012);
popper(0, S, A.hill(.24, .055, '#a9dd8c', '#88c46c', 12, { bumps: 3 }), .1, 0, .014);
popper(0, S, A.lolliTree(.07, '#5cbf4a', '#3f9934', 21), -.2, 0, .05, { sway: .03 });
popper(0, S, PR.rumah(.062), -.15, 0, .07);
popper(0, S, A.lolliTree(.055, '#6fcc55', '#4ea93e', 22), -.04, 0, .06, { sway: .03 });
popper(0, S, PR.puskesmas(.15, .1), .13, 0, .045);
popper(0, S, A.flower(.022, '#ff9ec1', 31), -.08, 0, .21, { dir: -1 });
popper(0, S, A.flower(.018, '#ffe066', 32), .02, 0, .22, { dir: -1 });
popper(0, S, A.bush(.05, .022, '#7cc35e', '#5aa543', 33), .17, 0, .22, { dir: -1 });
popper(0, S, A.fence(.06, .016), -.11, 0, .11);
const SUN = popper(0, K, A.sunOnStick(.022, .02), .14, .19, .006, { d: .9 });
for (const [cx, cy, w] of [[-.12, .22, .07], [.02, .25, .055]]) popper(0, K, A.cloud(w, cx * 100), cx, cy, .006, { d: 1 });
// spread 1: the clinic room
popper(1, K, PR.poster(.05), -.11, .2, .004, { d: .1 });
{ const win = A.cut(.08, .07, (x, W2, H2) => { x.beginPath(); x.roundRect(0, 0, W2, H2, 14); x.fillStyle = '#bfe0f2'; x.fill(); x.lineWidth = 9; x.strokeStyle = '#3a2a24'; x.stroke(); x.beginPath(); x.moveTo(W2 / 2, 0); x.lineTo(W2 / 2, H2); x.moveTo(0, H2 / 2); x.lineTo(W2, H2 / 2); x.stroke(); }, { ay: 0 }); popper(1, K, win, .1, .21, .004, { d: .2 }); }
popper(1, S, A.flower(.03, '#ff9ec1', 41), .18, 0, .06, { sway: .02 });
popper(1, S, PR.stool(.05), .14, 0, .09);
const SHIELD = popper(1, S, PR.shield(.085), 0, 0, .13, { t0: 31.0, tf: 1e9 });
const WORRY = popper(0, S, PR.worry(.03), 0, 0, 0, { t0: 14.4, tf: 19.9 });
const HEART = popper(0, S, PR.heart(.015), 0, 0, 0, { t0: 20.3, tf: 22.2 });
const BURST = popper(1, S, PR.burst(.024), .02, .025, .175, { t0: 27.8, tf: 28.5 });

// germs hanging on threads, dropping in and bouncing off the shield
const GERMS = [-.058, .06, .052].map((gx2, i) => { const g = new THREE.Group(); g.add(cutMesh(germ(60 + i))); const th = thread(.25); g.add(th); g.position.set(gx2, .3, .14 + i * .005); S.add(g); return { g, x: gx2, t0: 32.4 + i * .5, y: [.06, .075, .035][i] }; });

// ---------- characters ----------
const tun = makeTunas(.036), mama = makeAdult('mama', .064), bidan = makeAdult('bidan', .062);
for (const c of [tun, mama, bidan]) S.add(c.root, c.shadow);

const BEAT = 60 / 90;
function walkAt(t, a, b, x0, x1) { const u = seg(t, a, b), x = lerp(x0, x1, u); const moving = t > a && t < b; return { x, walk: (x - x0) / .012 * Math.PI, stride: moving ? 1 : 0 }; }
const blinkAt = t => { for (const b of [3.3, 9.1, 15.6, 21.0, 26.2, 33.5, 39.4]) if (t >= b && t < b + .14) return 1; return 0; };

function tunasState(t) {
  if (t < TURN[0] + .4) {
    const w = walkAt(t, 6.8, 13.6, -.17, .07);
    const worried = t > 14.2 && t < 20.6, holding = t > 19.8;
    return { x: w.x, z: .16, p: { walk: w.walk, stride: w.stride, armL: holding ? 1.0 : .35 + Math.sin(w.walk) * .25 * w.stride, armR: .35 - Math.sin(w.walk) * .25 * w.stride, expr: worried && !(t > 20.6) ? 'cemas' : 'senang', blink: blinkAt(t) } };
  }
  const cus = 27.8, hug = t > 36.4;
  const expr = t < cus ? 'cemas' : t < cus + 1.8 ? 'meringis' : hug ? 'lega' : 'senang';
  return { x: 0, z: .165, p: { armL: hug ? .9 : 1.0, armR: .4, expr, blink: blinkAt(t), plaster: seg(t, 28.0, 28.5), tear: t > cus + .3 ? seg(t, cus + .3, cus + 3.0) : 0 } };
}
function mamaState(t) {
  if (t < TURN[0] + .4) {
    const w = walkAt(t, 6.9, 13.6, -.19, .05);
    const reach = seg(t, 19.6, 20.3);
    return { x: w.x, z: .155, p: { walk: w.walk + Math.PI, stride: w.stride, armL: .12 - Math.sin(w.walk) * .2 * w.stride, armR: .12 + Math.sin(w.walk) * .2 * w.stride, reachR: reach > 0 ? [lerp(80, 300, reach), lerp(380, 520, reach)] : null, look: t > 14 ? .6 : 0 } };
  }
  const hugU = ss(seg(t, 36.4, 37.2));
  return { x: lerp(-.026, -.018, hugU), z: lerp(.155, .168, hugU), p: { reachR: hugU > 0 ? [lerp(420, 520, hugU), lerp(520, 640, hugU)] : [420, 520], reachL: hugU > 0 ? [lerp(-60, 260, hugU), lerp(400, 600, hugU)] : null, look: .6 } };
}
function bidanState(t) {
  if (t < TURN[1] - .3 || t > 36.4) return null;
  const inn = walkAt(t, 25.3, 26.6, .2, .055), out = walkAt(t, 34.4, 36.2, .055, .24);
  const w = t < 34.4 ? inn : out, sting = seg(t, 27.4, 27.8) * (1 - seg(t, 28.2, 28.8));
  return { x: w.x, z: .158, p: { walk: w.walk, stride: w.stride, armL: .12, armR: .12, reachR: t < 30.5 ? [lerp(-60, -150, sting), lerp(280, 330, sting)] : null, cotton: true, look: -.6 } };
}

// ---------- lights ----------
const sun = new THREE.DirectionalLight('#fff3e0', 2.4); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -.0001; sun.shadow.normalBias = .0004; sun.shadow.radius = 4;
Object.assign(sun.shadow.camera, { left: -.3, right: .3, top: .3, bottom: -.3, near: .1, far: 3 }); sun.position.set(-.35, .55, .75); sun.target.position.set(0, .05, .12); scene.add(sun, sun.target);
const hemi = new THREE.HemisphereLight('#cfe6ff', '#caa27a', .5); scene.add(hemi);
const lampLight = new THREE.PointLight('#ffcf94', .25, .8, 2); lampLight.position.set(-.28, .36, .44); scene.add(lampLight);

// ---------- camera: [px,py,pz, tx,ty,tz, fov, aperture] per shot; a new list = a hard cut ----------
const SH = [
  [[0, .02, .52, 1.15, -.02, .06, .2, 34, 3.0], [2.4, .0, .36, .95, 0, .07, .16, 32, 2.8], [4.6, .0, .22, .72, 0, .08, .13, 30, 2.4], [6.6, -.06, .1, .52, -.06, .05, .14, 30, 2.2]],
  [[6.6, -.13, .062, .42, -.13, .037, .155, 30, 2.4], [13.6, .06, .062, .42, .065, .04, .155, 30, 2.4]],
  [[13.8, .1, .05, .33, .07, .036, .16, 30, 2.6], [19.2, .098, .048, .31, .07, .036, .16, 30, 2.6]],
  [[19.3, .05, .052, .37, .05, .036, .16, 30, 2.4], [22.5, .045, .056, .38, .045, .038, .16, 30, 2.4]],
  [[22.6, .0, .14, .64, 0, .08, .1, 30, 1.8], [25.2, .0, .12, .58, 0, .07, .11, 30, 1.8]],
  [[25.3, .015, .058, .42, .015, .038, .16, 30, 2.4], [30.7, .01, .054, .38, .01, .038, .16, 30, 2.5]],
  [[30.8, .0, .085, .5, 0, .05, .14, 30, 2.2], [36.2, .0, .08, .47, 0, .05, .14, 30, 2.2]],
  [[36.3, -.012, .055, .35, -.012, .036, .165, 30, 2.5], [38.8, -.012, .052, .32, -.012, .036, .165, 30, 2.5], [42, .0, .42, .98, 0, .05, .15, 32, 3.0]],
];
const SHOTS = SH.map(k => ({ t0: k[0][0], f: track(k.map(r => [r[0], r.slice(1)])) }));
function camAt(t) { let s = SHOTS[0]; for (const x of SHOTS) if (t >= x.t0) s = x; return s.f(t); }

// ---------- narration ----------
const VD = await (await fetch('voices/dur.json')).json();
const LINES = [['n1', 3.0, 'Hari ini, Tunas mau imunisasi.'], ['n2', 14.2, 'Tunas agak deg-degan. Nggak apa-apa.'], ['n3', 19.6, 'Mama pegang tangan Tunas.'],
  ['n4', 28.4, 'Rasanya sakit sebentar. Boleh nangis.'], ['n5', 31.6, 'Imunisasi bantu badan Tunas melawan kuman.'], ['n6', 37.4, 'Tunas hebat!']];
const SUBS = LINES.map(([id, t0, s], i) => { let t1 = Math.max(t0 + 1.8, t0 + VD.dur[id] + .6); const nx = LINES[i + 1]; if (nx) t1 = Math.min(t1, nx[1] - .2); return { t0, t1, s }; });
function drawSubs(t) {
  for (const { t0, t1, s } of SUBS) {
    const a = Math.min(seg(t, t0 - .15, t0 + .15), 1 - seg(t, t1, t1 + .3)); if (a <= 0) continue;
    OX.save(); OX.globalAlpha = a; OX.textAlign = 'center'; OX.font = '600 46px Fredoka'; OX.lineJoin = 'round';
    OX.shadowColor = 'rgba(0,0,0,.35)'; OX.shadowBlur = 16; OX.lineWidth = 9; OX.strokeStyle = 'rgba(40,26,18,.85)'; OX.strokeText(s, 960, 1010); OX.shadowBlur = 0; OX.fillStyle = '#fffaf0'; OX.fillText(s, 960, 1010); OX.restore();
  }
}

// ---------- sound events ----------
const EV = [{ t: OPEN[0], type: 'creak' }, { t: OPEN[1] - .2, type: 'thump' }, { t: TURN[0] + .45, type: 'page', d: TURN[1] - TURN[0] - .7 }, { t: 27.0, type: 'silence', dur: .8 }, { t: 27.8, type: 'cus' }, { t: 28.0, type: 'crinkle' }, { t: 31.0, type: 'reveal' }, { t: 36.9, type: 'puff' }, { t: 38.9, type: 'whoosh' }];
for (const r of POPS) { const t0 = r.t0 ?? RISE[r.spread] + r.d; if (t0 < DUR) EV.push({ t: +(t0 + .1).toFixed(3), type: 'pop' }); }
for (const g of GERMS) EV.push({ t: g.t0 + .9, type: 'boing' });
LINES.forEach(([id, t0]) => EV.push({ t: t0, type: 'voice', id }));
{ let prev = 0; for (let f = 0; f < DUR * 30; f++) { const t = f / 30, s = tunasState(t); const ph = s.p.walk || 0; if (s.p.stride && Math.floor(ph / Math.PI) !== Math.floor(prev / Math.PI)) EV.push({ t, type: 'step' }); prev = ph; } }
EV.sort((a, b) => a.t - b.t);
window.EV = EV; window.DUR = DUR;

// ---------- render ----------
const tmp = new THREE.Vector3();
const toScreen = v => { const p = v.clone().project(cam); return [(p.x * .5 + .5) * W, (-p.y * .5 + .5) * H]; };
function place(c, st, y = 0) {
  c.root.visible = c.shadow.visible = !!st; if (!st) return;
  c.pose(st.p); c.root.position.set(st.x, y, st.z); c.shadow.position.set(st.x, .0004, st.z);
}
window.render = t => {
  book.setOpen(Math.PI / 2 * eio(seg(t, ...OPEN)));
  const spread = t >= TURN[0] + .45 ? 1 : 0, turning = t >= TURN[0] + .45 && t < TURN[1] - .3;
  book.groundMat.map = SPREAD[spread].ground; book.groundMat.needsUpdate = true;
  book.backMat.map = SPREAD[turning ? 0 : spread].sky; book.backMat.needsUpdate = true;
  if (turning) {
    book.leafFront.material.map = book.leafFront.material.emissiveMap = SPREAD[0].ground; book.leafBack.material.map = book.leafBack.material.emissiveMap = SPREAD[1].sky;
    book.leafFront.material.needsUpdate = book.leafBack.material.needsUpdate = true; book.setLeaf(eio(seg(t, TURN[0] + .45, TURN[1] - .3)));
  } else book.setLeaf(0);
  for (const r of POPS) { const k = riseOf(r, t); r.g.visible = k > .002; if (!r.g.visible) continue; r.g.rotation.x = r.dir * (Math.PI / 2) * (1 - k); if (r.sway) r.m.rotation.z = Math.sin(t * 1.6 + r.ph) * r.sway * k; }
  SUN.g.position.y = .19 + Math.sin(t * .9) * .003;
  // characters
  const ts = tunasState(t), ms = mamaState(t), bs = bidanState(t);
  const before = t < TURN[0] + .45;
  place(tun, (t > 5.4 && (before ? t < TURN[0] + .2 : t > TURN[1] - .2)) ? ts : null);
  place(mama, (t > 5.6 && (before ? t < TURN[0] + .2 : t > TURN[1] - .2)) ? ms : null);
  place(bidan, bs);
  // worry cloud + heart follow Tunas' head; burst at his arm
  WORRY.g.position.set(ts.x + .02, .05, ts.z - .004); HEART.g.position.set(ts.x - .013, .022, ts.z + .008);
  // germs drop on their threads, bump the shield and go back up
  for (const g of GERMS) { const k = t - g.t0; g.g.visible = t > 31.5 && t < 37; const dn = k > 0 ? spring(k, 5, .45) : 0, up = ss(seg(t, g.t0 + 1.0, g.t0 + 2.2)); g.g.position.y = lerp(.3, g.y, dn) + up * .25; g.g.rotation.z = Math.sin(t * 3 + g.x * 50) * .15 + (k > .9 && k < 1.3 ? Math.sin((k - .9) * 30) * .3 : 0); }
  // camera
  const c = camAt(t); cam.position.set(c[0], c[1], c[2]); cam.fov = c[6]; cam.lookAt(c[3], c[4], c[5]); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  post.dof.focus = Math.hypot(c[0] - c[3], c[1] - c[4], c[2] - c[5]); post.dof.aper = c[7]; post.dof.maxCoc = 14;
  post.vig.uniforms.fade.value = 1; post.vig.uniforms.warm.value = .12;
  scene.environmentIntensity = .45; scene.backgroundIntensity = .75;
  scene.updateMatrixWorld(true); post.composer.render();
  OX.clearRect(0, 0, W, H); drawSubs(t);
  if (t < 1 || t > DUR - 1.2) { OX.fillStyle = `rgba(0,0,0,${1 - seg(t, 0, 1) * (1 - seg(t, DUR - 1.2, DUR))})`; OX.fillRect(0, 0, W, H); }
};
window.render(Number(Q.get('t') || 0));
window.READY = true;
