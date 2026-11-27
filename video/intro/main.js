// TemanTumbuh Series: the 20 s intro (sung jingle). Same paper pop-up world as the episodes.
// Song sections (all takes): 0–3.4 "Satu, dua, tiga!" · 3.4–10.4 verse · 10.4–16.8 hook "Tum-tum-tumbuh" · 16.8–20 "TemanTumbuh!"
import * as THREE from 'three';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { lerp, seg, ss, eio, eo, back, spring, track, TAU, mulberry } from './lib.js';
import * as A from './art.js';
import { cut } from './art.js';
import { makeBook, coverCanvases, texOf, BW, BD } from './book.js';
import { cutMesh } from './cutmesh.js';
import { makePost } from './post.js';
import { makeTunas, makeAdult, drawTunas, TU_W, TU_H } from './chars.js';
import { cv, sh, GRAIN, INK } from './paper.js';

const W = 1920, H = 1080, Q = new URLSearchParams(location.search), DUR = 20;
const BPM = Number(Q.get('bpm') || 115), BEAT = 60 / BPM;   // take B measures about 115 BPM
// word times in take B (from its transcript): Satu .2, dua 1.3, tiga 2.3 · Buka 4.5 · yuk kita baca 6.7 · Ada tunas 8.5 · ada cerita 9.4
// instrumental 10–12.2 · Tum tum tumbuh 12.2/12.8 · tunas tumbuh 13.4 · Tum tum tumbuh 14.7/14.9 · kita tumbuh 15.5 · TemanTumbuh (cast shout) 16.75
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setSize(W, H); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.NeutralToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
document.getElementById('stage').appendChild(renderer.domElement);
const ov = document.getElementById('ov'), OX = ov.getContext('2d');
const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(30, W / H, .004, 30);
const post = makePost(renderer, scene, cam, W, H);

await Promise.all(['600 40px Fredoka', '700 40px Fredoka', '40px "Lilita One"'].map(f => document.fonts.load(f)));
const hdr = await new RGBELoader().loadAsync('assets/room_2k.hdr'); hdr.mapping = THREE.EquirectangularReflectionMapping;
scene.environment = hdr; scene.background = hdr; scene.backgroundBlurriness = .35;
const tl = new THREE.TextureLoader();
const wt = n => { const t = tl.load(`assets/walnut_${n}.jpg`); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(2.2, 1.4); return t; };
const wd = wt('diff'); wd.colorSpace = THREE.SRGBColorSpace;
const desk = new THREE.Mesh(new THREE.BoxGeometry(2.6, .04, 1.7), new THREE.MeshStandardMaterial({ map: wd, normalMap: wt('nor'), roughnessMap: wt('rough'), color: '#c9a88a', envMapIntensity: .8 }));
desk.position.set(0, -.02, .25); desk.receiveShadow = true; scene.add(desk);
const gl = new GLTFLoader();
async function prop(name, x, z, s, ry) { const m = (await gl.loadAsync(`assets/${name}/${name}.gltf`)).scene; m.position.set(x, 0, z); m.scale.setScalar(s); m.rotation.y = ry; m.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; }); scene.add(m); return m; }
// the lamp stands back and to the left, so its shadow falls on the desk, not on the book's backdrop
const lamp = await prop('desk_lamp_arm_01', -.6, -.12, .55, -.4);
lamp.traverse(o => { if (o.isMesh && o.material.name.includes('light')) { o.material = o.material.clone(); o.material.emissive = new THREE.Color('#ffd9a0'); o.material.emissiveIntensity = 6; } });

// ---------- paper helpers ----------
const PW = 2048, PH = Math.round(2048 * BD / BW);
function page(fn) { const c = cv(PW, PH), x = c.getContext('2d'); fn(x); x.save(); x.globalAlpha = .7; x.fillStyle = x.createPattern(GRAIN, 'repeat'); x.fillRect(0, 0, PW, PH); x.restore(); return c; }
function grad(x, stops) { const g = x.createLinearGradient(0, 0, 0, PH); stops.forEach(([o, c]) => g.addColorStop(o, c)); x.fillStyle = g; x.fillRect(0, 0, PW, PH); }
const R = mulberry(11);
const skyPage = page(x => { grad(x, [[0, '#a9d8f2'], [.75, '#dff1f4'], [1, '#eef7e3']]);
  for (let i = 0; i < 7; i++) { const cx = R() * PW, cy = PH * (.08 + R() * .35); x.fillStyle = 'rgba(255,255,255,.6)'; for (let k = 0; k < 4; k++) { x.beginPath(); x.arc(cx + k * 64, cy + (k % 2) * 22, 74, 0, TAU); x.fill(); } }
  x.fillStyle = '#c6e6b0'; x.fillRect(0, PH * .88, PW, PH * .12); });
const meadowPage = page(x => { grad(x, [[0, '#93cf70'], [1, '#ade086']]);
  x.fillStyle = '#f6ecd2'; x.beginPath(); x.moveTo(PW * .42, PH); x.bezierCurveTo(PW * .44, PH * .7, PW * .56, PH * .62, PW * .5, PH * .45); x.lineTo(PW * .54, PH * .45); x.bezierCurveTo(PW * .62, PH * .62, PW * .54, PH * .74, PW * .6, PH); x.closePath(); x.fill();
  for (let i = 0; i < 220; i++) { const px = R() * PW, py = R() * PH; x.beginPath(); x.arc(px, py, 5 + R() * 7, 0, TAU); x.fillStyle = ['#ffffff', '#ffe066', '#ff9ec1', '#bfe0ff'][(R() * 4) | 0]; x.fill(); } });
const textPage = (seed) => { const r = mulberry(seed); return page(x => { x.fillStyle = '#fbf4e4'; x.fillRect(0, 0, PW, PH);
  x.fillStyle = 'rgba(90,70,55,.28)'; for (let j = 0; j < 9; j++) { const w = PW * (.55 + r() * .3); x.fillRect(PW * .12, PH * (.14 + j * .085), w, 22); }
  x.beginPath(); x.arc(PW * .78, PH * .72, 150, 0, TAU); x.fillStyle = ['#f3c45f', '#ef93a8', '#8fc4ea'][seed % 3]; x.fill(); }); };

// ---------- the big book: TemanTumbuh ----------
const icon = (x, px, py, w, h) => { const c = cv(TU_W, TU_H); drawTunas(c.getContext('2d'), { expr: 'senang' }); x.drawImage(c, px + w * .05, py + h * .1, w * .9, h * .9 * TU_H / TU_W * .8); };
const book = makeBook(coverCanvases(icon, { title: 'TemanTumbuh', sub: 'Series', foot: '~ buka, baca, tumbuh ~', tpx: 150, spx: 150, ink: '#fff3d6' }));
scene.add(book.root);
book.groundMat.map = texOf(meadowPage); book.backMat.map = texOf(skyPage); book.groundMat.needsUpdate = book.backMat.needsUpdate = true;
const S = book.stage, K = book.sky;

// ---------- three little books (next stories) that count, fly like birds and clap on the beat ----------
const LB = [['#d9734f', 'Cuci', 'Tangan'], ['#5a8fc4', 'Tanam', 'Biji'], ['#e3b23c', 'Takut', 'Gelap']].map(([bg, a, b], i) => {
  const bk = makeBook(coverCanvases(icon, { bg, title: a, sub: b, foot: 'TemanTumbuh', tpx: 230, spx: 200 }));
  bk.groundMat.map = texOf(textPage(i + 1)); bk.backMat.map = texOf(textPage(i + 4)); bk.groundMat.needsUpdate = bk.backMat.needsUpdate = true;
  const wrap = new THREE.Group(), roll = new THREE.Group(); bk.root.scale.setScalar(.36); roll.add(bk.root); wrap.add(roll); scene.add(wrap);
  return { bk, wrap, roll, i };
});
const HOME = [[-.28, .26, .25], [.28, .26, -.3], [.29, .05, .15]];     // x, z, yaw on the desk at the start
const LAND = [[-.34, .2, .2], [.34, .2, -.2], [.32, .02, .15]];    // where they sit during the hook (book 2 keeps circling)
const COUNT = [.12, 1.22, 2.22];                                      // "Satu", "dua", "tiga"

// ---------- pop-ups on the spread ----------
const POPS = [];
function pop(parent, item, x, y, z, rise, o = {}) { const g = new THREE.Group(); g.position.set(x, y, z); const m = cutMesh(item, o); g.add(m); parent.add(g); const r = { g, m, rise, dir: o.dir ?? 1, sway: o.sway || 0, ph: x * 40 }; POPS.push(r); return r; }
const FOLD = [18.55, 18.95];   // everything folds flat before the book closes
const upAt = (a, d = .55) => t => Math.min(back(seg(t, a, a + d), 1.7), 1 - ss(seg(t, ...FOLD)));
pop(S, A.hill(.26, .085, '#9fd18a', '#7fb86a', 3), -.1, 0, .025, upAt(5.7));
pop(S, A.hill(.24, .075, '#b5e39a', '#93c87a', 5, { dots: ['#ffffff', '#ffe066'] }), .11, 0, .035, upAt(5.85));
pop(S, A.lolliTree(.1, '#5cbf4a', '#3f9934', 21), -.175, 0, .075, upAt(6.0), { sway: .03 });
pop(S, A.lolliTree(.085, '#6fcc55', '#4ea93e', 22), .175, 0, .085, upAt(6.15), { sway: .03 });
pop(S, A.bush(.05, .026, '#7cc35e', '#5aa543', 33), -.13, 0, .215, upAt(6.3), { dir: -1 });
pop(S, A.bush(.045, .024, '#86cc66', '#62a94a', 34), .135, 0, .225, upAt(6.4), { dir: -1 });
for (const [cx, cy, w, sd] of [[-.12, .25, .075, 3], [.05, .275, .06, 7]]) pop(K, A.cloud(w, sd), cx, cy, .006, upAt(6.0));
const SUN = pop(K, A.sunOnStick(.026, .05), .15, .02, .005, upAt(5.6));
// flowers pop on the hook's beats
const FLW = [[-.07, .235, '#ff9ec1'], [.07, .24, '#ffffff'], [-.035, .262, '#ffe066'], [.04, .265, '#ff9ec1'], [-.105, .255, '#bfe0ff'], [.105, .25, '#ffe066'], [-.15, .26, '#ffffff'], [.15, .262, '#ff9ec1']];
FLW.forEach(([x, z, col], i) => pop(S, A.flower(.028 + (i % 3) * .004, col, 40 + i), x, 0, z, upAt(12.2 + i * BEAT * 1.2, .35), { dir: -1, sway: .05 }));
// the paper pot Tunas grows out of
const potItem = cut(.05, .036, (x, W2, H2) => {
  x.beginPath(); x.moveTo(W2 * .12, H2 * .22); x.lineTo(W2 * .88, H2 * .22); x.lineTo(W2 * .76, H2); x.lineTo(W2 * .24, H2); x.closePath(); sh(x, '#e07856', 9);
  x.beginPath(); x.roundRect(0, 0, W2, H2 * .26, 14); sh(x, '#f08a66', 9);
  x.beginPath(); x.ellipse(W2 * .5, H2 * .62, W2 * .12, H2 * .14, 0, 0, TAU); x.fillStyle = '#c96446'; x.fill();
}, { ay: 1 });
const POT = pop(S, potItem, 0, 0, .185, t => Math.min(back(seg(t, 7.7, 8.2), 1.7), 1 - ss(seg(t, 10.2, 10.6))));
// the banner: "TemanTumbuh Series"
const bannerItem = cut(.15, .055, (x, W2, H2) => {
  x.beginPath(); x.roundRect(0, 0, W2, H2, 40); sh(x, '#fffaf0', 10);
  x.beginPath(); x.roundRect(14, 14, W2 - 28, H2 - 28, 30); x.lineWidth = 6; x.strokeStyle = '#e0b456'; x.stroke();
  x.textAlign = 'center'; x.textBaseline = 'middle'; x.font = `${Math.round(H2 * .5)}px "Lilita One"`; x.lineWidth = 16; x.strokeStyle = '#fffaf0';
  x.fillStyle = '#3f6b52'; x.fillText('TemanTumbuh', W2 / 2, H2 * .42);
  x.font = `600 ${Math.round(H2 * .2)}px Fredoka`; x.fillStyle = '#c46040'; x.fillText('S E R I E S', W2 / 2, H2 * .8);
}, { ay: 1 });
const BANNER = pop(K, bannerItem, 0, .125, .01, t => Math.min(back(seg(t, 16.7, 17.15), 1.6), 1 - ss(seg(t, ...FOLD))));
// paper-leaf confetti
const LEAVES = []; { const r = mulberry(5); for (let i = 0; i < 46; i++) { const m = cutMesh(A.leafBit(['#6fbf5a', '#9fd18a', '#f3c45f', '#ef93a8', '#e07856'][i % 5]), { s: 1.3, shadow: false });
  scene.add(m); LEAVES.push({ m, vx: (r() - .5) * .4, vy: .08 + r() * .14, vz: .02 + r() * .08, spin: (r() - .5) * 18, t0: 16.8 + r() * .25 }); } }

// ---------- characters ----------
const tunas = makeTunas(.05), mama = makeAdult('mama', .07), papa = makeAdult('papa', .072);
for (const c of [tunas, mama, papa]) S.add(c.root, c.shadow);
const blink = (t, o = 0) => ((t + o) % 3.7) < .13 ? 1 : 0;
const hop = (t, a, h = .006, d = .4) => t > a && t < a + d ? Math.sin(Math.PI * (t - a) / d) * h : 0;
const beatPulse = (t, t0) => { if (t < t0) return 0; const u = ((t - t0) % BEAT) / BEAT; return Math.exp(-u * 6); };
// within each hook line: crouch small on "tum-tum", then grow tall on "tumbuh"
const HOOK = [[12.2, 12.8], [14.7, 14.95]];   // [first 'tum', 'tumbuh']
function hookShape(t) {
  for (const [a, g] of HOOK) { const u = t - a, gu = t - g; if (u < -.1 || gu > 1.6) continue;
    const crouch = Math.min(ss(seg(u, -.1, .12)), 1 - ss(seg(gu, -.08, .08))), grow = Math.min(back(seg(gu, 0, .3), 2), 1 - ss(seg(gu, 1.0, 1.5)));
    return { sy: 1 - .16 * crouch + .18 * grow, sx: 1 + .08 * crouch - .05 * grow, lift: grow * .008 + hop(t, a, .004, .25) + hop(t, (a + g) / 2, .004, .25) }; }
  return { sy: 1, sx: 1, lift: 0 };
}
function cast(t) {
  const out = {};
  if (t > 7.95 && t < FOLD[1]) {   // Tunas sprouts from the pot, hops out, waves, then leads the hook
    const grow = back(seg(t, 8.05, 8.85), 1.6), out_ = ss(seg(t, 9.9, 10.35)), sh_ = hookShape(t), tag = hop(t, 16.7, .02, .6) + hop(t, 13.4, .01, .45) + hop(t, 15.5, .012, .45);
    const fold = 1 - ss(seg(t, ...FOLD));
    out.tunas = { x: 0, z: lerp(.18, .205, out_), y: lerp(.03, 0, out_) + Math.sin(Math.PI * out_) * .012 + sh_.lift + tag, s: Math.max(.05, grow) * fold, sx: sh_.sx, sy: sh_.sy,
      p: { expr: 'senang', blink: blink(t), armL: t > 16.7 || (t > 13.4 && t < 14.0) ? 2.3 : .35, armR: (t > 10.35 && t < 11.1) || t > 16.7 || (t > 13.4 && t < 14.0) ? 2.4 : .35 } };
  }
  const unfold = (a) => back(seg(t, a, a + .6), 1.6) * (1 - ss(seg(t, ...FOLD)));
  if (t > 10.5) out.mama = { x: -.095, z: .17, rx: unfold(10.6), y: hop(t, 16.7, .012, .5) + hop(t, 15.5, .008, .45), p: { armL: .12, armR: t > 16.7 ? 2.4 : .12 + 1.9 * beatPulse(t, 11.4 + BEAT), look: .4, blink: blink(t, 2.1) } };
  if (t > 10.9) out.papa = { x: .095, z: .17, rx: unfold(11.1), y: hop(t, 16.75, .012, .5) + hop(t, 15.52, .008, .45), p: { armL: t > 16.7 ? 2.4 : .12 + 1.9 * beatPulse(t, 11.6), armR: .12, look: -.4, blink: blink(t, 1.3), sandals: true } };
  return out;
}
function place(c, st) {
  c.root.visible = c.shadow.visible = !!st && (st.s ?? 1) > .02 && (st.rx ?? 1) > .01; if (!c.root.visible) return;
  c.pose(st.p); c.root.position.set(st.x, st.y || 0, st.z); c.root.rotation.x = -(Math.PI / 2) * (1 - (st.rx ?? 1));
  const s = st.s ?? 1; c.root.scale.set(s * (st.sx || 1), s * (st.sy || 1), s); c.shadow.position.set(st.x, .0004, st.z); c.shadow.scale.setScalar(s);
}

// ---------- lights ----------
const sun = new THREE.DirectionalLight('#fff3e0', 2.4); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -.0001; sun.shadow.normalBias = .0004; sun.shadow.radius = 4;
Object.assign(sun.shadow.camera, { left: -.45, right: .45, top: .45, bottom: -.45, near: .1, far: 3 }); sun.position.set(-.3, .6, .8); sun.target.position.set(0, .05, .12); scene.add(sun, sun.target);
scene.add(new THREE.HemisphereLight('#cfe6ff', '#caa27a', .5));
const lampLight = new THREE.PointLight('#ffcf94', .25, .9, 2); lampLight.position.set(-.5, .36, .0); scene.add(lampLight);

// ---------- camera: [t, px,py,pz, tx,ty,tz, fov, aperture] ----------
const TOP = (t, h = .8) => [t, 0, h, .16, 0, 0, .15, 32, 3];
const CAM = track([
  TOP(0), TOP(5.6), [7.1, 0, .15, .6, 0, .085, .12, 30, 2.2], [7.7, 0, .14, .58, 0, .08, .12, 30, 2.2],
  [8.4, 0, .075, .42, 0, .05, .17, 30, 2.4], [10.2, 0, .08, .44, 0, .05, .17, 30, 2.4],
  [11.0, 0, .1, .52, 0, .06, .14, 30, 2.3], [14.0, .015, .1, .5, .01, .06, .145, 30, 2.3], [16.0, 0, .105, .52, 0, .062, .14, 30, 2.3],
  [16.7, 0, .13, .58, 0, .1, .11, 30, 2.2], [18.7, 0, .13, .58, 0, .1, .11, 30, 2.2], TOP(19.95, .74), TOP(20, .74),
].map(r => [r[0], r.slice(1)]));
cam.up.set(0, .7, -.7);

window.EV = [{ t: 4.4, type: 'creak' }, { t: 19.85, type: 'thump' }]; window.DUR = DUR;

// ---------- render ----------
window.render = t => {
  // the big book: a little jump on "tiga", opens on the verse, closes at the very end
  const open = t < 18.95 ? eio(seg(t, 4.4, 5.6)) : 1 - eio(seg(t, 18.95, 19.85));
  book.setOpen(Math.PI / 2 * open); book.root.position.y = hop(t, 2.6, .012, .45);
  // little books
  for (const L of LB) {
    const [hx, hz, hy] = HOME[L.i], [lx, lz, ly] = LAND[L.i], ph = L.i * TAU / 3;
    const fly = Math.min(ss(seg(t, 4.6 + L.i * .15, 5.5 + L.i * .15)), 1 - ss(seg(t, 10.0 + L.i * .2, 10.8 + L.i * .2)));
    // birds in the sky: a loop close to the backdrop, far from the camera
    const a = (t - 4.6) * 1.1 + ph, px = Math.cos(a) * .16, pz = .05 + Math.sin(a) * .03, py = .15 + Math.sin(t * 2.1 + ph) * .01;
    const ground = t < 9.5 ? [hx, hz, hy] : [lx, lz, ly];
    const leave = t > 9.9 && t < 11.5 ? Math.sin(Math.PI * (1 - fly)) * .3 : 0;   // up and out over the top of the frame, then down at the side
    const x = lerp(ground[0], px, fly), z = lerp(ground[1], pz, fly), y = lerp(0, py, fly) + leave;
    const yaw = Math.sin(t * 1.7 + ph) * .25;   // spine across, open pages toward the camera, flapping like wings
    L.wrap.position.set(x, y + hop(t, COUNT[L.i], .03, .42), z);
    L.wrap.rotation.y = lerp(ground[2], yaw, ss(seg(fly, 0, .4))); L.bk.root.scale.setScalar(lerp(.36, .17, ss(fly)));
    const flapTh = Math.PI * (.72 + .2 * Math.sin(TAU * 3.2 * t + ph));
    const count = Math.sin(Math.PI * seg(t, COUNT[L.i], COUNT[L.i] + .42)) * .9;     // cover pops open on its count
    const clap = t > 11.2 && t < 18.5 ? beatPulse(t, 12.2) * .55 : 0;          // covers clap on the beat
    const cs_ = fly < .05; if (L.cs !== cs_) { L.cs = cs_; L.wrap.traverse(o => { if (o.isMesh) o.castShadow = cs_; }); }
    L.bk.setOpen(lerp(count + clap, flapTh, fly)); L.roll.rotation.x = lerp(0, flapTh / 2 - .35, fly);
  }
  // pop-ups
  for (const r of POPS) { const k = r.rise(t); r.g.visible = k > .002; if (!r.g.visible) continue; r.g.rotation.x = r.dir * (Math.PI / 2) * (1 - k); if (r.sway) r.m.rotation.z = Math.sin(t * 1.6 + r.ph) * r.sway * k; }
  SUN.g.position.y = lerp(.0, .1, eo(seg(t, 6.0, 8.0))); SUN.m.rotation.z = Math.sin(t * 2) * .05;
  BANNER.g.position.y = .125 + Math.sin(t * 3) * .002;
  for (const L of LEAVES) { const u = t - L.t0; L.m.visible = u > 0 && t < 18.9; if (!L.m.visible) continue;
    L.m.position.set(Math.sign(L.vx) * .085 + L.vx * u, .15 + L.vy * u - .2 * u * u, .03 + L.vz * u); L.m.rotation.set(L.spin * u * .5, L.spin * u, L.spin * u * .3); }
  // characters
  const cs = cast(t); place(tunas, cs.tunas); place(mama, cs.mama); place(papa, cs.papa);
  // camera and look
  const c = CAM(t); cam.position.set(c[0], c[1], c[2]); cam.fov = c[6]; cam.lookAt(c[3], c[4], c[5]); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  post.dof.focus = Math.hypot(c[0] - c[3], c[1] - c[4], c[2] - c[5]); post.dof.aper = c[7]; post.dof.maxCoc = 14;
  post.vig.uniforms.fade.value = 1; post.vig.uniforms.warm.value = .12;
  scene.environmentIntensity = .45; scene.backgroundIntensity = .75;
  scene.updateMatrixWorld(true); post.composer.render();
  OX.clearRect(0, 0, W, H);
  if (t < .35) { OX.fillStyle = `rgba(0,0,0,${1 - t / .35})`; OX.fillRect(0, 0, W, H); }
};
window.render(Number(Q.get('t') || 0));
window.READY = true;
