// TemanTumbuh Series: the 10 s outro, after the Ingat ya! summary. Calm goodnight and a "go read a book" handoff.
import * as THREE from 'three';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { lerp, seg, ss, eio, eo, back, track, TAU } from './lib.js';
import * as A from './art.js';
import { makeBook, coverCanvases, texOf, BW, BD } from './book.js';
import { makePost } from './post.js';
import { makeTunas, makeAdult, drawTunas, TU_W, TU_H } from './chars.js';
import { cv } from './paper.js';

const W = 1920, H = 1080, Q = new URLSearchParams(location.search), DUR = 11;
const NEXT = (Q.get('next') || 'Sikat|Gigi').split('|');   // the next story's title on the glowing book
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
const lamp = (await gl.loadAsync('assets/desk_lamp_arm_01/desk_lamp_arm_01.gltf')).scene; lamp.position.set(-.6, 0, -.12); lamp.scale.setScalar(.55); lamp.rotation.y = -.4;
let bulb = null; lamp.traverse(o => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; if (o.material.name.includes('light')) { o.material = o.material.clone(); o.material.emissive = new THREE.Color('#ffd9a0'); o.material.emissiveIntensity = 6; bulb = o.material; } } });
scene.add(lamp);

// the TemanTumbuh book lies closed on the desk; Tunas stands on it
const icon = (x, px, py, w, h) => { const c = cv(TU_W, TU_H); drawTunas(c.getContext('2d'), { expr: 'senang' }); x.drawImage(c, px + w * .05, py + h * .1, w * .9, h * .9 * TU_H / TU_W * .8); };
const book = makeBook(coverCanvases(icon, { title: 'TemanTumbuh', sub: 'Series', foot: '~ buka, baca, tumbuh ~', tpx: 150, spx: 150, ink: '#fff3d6' }));
book.setOpen(0); scene.add(book.root);

// three little books stand up behind it like a shelf; the middle one is the next story
const SHELF = [['#d9734f', 'Cuci', 'Tangan'], ['#e3b23c', NEXT[0], NEXT[1] || ''], ['#5a8fc4', 'Tanam', 'Biji']].map(([bg, a, b], i) => {
  const bk = makeBook(coverCanvases(icon, { bg, title: a, sub: b, foot: 'TemanTumbuh', tpx: 230, spx: 200, ink: i === 1 ? '#fff3d6' : undefined }));
  bk.setOpen(0); const s = i === 1 ? .42 : .36;
  const wrap = new THREE.Group(); bk.root.scale.setScalar(s); bk.root.position.z = -BD * s; wrap.add(bk.root);
  wrap.position.set((i - 1) * .17, 0, -.045 - (i === 1 ? .0 : .012)); wrap.rotation.y = (1 - i) * .12; scene.add(wrap);
  const glow = []; if (i === 1) bk.root.traverse(o => { if (o.isMesh && o.material && 'emissive' in o.material) { o.material = o.material.clone(); glow.push(o.material); } });
  return { bk, wrap, i, glow, s };
});
const STAND = [.55, .8, 1.05];

const tunas = makeTunas(.08); scene.add(tunas.root, tunas.shadow);
const mama = makeAdult('mama', .13), papa = makeAdult('papa', .134); scene.add(mama.root, mama.shadow, papa.root, papa.shadow);
const blink = t => (t % 3.4) < .13 ? 1 : 0;
const hop = (t, a, h = .006, d = .4) => t > a && t < a + d ? Math.sin(Math.PI * (t - a) / d) * h : 0;

// lights
const sun = new THREE.DirectionalLight('#fff3e0', 2.2); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -.0001; sun.shadow.normalBias = .0004; sun.shadow.radius = 4;
Object.assign(sun.shadow.camera, { left: -.45, right: .45, top: .45, bottom: -.45, near: .1, far: 3 }); sun.position.set(-.3, .6, .8); sun.target.position.set(0, .05, .1); scene.add(sun, sun.target);
const hemi = new THREE.HemisphereLight('#cfe6ff', '#caa27a', .5); scene.add(hemi);
const lampLight = new THREE.PointLight('#ffcf94', .35, .9, 2); lampLight.position.set(-.5, .36, .0); scene.add(lampLight);

// camera: from the top-down view the episode ends on, down to desk level
const CAM = track([
  [0, [0, .74, .16, 0, 0, .15, 32, 3]], [.3, [0, .74, .16, 0, 0, .15, 32, 3]],
  [2.0, [0, .25, .82, 0, .035, .19, 30, 2.2]], [8.0, [0, .23, .78, 0, .04, .2, 30, 2.2]], [11, [0, .22, .76, 0, .04, .2, 30, 2.2]],
]);
cam.up.set(0, .7, -.7);

// read-along text at the bottom, in the book's font
const LINES = [
  [2.2, 'Sekarang, yuk baca buku sama Mama atau Papa!'],
  [6.0, 'Sampai ketemu lagi, ya!'],
  [8.0, 'Dadaaah!'],
  [8.0, 'Dadaaah!'],
  [8.02, 'Dadaaah!'],
];
function drawSubs(t, a = 1) {
  const L = [...LINES].reverse().find(([t0]) => t >= t0); if (!L) return; const [t0, txt] = L, nx = LINES[LINES.indexOf(L) + 1];
  const k = Math.min(ss(seg(t, t0, t0 + .25)), nx ? 1 : 1, 1 - ss(seg(t, nx ? nx[0] - .25 : 99, nx ? nx[0] : 100))) * a; if (k <= 0) return;
  OX.save(); OX.globalAlpha = k; OX.font = '700 64px Fredoka'; OX.textAlign = 'center'; OX.textBaseline = 'middle';
  OX.lineJoin = 'round'; OX.lineWidth = 14; OX.strokeStyle = 'rgba(60,40,28,.85)'; OX.strokeText(txt, W / 2, H * .88); OX.fillStyle = '#fff6e6'; OX.fillText(txt, W / 2, H * .88); OX.restore();
}

window.EV = STAND.map(t => ({ t, type: 'stand' })); window.DUR = DUR;

window.render = t => {
  // shelf books stand up one by one; the next story hops and glows on the chime
  for (const B of SHELF) {
    const k = back(seg(t, STAND[B.i], STAND[B.i] + .45), 1.6);
    B.wrap.rotation.x = (Math.PI / 2) * k; B.wrap.visible = k > .002 || t > STAND[B.i];
    if (B.i === 1) { B.wrap.position.y = hop(t, 5.5, .02, .45) + hop(t, 6.0, .008, .3); const g = Math.sin(Math.PI * seg(t, 5.5, 7.2)) * .55; for (const m of B.glow) { m.emissive = m.emissive || new THREE.Color(); m.emissive.set('#ffd27a'); m.emissiveIntensity = g; } }
  }
  // Tunas pops up on the closed book, points at the books, waves goodbye
  const up = back(seg(t, 1.3, 1.85), 1.7);
  tunas.root.visible = tunas.shadow.visible = up > .01;
  const point = t > 3.0 && t < 5.4, bye = t > 6.0 && t < 10.0, wave = bye ? Math.sin(t * 9) * .35 : 0;
  tunas.pose({ expr: 'senang', blink: blink(t), armL: bye ? 2.3 + wave : (t > 1.9 && t < 2.6 ? 2.3 : .35), armR: point ? 1.6 : bye ? 2.3 - wave : .35, look: point ? -.25 : 0 });
  tunas.root.position.set(0, hop(t, 2.15, .008, .4) + hop(t, 6.0, .012, .45) + hop(t, 8.0, .02, .5), .345); tunas.root.rotation.x = -(Math.PI / 2) * (1 - up);
  tunas.shadow.position.set(0, .0004, .345);
  // the room winds down: the lamp dims, then a warm fade
  // Mama and Papa pop up beside Tunas and wave with everyone; all jump on "Dadaaah!"
  for (const [c, x, a, ph] of [[mama, -.17, 6.1, 0], [papa, .17, 6.3, 1.3]]) {
    const k = back(seg(t, a, a + .55), 1.7); c.root.visible = c.shadow.visible = k > .01;
    const w = Math.sin(t * 8 + ph) * .35;
    c.pose({ armL: x > 0 ? 2.3 + w : .12, armR: x < 0 ? 2.3 + w : .12, look: x < 0 ? .35 : -.35, blink: ((t + ph) % 3.1) < .13 ? 1 : 0, sandals: x > 0 });
    c.root.position.set(x, hop(t, 8.0 + ph * .02, .016, .5), .3); c.root.rotation.x = -(Math.PI / 2) * (1 - k); c.shadow.position.set(x, .0004, .3);
  }
  const dim = ss(seg(t, 9.2, 10.4));
  if (bulb) bulb.emissiveIntensity = 6 * (1 - .7 * dim); lampLight.intensity = .35 * (1 - .6 * dim); sun.intensity = 2.2 * (1 - .55 * dim); hemi.intensity = .5 * (1 - .5 * dim);
  const c = CAM(t); cam.position.set(c[0], c[1], c[2]); cam.fov = c[6]; cam.lookAt(c[3], c[4], c[5]); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  post.dof.focus = Math.hypot(c[0] - c[3], c[1] - c[4], c[2] - c[5]); post.dof.aper = c[7]; post.dof.maxCoc = 14;
  post.vig.uniforms.fade.value = 1; post.vig.uniforms.warm.value = .12 + .1 * dim;
  scene.environmentIntensity = .45 * (1 - .4 * dim); scene.backgroundIntensity = .75 * (1 - .5 * dim);
  scene.updateMatrixWorld(true); post.composer.render();
  OX.clearRect(0, 0, W, H);
  drawSubs(t, 1 - ss(seg(t, 9.3, 9.8)));
  const f = ss(seg(t, 9.5, 10.5)); if (f > 0) { OX.fillStyle = `rgba(30,20,14,${f})`; OX.fillRect(0, 0, W, H); }
  const m = Math.min(ss(seg(t, 9.9, 10.4)), 1); if (m > 0) { OX.save(); OX.globalAlpha = m; OX.textAlign = 'center'; OX.textBaseline = 'middle';
    OX.font = '96px "Lilita One"'; OX.fillStyle = '#fff3d6'; OX.fillText('TemanTumbuh', W / 2, H / 2 - 20); OX.font = '600 34px Fredoka'; OX.fillStyle = '#e0b456'; OX.fillText('S E R I E S', W / 2, H / 2 + 52); OX.restore(); }
};
window.render(Number(Q.get('t') || 0));
window.READY = true;
