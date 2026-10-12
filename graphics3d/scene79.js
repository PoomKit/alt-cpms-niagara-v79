// CPMS reference building V7.9 - 8 storeys, chiller plant on the ground floor, cooling towers on the roof, air side per floor.
// Max equipment drawn (6 per type); slots that are not installed are ghosts.  Layers: shell / plant / piping / air side / zones / future systems.
// Data: window.MODEL (model.py), window.ALARMS (alarms.py), window.PTS (live points).  Live = BajaScript, else DEMO.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { Sky } from 'three/examples/jsm/objects/Sky.js';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { installR9 } from './r9office.js';
import { buildDevices } from './devices79.js';

const M = window.MODEL, AL = window.ALARMS, PTS = window.PTS, EFX = window.EFFECTS;
const $ = id => document.getElementById(id);
const mm = v => v / 1000;
const P3 = (x, y, z) => new THREE.Vector3(mm(x), mm(z), -mm(y));          // model (x east, y north, z up) -> three
const clock = new THREE.Clock();
// ------------------------------------------------------------------ renderer / scene
const host = $('view');
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(2, devicePixelRatio)); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.55; renderer.outputColorSpace = THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 4000);
camera.position.set(95, 70, 60);
const controls = new OrbitControls(camera, renderer.domElement); controls.target.set(30, 12, -20); controls.enableDamping = true;
controls.maxPolarAngle = Math.PI * 0.495; controls.minDistance = 2; controls.maxDistance = 420;
Object.assign(controls, { zoomToCursor: true, screenSpacePanning: true, dampingFactor: .09, zoomSpeed: 1.3, panSpeed: 1.1, rotateSpeed: .7, keyPanSpeed: 25 });
controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN }; controls.listenToKeyEvents(window);
let FLY = null;   // smooth camera move: flyTo(position, target)
function flyTo(p, tg, ms = 900){ FLY = { p0: camera.position.clone(), t0: controls.target.clone(), p1: new THREE.Vector3(...p), t1: new THREE.Vector3(...tg), s: performance.now(), ms }; }
function flyStep(){ if (!FLY) return; const k = Math.min(1, (performance.now() - FLY.s) / FLY.ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
  camera.position.lerpVectors(FLY.p0, FLY.p1, e); controls.target.lerpVectors(FLY.t0, FLY.t1, e); if (k >= 1) FLY = null; }
function zoomBy(f){ const d = camera.position.clone().sub(controls.target); flyTo(controls.target.clone().add(d.multiplyScalar(f)).toArray(), controls.target.toArray(), 350); }
function resize(){ const w = host.clientWidth, h = host.clientHeight; renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }
addEventListener('resize', resize); resize();
const pmrem = new THREE.PMREMGenerator(renderer); scene.environmentIntensity = .3;

// ------------------------------------------------------------------ procedural textures
function canvasTex(w, h, draw, repeat){ const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); draw(g, w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); } return t; }
function noise(g, w, h, base, amp, n){ g.fillStyle = base; g.fillRect(0, 0, w, h); for (let i = 0; i < n; i++) { const v = (Math.random() - .5) * amp;
  g.fillStyle = `rgba(${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${Math.abs(v)})`; const s = Math.random() * 3 + .5; g.fillRect(Math.random() * w, Math.random() * h, s, s); } }
const T = {
  concrete: canvasTex(512, 512, (g, w, h) => { noise(g, w, h, '#b3ada2', .14, 16000); g.strokeStyle = 'rgba(0,0,0,.18)'; g.lineWidth = 2; g.strokeRect(0, 0, w, h); }, [6, 4]),
  asphalt: canvasTex(512, 512, (g, w, h) => noise(g, w, h, '#3a3c3f', .25, 22000), [60, 60]),
  grass: canvasTex(512, 512, (g, w, h) => { noise(g, w, h, '#5d7b36', .22, 20000); for (let i = 0; i < 9000; i++) { const x = Math.random() * w, y = Math.random() * h, gg = 90 + Math.random() * 70 | 0;
    g.strokeStyle = `rgba(${gg * .55 | 0},${gg},${gg * .35 | 0},.55)`; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.random() * 2 - 1, y - 3 - Math.random() * 4); g.stroke(); } }, [90, 90]),
  roof: canvasTex(512, 512, (g, w, h) => { noise(g, w, h, '#a9a49a', .12, 12000); }, [4, 3]),
  wall: canvasTex(256, 256, (g, w, h) => noise(g, w, h, '#cfc9be', .08, 5000), [4, 2]),
  louvre: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#2d3a35'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 8) { g.fillStyle = '#4b5f57'; g.fillRect(0, y, w, 4); } }, [1, 1]),
  ctPanel: canvasTex(256, 256, (g, w, h) => { noise(g, w, h, '#c8cdd0', .06, 3000); for (let x = 0; x < w; x += 32) { g.fillStyle = 'rgba(0,0,0,.10)'; g.fillRect(x, 0, 3, h); } }, [2, 1]),
  ctLouvre: canvasTex(128, 256, (g, w, h) => { g.fillStyle = '#20302c'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 10) { const gr = g.createLinearGradient(0, y, 0, y + 7);
    gr.addColorStop(0, '#5e7a6f'); gr.addColorStop(1, '#2b3d37'); g.fillStyle = gr; g.fillRect(0, y, w, 7); } }, [3, 3]),
  facade: canvasTex(512, 256, (g, w, h) => { g.fillStyle = '#e9e6df'; g.fillRect(0, 0, w, h); g.fillStyle = '#c4c9cc'; for (let x = 0; x < w; x += 64) g.fillRect(x, 0, 2, h);
    g.fillStyle = '#5d7486'; g.fillRect(0, h * .62, w, h * .2); g.fillStyle = 'rgba(255,255,255,.25)'; for (let x = 0; x < w; x += 64) g.fillRect(x + 4, h * .64, 24, h * .16); }, [8, 1]),
  water: canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#4f7f8f'; g.fillRect(0, 0, w, h); for (let i = 0; i < 300; i++) { g.strokeStyle = 'rgba(255,255,255,.18)'; g.beginPath();
    const x = Math.random() * w, y = Math.random() * h; g.moveTo(x, y); g.lineTo(x + 18, y + 2); g.stroke(); } }, [1, 1]),
  fall: canvasTex(64, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(190,225,240,.0)'); gr.addColorStop(.1, 'rgba(190,225,240,.75)');
    gr.addColorStop(1, 'rgba(150,200,220,.35)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); for (let i = 0; i < 60; i++) { g.fillStyle = 'rgba(255,255,255,.55)'; g.fillRect(Math.random() * w, Math.random() * h, 1.5, 14); } }, [3, 1]),
  soft: canvasTex(128, 128, (g, w, h) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }),
  cloud: canvasTex(256, 128, (g, w, h) => { for (let i = 0; i < 26; i++) { const x = 40 + Math.random() * 176, y = 50 + Math.random() * 40, r = 18 + Math.random() * 30;
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); } }),
};
const MAT = {
  concrete: new THREE.MeshStandardMaterial({ map: T.concrete, roughness: .92 }),
  slab: new THREE.MeshStandardMaterial({ map: T.roof, roughness: .9 }),
  wall: new THREE.MeshStandardMaterial({ map: T.wall, roughness: .85 }),
  steel: new THREE.MeshStandardMaterial({ color: 0x3b4045, metalness: .55, roughness: .5 }),
  galv: new THREE.MeshStandardMaterial({ color: 0xa4abb0, metalness: .75, roughness: .38 }),
  almond: new THREE.MeshStandardMaterial({ color: 0xd8cfb6, metalness: .25, roughness: .42 }),
  almondDark: new THREE.MeshStandardMaterial({ color: 0xb9ae93, metalness: .3, roughness: .5 }),
  panel: new THREE.MeshStandardMaterial({ color: 0xcfd3d4, metalness: .35, roughness: .4 }),
  black: new THREE.MeshStandardMaterial({ color: 0x1d2024, metalness: .3, roughness: .6 }),
  motor: new THREE.MeshStandardMaterial({ color: 0x2d4f7c, metalness: .45, roughness: .45 }),
  iron: new THREE.MeshStandardMaterial({ color: 0x4a4f55, metalness: .6, roughness: .55 }),
  red: new THREE.MeshStandardMaterial({ color: 0xb3261e, metalness: .3, roughness: .45 }),
  yellow: new THREE.MeshStandardMaterial({ color: 0xf0b323, metalness: .2, roughness: .5 }),
  ctPanel: new THREE.MeshStandardMaterial({ map: T.ctPanel, roughness: .55, metalness: .1 }),
  ctLouvre: new THREE.MeshStandardMaterial({ map: T.ctLouvre, roughness: .7 }),
  glassDark: new THREE.MeshStandardMaterial({ color: 0x0e2230, metalness: .9, roughness: .08 }),
  water: new THREE.MeshStandardMaterial({ map: T.water, color: 0x8fb8c4, metalness: .2, roughness: .08, transparent: true, opacity: .85 }),
  frp: new THREE.MeshStandardMaterial({ color: 0xe9edef, roughness: .42, metalness: .05 }),
  screen: new THREE.MeshStandardMaterial({ color: 0x0d3550, emissive: 0x1a6ea0, emissiveIntensity: .8 }),
};
// r6 (R9 palette): neutral concrete, powder-coated housings, galvanised steel (reference appearance, not an as-built colour)
MAT.almond.color.set('#dedbd0'); MAT.almond.roughness = .58; MAT.almond.metalness = .12; MAT.almondDark.color.set('#a4aaa7'); MAT.almondDark.roughness = .64;
MAT.motor.color.set('#345e73'); MAT.motor.roughness = .52; MAT.iron.color.set('#526970'); MAT.iron.roughness = .65;
MAT.panel.color.set('#d2d8d7'); MAT.panel.roughness = .62; MAT.panel.metalness = .12; MAT.galv.color.set('#a9b2b4'); MAT.galv.roughness = .48; MAT.galv.metalness = .68;
MAT.frp.color.set('#e4e6df'); MAT.frp.roughness = .72; MAT.yellow.color.set('#c9ab50'); MAT.yellow.roughness = .68; MAT.steel.color.set('#667279'); MAT.steel.roughness = .65;
const svcMat = {}; for (const k in M.service) { const [, col, ins] = M.service[k];
  svcMat[k] = ins ? new THREE.MeshStandardMaterial({ color: 0xd3d8dc, metalness: .85, roughness: .3 }) : new THREE.MeshStandardMaterial({ color: new THREE.Color(col), metalness: .35, roughness: .4 });
  svcMat[k + '_band'] = new THREE.MeshStandardMaterial({ color: new THREE.Color(col), metalness: .2, roughness: .5 }); }

function mesh(geo, mat, parent, pos, rot){ const m = new THREE.Mesh(geo, mat); m.castShadow = m.receiveShadow = true; if (pos) m.position.copy(pos); if (rot) m.rotation.set(...rot); parent.add(m); return m; }
const box = (w, h, d, r = 0) => r ? new RoundedBoxGeometry(w, h, d, 3, r) : new THREE.BoxGeometry(w, h, d);
const cyl = (r, l, s = 32) => new THREE.CylinderGeometry(r, r, l, s);

// ------------------------------------------------------------------ sky, sun, environment, outside world
const sky = new Sky(); sky.scale.setScalar(2500); scene.add(sky);
const U = sky.material.uniforms; U.turbidity.value = 6; U.rayleigh.value = 1.6; U.mieCoefficient.value = .006; U.mieDirectionalG.value = .85;
const sun = new THREE.DirectionalLight(0xfff2dc, 3.2); sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 60, bottom: -60, near: 1, far: 400 }); sun.shadow.bias = -0.0004; sun.shadow.normalBias = .03;
scene.add(sun, sun.target); sun.target.position.set(32, 0, -20);
const hemi = new THREE.HemisphereLight(0xcfe3ff, 0x5a5448, .55); scene.add(hemi);
const ground = mesh(new THREE.PlaneGeometry(1600, 1600), new THREE.MeshStandardMaterial({ map: T.grass, roughness: 1 }), scene, new THREE.Vector3(32, -0.32, -20), [-Math.PI / 2, 0, 0]);
const apron = mesh(new THREE.PlaneGeometry(130, 100), new THREE.MeshStandardMaterial({ map: T.asphalt, roughness: .85, metalness: .05 }), scene, new THREE.Vector3(32, -0.3, -20), [-Math.PI / 2, 0, 0]);
const WET = [apron.material, ground.material, MAT.slab];
for (let i = 0; i < 30; i++) mesh(box(.12, .01, 5), new THREE.MeshStandardMaterial({ color: 0xe8e8e0, roughness: .8 }), scene, new THREE.Vector3(-4 + i * 2.6, -0.29, 12));
const lampLights = [];
for (let i = 0; i < 7; i++) { const g = new THREE.Group(); g.position.set(-10 + i * 14, -0.3, 22); scene.add(g); mesh(cyl(.09, 9, 10), MAT.galv, g, new THREE.Vector3(0, 4.5, 0));
  mesh(box(1.2, .18, .4), MAT.galv, g, new THREE.Vector3(.5, 9, 0)); const L = new THREE.PointLight(0xffd6a0, 0, 40, 1.6); L.position.set(.6, 8.7, 0); g.add(L); lampLights.push(L); }
const trunkG = cyl(.18, 3, 8), crownG = new THREE.IcosahedronGeometry(1.9, 1); const crownM = new THREE.MeshStandardMaterial({ color: 0x3d6b2f, roughness: .95, flatShading: true });
const trunkM = new THREE.MeshStandardMaterial({ color: 0x5b4632, roughness: 1 }); const trees = [];
const leafM = [0x2f5a24, 0x3b6b2a, 0x4a7a32, 0x355f2c, 0x56813a].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: .9, flatShading: true }));
for (let i = 0; i < 70; i++) { const a = Math.random() * Math.PI * 2, r = 62 + Math.random() * 80, x = 32 + Math.cos(a) * r, z = -20 + Math.sin(a) * r;
  const g = new THREE.Group(); g.position.set(x, -0.3, z); const s = .8 + Math.random() * .8; g.scale.setScalar(s); g.rotation.y = Math.random() * 6; scene.add(g);
  mesh(trunkG, trunkM, g, new THREE.Vector3(0, 1.5, 0));
  for (let k = 0; k < 5; k++) { const c = mesh(crownG, leafM[(i + k) % leafM.length], g, new THREE.Vector3((Math.random() - .5) * 1.8, 3.4 + Math.random() * 1.4, (Math.random() - .5) * 1.8)); c.scale.setScalar(.55 + Math.random() * .4); }
  trees.push(g); }
// ------------------------------------------------------------------ r7: site around the building - street grid with lanes and kerbs,
// sidewalks, car parks with cars, street trees and neighbouring buildings (reference context only, not survey data)
const SITE = new THREE.Group(); scene.add(SITE);
{ const ROADS = [{ x: 35, z: 40, w: 380, d: 12 }, { x: 35, z: -85, w: 380, d: 12 }, { x: 110, z: -22, w: 12, d: 330 }, { x: -50, z: -22, w: 12, d: 330 }];
  const onRoad = (x, z, m = 0) => ROADS.some(r => Math.abs(x - r.x) < r.w / 2 + m && Math.abs(z - r.z) < r.d / 2 + m);
  const asph = new THREE.MeshStandardMaterial({ map: T.asphalt, color: 0x9a9a9a, roughness: .9 }), walk = new THREE.MeshStandardMaterial({ color: 0xc9c5bb, roughness: .95 });
  const kerb = new THREE.MeshStandardMaterial({ color: 0xe2ded5, roughness: .8 }), paint = new THREE.MeshStandardMaterial({ color: 0xf2f2ea, roughness: .7 }), yel = new THREE.MeshStandardMaterial({ color: 0xe8c234, roughness: .7 });
  for (const r of ROADS) { mesh(box(r.w, .04, r.d), asph, SITE, new THREE.Vector3(r.x, -0.3, r.z));
    const along = r.w > r.d, L = along ? r.w : r.d;
    for (const sd of [-1, 1]) { const o = (along ? r.d : r.w) / 2 + 1.9;                                        // sidewalk 3.5 m + kerb
      mesh(box(along ? L : 3.5, .16, along ? 3.5 : L), walk, SITE, new THREE.Vector3(r.x + (along ? 0 : sd * o), -0.22, r.z + (along ? sd * o : 0)));
      mesh(box(along ? L : .2, .2, along ? .2 : L), kerb, SITE, new THREE.Vector3(r.x + (along ? 0 : sd * (o - 1.8)), -0.2, r.z + (along ? sd * (o - 1.8) : 0))); }
    const dash = new THREE.InstancedMesh(box(along ? 3 : .15, .02, along ? .15 : 3), paint, Math.floor(L / 8)); const m4 = new THREE.Matrix4();
    for (let i = 0; i < dash.count; i++) { const t = -L / 2 + 4 + i * 8; m4.makeTranslation(r.x + (along ? t : 0), -0.27, r.z + (along ? 0 : t)); dash.setMatrixAt(i, m4); }
    SITE.add(dash);
    for (const sd of [-1, 1]) mesh(box(along ? L : .12, .02, along ? .12 : L), yel, SITE, new THREE.Vector3(r.x + (along ? 0 : sd * (r.w / 2 - .4)), -0.27, r.z + (along ? sd * (r.d / 2 - .4) : 0))); }
  // cars: south lot (stalls at z 12) and west lot, instanced body + cabin, varied colours
  const cars = [];
  for (let i = 0; i < 28; i++) if (Math.random() < .7) cars.push([-2.7 + i * 2.6, 12, 0]);
  for (const x of [-27, -19, -11]) for (let i = 0; i < 20; i++) { const z = -62 + i * 2.6; if (Math.random() < .6) cars.push([x, z, Math.PI / 2]); }
  for (const x of [-27, -19, -11]) for (let i = 0; i < 21; i++) mesh(box(5, .01, .12), paint, SITE, new THREE.Vector3(x, -0.28, -63.3 + i * 2.6));
  const CC = [0xf4f4f2, 0x1d1f22, 0x8a9096, 0x7a1f22, 0x1f3a5f, 0xb8bcc2, 0x3a4a3a];
  const body = new THREE.InstancedMesh(box(1.8, .75, 4.4, .12), new THREE.MeshStandardMaterial({ roughness: .35, metalness: .55 }), cars.length);
  const cab = new THREE.InstancedMesh(box(1.6, .55, 2.3, .12), new THREE.MeshStandardMaterial({ color: 0x1b2430, roughness: .15, metalness: .6 }), cars.length);
  const wheel = new THREE.InstancedMesh(cyl(.33, .22, 14), new THREE.MeshStandardMaterial({ color: 0x111111, roughness: .9 }), cars.length * 4);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), qw = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, Math.PI / 2)), one = new THREE.Vector3(1, 1, 1);
  cars.forEach(([x, z, a], i) => { q.setFromEuler(new THREE.Euler(0, a, 0));
    body.setMatrixAt(i, m4.compose(new THREE.Vector3(x, .25, z), q, one)); body.setColorAt(i, new THREE.Color(CC[(i * 7) % CC.length]));
    cab.setMatrixAt(i, m4.compose(new THREE.Vector3(x, .85, z).add(new THREE.Vector3(0, 0, -.2).applyQuaternion(q)), q, one));
    [[-.85, 1.35], [.85, 1.35], [-.85, -1.35], [.85, -1.35]].forEach(([dx, dz], k) => wheel.setMatrixAt(i * 4 + k, m4.compose(new THREE.Vector3(x, .03, z).add(new THREE.Vector3(dx, 0, dz).applyQuaternion(q)), q.clone().multiply(qw), one))); });
  for (const im of [body, cab, wheel]) { im.castShadow = true; im.receiveShadow = true; SITE.add(im); }
  // neighbouring buildings: plain massing with a window grid (reference context)
  const winTex = canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#d9d6cf'; g.fillRect(0, 0, w, h); for (let y = 0; y < 8; y++) for (let x = 0; x < 6; x++) { g.fillStyle = Math.random() < .25 ? '#7d8f9f' : '#5d6f80'; g.fillRect(8 + x * 41, 10 + y * 31, 30, 18); } });
  winTex.wrapS = winTex.wrapT = THREE.RepeatWrapping;
  const NB = [[-12, 72, 34, 22, 18], [34, 74, 30, 26, 30], [80, 70, 26, 20, 12], [150, 60, 30, 34, 24], [148, 10, 26, 30, 36], [146, -50, 30, 26, 16],
              [150, -120, 34, 30, 22], [80, -122, 40, 26, 28], [20, -124, 36, 24, 14], [-40, -126, 30, 30, 20], [-92, -60, 26, 34, 26], [-94, 6, 28, 30, 12], [-90, 66, 26, 26, 18]];
  for (const [x, z, w, d, h] of NB) { const t = winTex.clone(); t.needsUpdate = true; t.repeat.set(Math.max(1, Math.round(w / 6)), Math.max(1, Math.round(h / 3.6)));
    const m = new THREE.MeshStandardMaterial({ map: t, roughness: .75, color: [0xffffff, 0xf1ebe0, 0xe6ebef][Math.abs(x + z) % 3] });
    const b = mesh(box(w, h, d), m, SITE, new THREE.Vector3(x, h / 2 - .3, z)); b.castShadow = b.receiveShadow = true;
    mesh(box(w + .6, .8, d + .6), MAT.concrete, SITE, new THREE.Vector3(x, h + .1, z)); }
  // street trees every 10 m along the sidewalks; random park trees off the roads and buildings
  const inNB = (x, z, m) => NB.some(([bx, bz, w, d]) => Math.abs(x - bx) < w / 2 + m && Math.abs(z - bz) < d / 2 + m);
  for (const g of trees) if (onRoad(g.position.x, g.position.z, 5) || inNB(g.position.x, g.position.z, 3)) g.visible = false;
  const crownI = [], trunkI = [];
  for (const r of ROADS) { const along = r.w > r.d, L = along ? r.w : r.d;
    for (const sd of [-1, 1]) for (let t = -L / 2 + 6; t < L / 2 - 6; t += 10) { const x = r.x + (along ? t : sd * (r.w / 2 + 3)), z = r.z + (along ? sd * (r.d / 2 + 3) : t);
      if (ROADS.some(o => o !== r && onRoad(x, z, 4) && Math.abs(x - o.x) < o.w / 2 + 4 && Math.abs(z - o.z) < o.d / 2 + 4) || inNB(x, z, 1) || (x > -36 && x < 100 && z > -72 && z < 32)) continue;
      trunkI.push([x, z]); crownI.push([x, z]); } }
  const tI = new THREE.InstancedMesh(trunkG, trunkM, trunkI.length), cI = new THREE.InstancedMesh(crownG, leafM[1], crownI.length);
  trunkI.forEach(([x, z], i) => { tI.setMatrixAt(i, m4.makeTranslation(x, 1.2, z)); cI.setMatrixAt(i, m4.compose(new THREE.Vector3(x, 4, z), new THREE.Quaternion(), new THREE.Vector3(1.1, 1.25, 1.1))); });
  tI.castShadow = cI.castShadow = true; SITE.add(tI, cI); }
const storeGlass = { material: { emissiveIntensity: 0 } };
const AIRSIDE = { material: {} };

// ------------------------------------------------------------------ the building: plant room (1F), 8 floors, core, curtain wall, roof
const BLD = M.building, ROOFZ = M.roof_z, R = { x: M.room.x, y: M.room.y, h: M.room.h, slab: BLD.slab, wall: M.room.wall };
const W = mm(R.wall), RX = mm(R.x), RY = mm(R.y), RH = mm(R.h);
const LAYER = { shell: new THREE.Group(), plant: new THREE.Group(), piping: new THREE.Group(), air: new THREE.Group(), zones: new THREE.Group(), systems: new THREE.Group() };
for (const k in LAYER) scene.add(LAYER[k]);
const plant = LAYER.plant;
const XRAY = [], FLOORS = {};                 // floor -> {objs: [...]} (floor filter)
// V7.9 r4 (R9 design): chiller plant in basement B1 when the model puts the plant equipment below ground
const BASEMENT = M.equipment.some(e => e.type === 'chiller' && e.z < -1000);
const B1Z = BASEMENT ? Math.min(...M.equipment.filter(e => e.z < -1000).map(e => e.z)) - 100 : 0;
const zOf = f => f === 0 ? B1Z : f === 1 ? 0 : BLD.f1_h + (f - 2) * BLD.typ_h;
function onFloor(f, o){ (FLOORS[f] = FLOORS[f] || []).push(o); o.userData.floor = f; return o; }
const groundSlab = mesh(box(mm(BLD.x) + 2, .3, mm(BLD.y) + 2), MAT.concrete, LAYER.shell, P3(BLD.x / 2, BLD.y / 2, -150)); if (BASEMENT) onFloor(1, groundSlab);
const floor = BASEMENT ? mesh(box(mm(BLD.x), .3, mm(BLD.y)), new THREE.MeshStandardMaterial({ map: T.concrete, roughness: .55, metalness: .05, color: 0xb9bcb8 }), LAYER.plant, P3(BLD.x / 2, BLD.y / 2, B1Z - 150))
  : mesh(box(RX, .02, RY), new THREE.MeshStandardMaterial({ map: T.concrete, roughness: .55, metalness: .05, color: 0xb9bcb8 }), LAYER.plant, P3(R.x / 2, R.y / 2, 10));
if (BASEMENT) onFloor(0, floor);
function wall(x1, y1, x2, y2, h, holes, parent){ const L = Math.hypot(x2 - x1, y2 - y1), g = new THREE.Group(); g.position.copy(P3(x1, y1, 0)); g.rotation.y = -Math.atan2(y2 - y1, x2 - x1);
  const m = MAT.wall.clone(); m.transparent = true; XRAY.push(m); let segs = [[0, L, 0, h]];
  for (const o of holes || []) segs = segs.flatMap(([a, b, z0, z1]) => o.x >= b || o.x + o.w <= a ? [[a, b, z0, z1]] :
    [[a, o.x, z0, z1], [o.x + o.w, b, z0, z1], [o.x, o.x + o.w, z0, o.z], [o.x, o.x + o.w, o.z + o.h, z1]].filter(s => s[1] - s[0] > 1 && s[3] - s[2] > 1));
  for (const [a, b, z0, z1] of segs) mesh(box(mm(b - a), mm(z1 - z0), W), m, g, new THREE.Vector3(mm((a + b) / 2), mm((z0 + z1) / 2), 0));
  for (const o of holes || []) if (o.louvre) mesh(box(mm(o.w), mm(o.h), .05), new THREE.MeshStandardMaterial({ map: T.louvre, roughness: .7 }), g, new THREE.Vector3(mm(o.x + o.w / 2), mm(o.z + o.h / 2), 0));
  (parent || LAYER.shell).add(g); return g; }
const RHm = R.h;
if (!BASEMENT) {
onFloor(1, wall(0, 0, R.x, 0, RHm, [{ x: 2000, w: 3000, z: 0, h: 3500 }, { x: 12000, w: 4000, z: 2500, h: 1800, louvre: true }, { x: 24000, w: 4000, z: 2500, h: 1800, louvre: true }]));
onFloor(1, wall(R.x, 0, R.x, R.y, RHm, [{ x: 4000, w: 2400, z: 2600, h: 1500, louvre: true }]));
onFloor(1, wall(R.x, R.y, 0, R.y, RHm, [{ x: 30000, w: 1800, z: 0, h: 2400 }]));
onFloor(1, wall(0, R.y, 0, 0, RHm, []));
} else {   // B1 plant room: retaining walls (see-through in x-ray), columns, ceiling lights
  const bw = MAT.wall.clone(); bw.transparent = true; XRAY.push(bw); const bh = -B1Z - 300, g = new THREE.Group(); LAYER.shell.add(g); onFloor(0, g);
  for (const [x, y, w, d] of [[BLD.x / 2, -150, BLD.x + 300, 300], [BLD.x / 2, BLD.y + 150, BLD.x + 300, 300], [-150, BLD.y / 2, 300, BLD.y], [BLD.x + 150, BLD.y / 2, 300, BLD.y]])
    mesh(box(mm(w), mm(bh), mm(d)), bw, g, P3(x, y, B1Z + bh / 2));
  for (const [n, x] of M.grid_x) for (const [m_, y] of M.grid_y) mesh(box(.6, mm(bh), .6), MAT.concrete, g, P3(x, y, B1Z + bh / 2));
  for (let x = 6000; x < BLD.x; x += 9000) for (let y = 4000; y < BLD.y; y += 8000) { const q = P3(x, y, -500);
    mesh(box(1.2, .06, .2), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff4e0, emissiveIntensity: 1.2 }), g, q); } }
// floors, columns, curtain wall, core
const glassM = new THREE.MeshStandardMaterial({ color: 0x9db8c2, metalness: .15, roughness: .04, transparent: true, opacity: .42, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: .65 });
const mullM = new THREE.MeshStandardMaterial({ color: 0x3f4448, metalness: .6, roughness: .4 });   // dark anodised aluminium
const slabM = MAT.slab.clone(); slabM.transparent = true; XRAY.push(slabM);
for (let f = 2; f <= BLD.floors + 1; f++) { const z = f > BLD.floors ? ROOFZ : zOf(f);
  onFloor(f, mesh(box(mm(BLD.x), mm(BLD.slab), mm(BLD.y)), slabM, LAYER.shell, P3(BLD.x / 2, BLD.y / 2, z - BLD.slab / 2))); }
for (let f = 1; f <= BLD.floors; f++) { const z0 = zOf(f), h = (f === 1 ? BLD.f1_h : BLD.typ_h) - BLD.slab, g = new THREE.Group(); LAYER.shell.add(g); onFloor(f, g);
  for (const [x1, y1, x2, y2] of [[0, 0, BLD.x, 0], [BLD.x, 0, BLD.x, BLD.y], [BLD.x, BLD.y, 0, BLD.y], [0, BLD.y, 0, 0]]) {
    if (f === 1 && !BASEMENT && y1 === 0 && y2 === 0) { mesh(box(mm(BLD.x - R.x), mm(h), .03), glassM, g, P3((R.x + BLD.x) / 2, 0, z0 + h / 2)); continue; }
    if (f === 1 && !BASEMENT && x1 === 0 && x2 === 0) { mesh(box(.03, mm(h), mm(BLD.y - R.y)), glassM, g, P3(0, (R.y + BLD.y) / 2, z0 + h / 2)); continue; }
    const L = Math.hypot(x2 - x1, y2 - y1), horiz = y1 === y2;
    mesh(box(horiz ? mm(L) : .03, mm(h), horiz ? .03 : mm(L)), glassM, g, P3((x1 + x2) / 2, (y1 + y2) / 2, z0 + h / 2));
    for (let s = 0; s <= L; s += 2000) { const x = horiz ? Math.min(x1, x2) + s : x1, y = horiz ? y1 : Math.min(y1, y2) + s; mesh(box(.06, mm(h), .06), mullM, g, P3(x, y, z0 + h / 2)); }
    mesh(box(horiz ? mm(L) : .3, .7, horiz ? .3 : mm(L)), MAT.concrete, g, P3((x1 + x2) / 2, (y1 + y2) / 2, z0 + h - 350)); }   // concrete spandrel / slab edge
  for (const [n, x] of M.grid_x) for (const [m_, y] of M.grid_y) { if (f === 1 && !BASEMENT && x <= R.x && y <= R.y) continue;
    mesh(box(.6, mm(h), .6), MAT.concrete, g, P3(x, y, z0 + h / 2)); } }
const coreM = new THREE.MeshStandardMaterial({ map: T.concrete, color: 0xe2ddd3, roughness: .9, transparent: true }); XRAY.push(coreM);
mesh(box(mm(M.core.x1 - M.core.x0), mm(ROOFZ + 3500), mm(M.core.y1 - M.core.y0)), coreM, LAYER.shell, P3((M.core.x0 + M.core.x1) / 2, (M.core.y0 + M.core.y1) / 2, (ROOFZ + 3500) / 2));
for (const [x, y, w, d] of [[BLD.x / 2, 0, BLD.x, 300], [BLD.x / 2, BLD.y, BLD.x, 300], [0, BLD.y / 2, 300, BLD.y], [BLD.x, BLD.y / 2, 300, BLD.y]])
  onFloor(9, mesh(box(mm(w), mm(BLD.parapet), mm(d)), MAT.concrete, LAYER.shell, P3(x, y, ROOFZ + BLD.parapet / 2)));
const roomLights = []; if (!BASEMENT) for (let x = 4000; x < R.x; x += 8000) for (const y of [3500, 11500]) {
  const p = P3(x, y, R.h - 400); mesh(box(1.2, .06, .2), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff4e0, emissiveIntensity: 1.2 }), plant, p);
  const L = new THREE.PointLight(0xfff1dc, 9, 14, 1.8); L.position.copy(p).add(new THREE.Vector3(0, -.2, 0)); plant.add(L); roomLights.push(L); }
function textSprite(txt, size, col, bg){ const c = document.createElement('canvas'), g = c.getContext('2d'); c.width = 256; c.height = 128;
  if (bg) { g.fillStyle = bg; g.beginPath(); g.arc(128, 64, 54, 0, 7); g.fill(); } g.fillStyle = col; g.font = `600 ${size}px "Segoe UI",sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, 128, 66);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false, transparent: true })); s.scale.set(1.2, .6, 1); return s; }
for (const [n, x] of M.grid_x) { const s = textSprite(n, 46, '#1b2a36', 'rgba(255,255,255,.85)'); s.position.copy(P3(x, -2500, 0)); s.scale.set(1.6, .8, 1); LAYER.shell.add(s); }
for (const [n, y] of M.grid_y) { const s = textSprite(n, 46, '#1b2a36', 'rgba(255,255,255,.85)'); s.position.copy(P3(-2500, y, 0)); s.scale.set(1.6, .8, 1); LAYER.shell.add(s); }

// ------------------------------------------------------------------ equipment builders
const EQ = {};   // id -> {g, parts, mats, data}
function equipGroup(e){ const g = new THREE.Group(); g.position.copy(P3(e.x, e.y, e.z)); g.rotation.y = THREE.MathUtils.degToRad(e.rot || 0); (e.layer === 'air' ? LAYER.air : plant).add(g); if (e.floor !== undefined && e.floor !== null) onFloor(e.floor, g); else if (e.type === 'ct') onFloor(9, g);
  const rec = { e, g, parts: {}, spin: [], base: g.position.clone(), mats: new Set() }; EQ[e.id] = rec; g.userData.eq = e.id; return rec; }
function own(rec, m){ const c = m.clone(); rec.mats.add(c); return c; }
function lcd(w, h){ const c = document.createElement('canvas'); c.width = w; c.height = h; const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.MeshBasicMaterial({ map: tex, toneMapped: false });
  return { mat, draw(lines, bg = '#06263a', fg = '#7fe3ff'){ const g = c.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = `600 ${Math.floor(h / (lines.length + .6))}px Consolas,monospace`;
    lines.forEach((l, i) => g.fillText(l, 6, (i + 1) * h / (lines.length + .3))); tex.needsUpdate = true; } }; }
function nozzle(g, m, p){ mesh(cyl(.11, .5, 24), m, g, p, [0, 0, Math.PI / 2]); mesh(cyl(.19, .03, 28), MAT.iron, g, p.clone().add(new THREE.Vector3(-.25, 0, 0)), [0, 0, Math.PI / 2]); }
function chiller(e){ const r = equipGroup(e), L = mm(e.L), Wd = mm(e.W), H = mm(e.H), g = r.g, a = own(r, MAT.almond), ad = own(r, MAT.almondDark);
  mesh(box(L + .3, .1, Wd + .3), MAT.concrete, g, new THREE.Vector3(0, -.05, 0));                                              // 100 mm housekeeping pad
  mesh(box(L, .18, Wd * .92), own(r, MAT.steel), g, new THREE.Vector3(0, .09, 0));                                             // skid
  for (const s of [-1, 1]) mesh(box(.25, .55, Wd * .8), ad, g, new THREE.Vector3(s * L * .36, .45, 0));                         // tube sheet supports
  for (const s of [-1, 1]) for (const z of [-.7, .7]) mesh(box(.16, .04, .16), MAT.black, g, new THREE.Vector3(s * L * .42, .02, z));   // isolation pads
  const cond = mesh(cyl(.36, L * .86, 40), a, g, new THREE.Vector3(0, .62, -.22), [0, 0, Math.PI / 2]);                            // condenser G1
  const evap = mesh(cyl(.42, L * .9, 40), a, g, new THREE.Vector3(0, 1.08, .18), [0, 0, Math.PI / 2]);                            // evaporator G2 (insulated)
  r.parts.evap = evap; r.parts.cond = cond;
  for (const s of [-1, 1]) { mesh(cyl(.44, .12, 40), ad, g, new THREE.Vector3(s * L * .455, 1.08, .18), [0, 0, Math.PI / 2]);       // water boxes
    mesh(cyl(.38, .12, 40), ad, g, new THREE.Vector3(s * L * .44, .62, -.22), [0, 0, Math.PI / 2]); }
  for (const z of [.43, -.07]) nozzle(g, own(r, MAT.steel), new THREE.Vector3(-L * .5 - .05, 1.08, z));                           // CHW in / out
  for (const z of [-.42, -.02]) nozzle(g, own(r, MAT.steel), new THREE.Vector3(-L * .5 - .05, .62, z));                           // CDW in / out
  const comp = mesh(box(L * .36, .55, .62, .08), a, g, new THREE.Vector3(L * .05, 1.72, .05)); r.parts.comp = comp;                // screw compressor
  mesh(cyl(.26, .5, 32), ad, g, new THREE.Vector3(L * .26, 1.72, .05), [0, 0, Math.PI / 2]);                                       // motor housing
  for (const [x, z] of [[-L * .28, -.45], [-L * .1, -.45]]) { mesh(cyl(.17, .9, 28), a, g, new THREE.Vector3(x, 1.25, z));          // oil separators
    mesh(new THREE.SphereGeometry(.17, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), a, g, new THREE.Vector3(x, 1.7, z)); }
  mesh(new THREE.TorusGeometry(.32, .07, 14, 32, Math.PI), a, g, new THREE.Vector3(-L * .19, 1.72, -.45));                          // discharge line
  const pnl = mesh(box(.32, 1.1, .95, .02), own(r, MAT.panel), g, new THREE.Vector3(L * .5 + .02, 1.25, .25)); r.parts.panel = pnl;   // starter / UC800
  const scr = lcd(256, 128); mesh(new THREE.PlaneGeometry(.3, .16), scr.mat, g, new THREE.Vector3(L * .5 + .185, 1.45, .25), [0, Math.PI / 2, 0]); r.parts.lcd = scr;
  r.parts.beacon = mesh(cyl(.04, .1, 14), new THREE.MeshStandardMaterial({ color: 0x1b1b1b, emissive: 0x22c55e, emissiveIntensity: 0 }), g, new THREE.Vector3(L * .5 + .02, 1.86, .6));
  r.spin = []; }
function pump(e){ const r = equipGroup(e), g = r.g, L = mm(e.L);
  mesh(box(L + .25, .3, mm(e.W) + .35), own(r, MAT.concrete), g, new THREE.Vector3(0, .15, 0));                                      // inertia base
  mesh(box(L, .06, mm(e.W)), own(r, MAT.steel), g, new THREE.Vector3(0, .33, 0));
  const mot = mesh(cyl(.21, .62, 32), own(r, MAT.motor), g, new THREE.Vector3(L * .22, .6, 0), [0, 0, Math.PI / 2]); r.parts.motor = mot;
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; mesh(box(.6, .02, .05), own(r, MAT.motor), g, new THREE.Vector3(L * .22, .6 + Math.sin(a) * .215, Math.cos(a) * .215), [a, 0, 0]); }
  mesh(cyl(.13, .04, 24), own(r, MAT.motor), g, new THREE.Vector3(L * .22 + .33, .6, 0), [0, 0, Math.PI / 2]);
  const fan = mesh(cyl(.12, .05, 6), MAT.black, g, new THREE.Vector3(L * .22 + .36, .6, 0), [0, 0, Math.PI / 2]); r.spin.push({ m: fan, axis: 'x' });
  mesh(box(.32, .2, .22), MAT.yellow, g, new THREE.Vector3(-L * .07, .6, 0));                                                           // coupling guard
  const shaft = mesh(cyl(.035, .3, 12), MAT.galv, g, new THREE.Vector3(-L * .07, .6, 0), [0, 0, Math.PI / 2]); r.spin.push({ m: shaft, axis: 'x' });
  const vol = mesh(cyl(.3, .22, 36), own(r, MAT.iron), g, new THREE.Vector3(-L * .3, .62, 0), [Math.PI / 2, 0, 0]); r.parts.volute = vol;  // volute
  mesh(cyl(.1, .3, 24), own(r, MAT.iron), g, new THREE.Vector3(-L * .44, .62, 0), [0, 0, Math.PI / 2]);                                 // suction
  mesh(cyl(.09, .32, 24), own(r, MAT.iron), g, new THREE.Vector3(-L * .3, .95, 0));                                                     // discharge
  for (const s of [-1, 1]) mesh(box(.12, .12, .5), MAT.steel, g, new THREE.Vector3(s * L * .45, .05, 0)); }                              // spring isolators
function coolingTower(e){ const r = equipGroup(e), g = r.g, L = mm(e.L), D = mm(e.W), H = mm(e.H), frp = own(r, MAT.frp), st = MAT.galv;
  const legH = mm(e.z - ROOFZ);
  for (const [x, z] of [[-L / 2 + .1, -D / 2 + .1], [L / 2 - .1, -D / 2 + .1], [-L / 2 + .1, D / 2 - .1], [L / 2 - .1, D / 2 - .1], [0, -D / 2 + .1], [0, D / 2 - .1]])
    mesh(box(.15, legH, .15), st, g, new THREE.Vector3(x, -legH / 2, z));                                                           // steel support frame
  mesh(box(L, .1, D), st, g, new THREE.Vector3(0, -.05, 0));
  const bd = m => { m.userData.body = 1; return m; };                                                                              // r5: replaced by the Blender body
  r.parts.basin = bd(mesh(box(L, .55, D, .02), frp, g, new THREE.Vector3(0, .275, 0)));                                            // cold water basin
  const wm = MAT.water.clone(); wm.map = T.water.clone(); wm.map.wrapS = wm.map.wrapT = THREE.RepeatWrapping; wm.map.needsUpdate = true;
  const water = mesh(new THREE.PlaneGeometry(L - .08, D - .08), wm, g, new THREE.Vector3(0, .45, 0), [-Math.PI / 2, 0, 0]); water.castShadow = false; r.parts.water = water;
  for (const s of [-1, 1]) bd(mesh(box(L, H - .55, .08), frp, g, new THREE.Vector3(0, .55 + (H - .55) / 2, s * D / 2)));        // cased faces
  const fill = new THREE.MeshStandardMaterial({ color: 0x33413f, roughness: .95 });
  for (const s of [-1, 1]) bd(mesh(box(.55, H - 1.1, D - .3), fill, g, new THREE.Vector3(s * (L / 2 - .55), .55 + (H - 1.1) / 2 + .05, 0)));   // fill packs
  const curtain = new THREE.MeshBasicMaterial({ map: T.fall.clone(), transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide, color: 0xd6f0ff });
  curtain.map.wrapS = curtain.map.wrapT = THREE.RepeatWrapping; curtain.map.repeat.set(7, 2); curtain.map.needsUpdate = true; r.parts.curtain = curtain;
  for (const s of [-1, 1]) mesh(new THREE.PlaneGeometry(D - .32, H - 1.1), curtain, g, new THREE.Vector3(s * (L / 2 - .24), .55 + (H - 1.1) / 2, 0), [0, Math.PI / 2, 0]).castShadow = false;
  const lv = MAT.ctLouvre.clone(); lv.transparent = true; lv.opacity = .55; lv.depthWrite = false;
  for (const s of [-1, 1]) bd(mesh(box(.05, H - .95, D - .16), lv, g, new THREE.Vector3(s * (L / 2 - .03), .55 + (H - .95) / 2, 0)));   // air-inlet louvres
  bd(mesh(box(L, .1, D), frp, g, new THREE.Vector3(0, H, 0)));                                                                      // fan deck
  r.parts.hot = []; for (const s of [-1, 1]) { const x = s * L * .3;                                                                 // hot water basins (open)
    for (const [w, d, px, pz] of [[L * .36, .04, x, D * .4], [L * .36, .04, x, -D * .4], [.04, D * .8, x - L * .18, 0], [.04, D * .8, x + L * .18, 0]]) mesh(box(w, .25, d), frp, g, new THREE.Vector3(px, H + .17, pz));
    const hm = wm.clone(); hm.map = T.water.clone(); hm.map.wrapS = hm.map.wrapT = THREE.RepeatWrapping; hm.map.needsUpdate = true; hm.opacity = .9;
    mesh(new THREE.PlaneGeometry(L * .35, D * .79), hm, g, new THREE.Vector3(x, H + .2, 0), [-Math.PI / 2, 0, 0]).castShadow = false; r.parts.hot.push(hm); }
  // fan + discharge elbow hood (white FRP), outlet facing south
  bd(mesh(new THREE.CylinderGeometry(.86, 1.08, .5, 48, 1, true), frp, g, new THREE.Vector3(0, H + .3, 0))).material.side = THREE.DoubleSide;
  const fan = new THREE.Group(); fan.position.set(0, H + .35, 0); g.add(fan); r.spin.push({ m: fan, axis: 'y', fan: true }); r.parts.fan = fan;
  for (let i = 0; i < 6; i++) { const b = mesh(box(.92, .025, .22), MAT.black, fan, null, [.22, i * Math.PI / 3, 0]); b.position.set(Math.cos(i * Math.PI / 3) * .5, 0, -Math.sin(i * Math.PI / 3) * .5); }
  mesh(cyl(.14, .22, 18), MAT.galv, fan, null);
  const hc = new THREE.CubicBezierCurve3(new THREE.Vector3(0, H + .5, 0), new THREE.Vector3(0, H + 1.25, 0), new THREE.Vector3(0, H + 1.5, -.15), new THREE.Vector3(0, H + 1.5, -1.15));
  const hood = mesh(new THREE.TubeGeometry(hc, 40, .86, 48, false), frp, g); hood.material = frp.clone(); hood.material.side = THREE.DoubleSide; r.mats.add(hood.material);
  const rim = mesh(new THREE.TorusGeometry(.86, .045, 10, 48), frp, g, new THREE.Vector3(0, H + 1.5, -1.15));
  const scr = mesh(new THREE.CircleGeometry(.84, 40), new THREE.MeshStandardMaterial({ color: 0x9aa3a8, metalness: .6, roughness: .5, transparent: true, opacity: .22, side: THREE.DoubleSide, depthWrite: false }), g, new THREE.Vector3(0, H + 1.5, -1.13));
  scr.castShadow = false; r.parts.outlet = new THREE.Vector3(0, H + 1.5, -1.2);
  bd(mesh(box(.34, .3, .3), own(r, MAT.motor), g, new THREE.Vector3(.95, H + .25, -.75))); bd(mesh(box(.24, .2, .14), MAT.panel, g, new THREE.Vector3(1.15, H + .25, -.45)));   // fan motor + isolator
  // handrail around the fan deck (posts @ ~0.9 m, top + mid rail, toe board)
  const rail = MAT.yellow; const rh = H + .06;
  for (const z of [-D / 2 + .04, D / 2 - .04]) { mesh(box(L, .04, .04), rail, g, new THREE.Vector3(0, rh + 1.1, z)); mesh(box(L, .03, .03), rail, g, new THREE.Vector3(0, rh + .55, z));
    mesh(box(L, .1, .015), rail, g, new THREE.Vector3(0, rh + .05, z)); for (let x = -L / 2 + .04; x <= L / 2; x += .86) mesh(box(.04, 1.1, .04), rail, g, new THREE.Vector3(x, rh + .55, z)); }
  const ends = e.cell === 1 ? [-1] : [1];
  for (const s of ends) { const x = s * (L / 2 - .04); mesh(box(.04, .04, D), rail, g, new THREE.Vector3(x, rh + 1.1, 0)); mesh(box(.03, .03, D), rail, g, new THREE.Vector3(x, rh + .55, 0));
    for (let z = -D / 2 + .04; z <= D / 2; z += .86) mesh(box(.04, 1.1, .04), rail, g, new THREE.Vector3(x, rh + .55, z)); }
  // access ladder with safety cage on the south face (one per tower)
  if (e.cell === 1) { const lx = .75, lz = D / 2 + .22, y0 = -legH, y1 = rh + 1.1;
    for (const dx of [-.22, .22]) mesh(box(.05, y1 - y0, .05), MAT.galv, g, new THREE.Vector3(lx + dx, (y0 + y1) / 2, lz));
    for (let y = y0 + .3; y < rh; y += .3) mesh(cyl(.014, .44, 8), MAT.galv, g, new THREE.Vector3(lx, y, lz), [0, 0, Math.PI / 2]);
    for (let y = y0 + 2.2; y < y1; y += .7) mesh(new THREE.TorusGeometry(.36, .014, 6, 24, Math.PI), MAT.galv, g, new THREE.Vector3(lx, y, lz), [Math.PI / 2, 0, 0]); }
  // overflow sheets + puddle (alarm), vapour plume
  const fall = new THREE.MeshStandardMaterial({ map: T.fall.clone(), color: 0x3aa0d8, emissive: 0x0b4f78, emissiveIntensity: .6, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide }); fall.map.needsUpdate = true;
  r.parts.fall = []; for (const s of [-1, 1]) { const f = mesh(new THREE.PlaneGeometry(L, 1.6), fall, g, new THREE.Vector3(0, -.3, s * (D / 2 + .03))); f.castShadow = false; r.parts.fall.push(f); }
  r.parts.fallMat = fall;
  const pud = mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshStandardMaterial({ color: 0x5a8fa8, roughness: .05, metalness: .3, transparent: true, opacity: .8 }), g, new THREE.Vector3(0, -legH + .01, 0), [-Math.PI / 2, 0, 0]); pud.visible = false; r.parts.puddle = pud;
  r.parts.plume = particles(70, 0xf2f6f8, 1.1, 0); }
function genericBox(e, mat, cylinder){ const r = equipGroup(e), g = r.g;
  if (cylinder) { mesh(cyl(mm(e.L) / 2, mm(e.H) - .2, 36), own(r, mat), g, new THREE.Vector3(0, mm(e.H) / 2 + .1, 0)); mesh(new THREE.SphereGeometry(mm(e.L) / 2, 30, 14, 0, 6.3, 0, 1.6), own(r, mat), g, new THREE.Vector3(0, mm(e.H) - .1, 0));
    for (let i = 0; i < 3; i++) mesh(box(.06, .25, .06), MAT.steel, g, new THREE.Vector3(Math.cos(i * 2.1) * .3, .1, Math.sin(i * 2.1) * .3)); }
  else if (e.type === 'bypass') { for (const s of [-1, 1]) mesh(box(.1, mm(e.H), mm(e.W)), own(r, MAT.steel), g, new THREE.Vector3(s * (mm(e.L) / 2 - .1), mm(e.H) / 2, 0));
    mesh(box(mm(e.L), .08, .12), own(r, MAT.steel), g, new THREE.Vector3(0, mm(e.H) - .04, 0)); }
  else mesh(box(mm(e.L), mm(e.H), mm(e.W), .03), own(r, mat), g, new THREE.Vector3(0, mm(e.H) / 2, 0));
  if (e.type === 'panel') { const s = lcd(256, 128); mesh(new THREE.PlaneGeometry(mm(e.L) * .32, .19), s.mat, g, new THREE.Vector3(-.2, 1.4, mm(e.W) / 2 + .021)); r.parts.lcd = s; r.parts.panel = g.children[0];
    r.parts.leds = []; for (let i = 0; i < 8; i++) r.parts.leds.push(mesh(new THREE.SphereGeometry(.012, 8, 6), new THREE.MeshStandardMaterial({ color: 0x111, emissive: i % 3 ? 0x22c55e : 0xffb020, emissiveIntensity: 1 }), g, new THREE.Vector3(.15 + (i % 4) * .05, 1.5 - Math.floor(i / 4) * .05, mm(e.W) / 2 + .02))); }
  return r; }
function ahu(e){ const r = equipGroup(e), g = r.g, L = mm(e.L), Wd = mm(e.W), H = mm(e.H), m = own(r, MAT.panel);
  mesh(box(L, H, Wd, .03), m, g, new THREE.Vector3(0, H / 2, 0));
  mesh(box(L * .3, H * .8, .02), new THREE.MeshStandardMaterial({ color: 0x7c8a94, metalness: .6, roughness: .4 }), g, new THREE.Vector3(-L * .25, H / 2, Wd / 2 + .011));   // coil access
  const fan = new THREE.Group(); fan.position.set(L * .25, H / 2, Wd / 2 + .02); g.add(fan); r.spin.push({ m: fan, axis: 'z', fan: true });
  mesh(new THREE.TorusGeometry(H * .32, .03, 8, 32), MAT.steel, g, new THREE.Vector3(L * .25, H / 2, Wd / 2 + .02));
  for (let i = 0; i < 5; i++) mesh(box(H * .55, .07, .02), MAT.black, fan, null, [0, 0, i * Math.PI / 5]);
  const scr = lcd(256, 96); mesh(new THREE.PlaneGeometry(.5, .19), scr.mat, g, new THREE.Vector3(-L * .25, H * .85, Wd / 2 + .03)); r.parts.lcd = scr; return r; }
function fcu(e){ const r = equipGroup(e), g = r.g; mesh(box(mm(e.L), mm(e.H), mm(e.W), .02), own(r, MAT.panel), g, new THREE.Vector3(0, mm(e.H) / 2, 0));
  const fan = new THREE.Group(); fan.position.set(0, -.01, 0); g.add(fan); r.spin.push({ m: fan, axis: 'y', fan: true }); for (let i = 0; i < 3; i++) mesh(box(.5, .01, .06), MAT.black, fan, null, [0, i * 1.05, 0]); return r; }
function fanUnit(e){ const r = equipGroup(e), g = r.g, D = mm(e.L); mesh(cyl(D / 2, mm(e.H), 28), own(r, MAT.galv), g, new THREE.Vector3(0, mm(e.H) / 2, 0));
  const fan = new THREE.Group(); fan.position.set(0, mm(e.H) + .02, 0); g.add(fan); r.spin.push({ m: fan, axis: 'y', fan: true }); for (let i = 0; i < 4; i++) mesh(box(D * .8, .02, .12), MAT.black, fan, null, [0, i * Math.PI / 4, 0]); return r; }
for (const e of [...M.equipment, ...M.air_equipment]) {
  if (e.type === 'chiller') chiller(e); else if (e.type === 'pump') pump(e); else if (e.type === 'ct') coolingTower(e);
  else if (e.type === 'ahu') ahu(e); else if (e.type === 'fcu') fcu(e); else if (e.type === 'fan') fanUnit(e);
  else if (e.type === 'exptank') genericBox(e, MAT.red, true); else if (e.type === 'panel') genericBox(e, MAT.panel); else genericBox(e, MAT.galv); }

// ------------------------------------------------------------------ V7.9 r4: Blender equipment models (window.GLB, base64 GLB per type)
// the procedural body is replaced by the model; animated / alarm parts are taken from the model's named nodes
const GLBS = {}, GLB_WAIT = {};
function glb(name, cb){ const src = (window.GLB || {})[name]; if (!src) return;
  if (GLBS[name]) return cb(GLBS[name]); (GLB_WAIT[name] = GLB_WAIT[name] || []).push(cb); if (GLB_WAIT[name].length > 1) return;
  const bin = Uint8Array.from(atob(src), c => c.charCodeAt(0)).buffer;
  new GLTFLoader().parse(bin, '', g => { const m = g.scene; m.traverse(o => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } }); GLBS[name] = m; GLB_WAIT[name].forEach(f => f(m)); }, err => console.warn('GLB ' + name, err)); }
// reference size of each model [L, W, H] (m); the page scales a model to the R9 size of each unit
const GLB_REF = { chiller: [3.774, 1.771, 2.033], pump: [1.75, .65, .85], ahu: [3.6, 1.8, 2.1], oau: [4.2, 2.0, 2.2], tower: [2.6, 2.6, 2.7],
  roof_fan: [1.2, 1.2, 1.1], exptank: [.9, .9, 1.6], bypass: [1.3, .5, 1.04], panel: [2.4, .5, 2.1] };
function useModel(rec, model, map, name){ const L = mm(rec.e.L), W = mm(rec.e.W), H = mm(rec.e.H), ref = GLB_REF[name || rec.e.type];
  const live = rec.e.type === 'ct';                       // cooling tower: only the static body is replaced (water, fan, plume, rails stay)
  for (const c of [...rec.g.children]) if (!live || c.userData.body) rec.g.remove(c);
  const o = model.clone(true); o.scale.set(L / ref[0], H / ref[2], W / ref[1]); rec.g.add(o); if (!live) rec.mats.clear();
  o.traverse(m => { if (!m.isMesh) return; m.material = m.material.clone(); rec.mats.add(m.material); });
  const node = n => o.getObjectByName(n);
  for (const [part, n] of Object.entries(map)) { const x = node(n); if (x) rec.parts[part] = x; }
  if (rec.parts.screen && rec.parts.lcd) rec.parts.screen.material = rec.parts.lcd.mat;
  if (rec.parts.comp) rec.parts.compY = rec.parts.comp.position.y;
  if (live) { rec.parts.basin = node('casing') || rec.parts.basin; rec.ghost = undefined; return; }
  rec.spin = []; if (rec.e.type === 'pump') for (const n of ['motorFan', 'shaft']) { const x = node(n); if (x) rec.spin.push({ m: x, axis: 'x' }); }
  if (rec.e.type === 'ahu') { const x = node('fanWheel'); if (x) rec.spin.push({ m: x, axis: 'z', fan: true }); }
  if (rec.e.type === 'fan') { const x = node('fanWheel'); if (x) rec.spin.push({ m: x, axis: 'y', fan: true }); }
  if (rec.e.type === 'panel') { const x = node('pilots'); rec.parts.leds = []; if (x) x.traverse(m => { if (m.isMesh) rec.parts.leds.push(m); }); }   // multi-material node = group of meshes
  if (rec.e.type === 'panel' || rec.e.type === 'ahu') { const x = node('screen'); if (x && rec.parts.lcd) x.material = rec.parts.lcd.mat; }
  rec.ghost = undefined; }
for (const id in EQ) { const r = EQ[id], t = r.e.type;
  if (t === 'chiller') glb('chiller', m => useModel(r, m, { comp: 'comp', evap: 'evap', cond: 'cond', panel: 'panel', screen: 'screen', beacon: 'beacon' }));
  else if (t === 'pump') glb('pump', m => useModel(r, m, { motor: 'motor', volute: 'volute' }));
  else if (t === 'ahu') { const n = r.e.L > 3600 ? 'oau' : 'ahu'; glb(n, m => useModel(r, m, { screen: 'screen' }, n)); }
  else if (t === 'ct') glb('tower', m => useModel(r, m, {}, 'tower'));
  else if (t === 'fan') glb('roof_fan', m => useModel(r, m, {}, 'roof_fan'));
  else if (t === 'exptank' || t === 'bypass' || t === 'panel') glb(t, m => useModel(r, m, { panel: 'cabinet' }, t)); }
// roof: steel grillage under the towers + walkway
mesh(box(mm(M.ct_span[1] - M.ct_span[0]) + 3, .25, 3.2), MAT.steel, plant, P3((M.ct_span[0] + M.ct_span[1]) / 2, 6000, ROOFZ + 900));
mesh(box(mm(M.ct_span[1] - M.ct_span[0]) + 3, .05, .9), new THREE.MeshStandardMaterial({ color: 0x6b7378, metalness: .6, roughness: .5 }), plant, P3((M.ct_span[0] + M.ct_span[1]) / 2, 4100, ROOFZ + 30));
// ------------------------------------------------------------------ pipes (real bends, water visible inside), supports, valves & instruments
const PIPE = {}; const YV = new THREE.Vector3(0, 1, 0);
const dnR = dn => mm(dn * 25.4 / 2 * 1.08);                                   // ~ outside radius
const insul = svc => M.service[svc][2] ? .045 : 0;
const WCOL = { CHS: 0x1d6fd6, CHR: 0x46a2f0, CDS: 0x1a8fb0, CDR: 0x3aa6c4, D: 0x7a8a90, MU: 0x4fb9e0 };
const WVS = 'varying vec2 vUv; varying vec3 vN; varying vec3 vV; void main(){ vUv=uv; vec4 mv=modelViewMatrix*vec4(position,1.); vV=-mv.xyz; vN=normalMatrix*normal; gl_Position=projectionMatrix*mv; }';
const WFS = `uniform float ph,len,off,s0,s1,on,ice; uniform vec3 col; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+1.),f.x),f.y);}
void main(){ float s=off+vUv.x*len; float act=on*step(s0,s)*step(s,s1); float u=s-ph*act; float a=vUv.y*6.2832; vec2 q=vec2(cos(a),sin(a));
 float n=n2(vec2(u*2.4,q.x*2.+q.y*1.3+7.))*.6+n2(vec2(u*6.5,q.y*3.-q.x*2.))*.4;
 float st=smoothstep(.55,.95,n2(vec2(u*1.15,q.x*5.+q.y*5.)));
 float bub=step(.993,h(floor(vec2(u*24.,vUv.y*40.))))*act;
 vec3 N=normalize(vN),Vd=normalize(vV); float fr=pow(1.-abs(dot(N,Vd)),2.5); float lam=.55+.45*max(dot(N,normalize(vec3(.3,1.,.4))),0.);
 vec3 c=col*(.45+.55*n)*lam+vec3(.75,.92,1.)*(st*.45*(.35+.65*act)+bub)+fr*vec3(.3,.45,.55);
 c=mix(c,vec3(.86,.94,1.)*(.8+.2*n),ice); c*=mix(.5,1.,max(act,ice));
 gl_FragColor=vec4(c,1.);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
}`;
function splitAt(v, s){ let acc = 0; for (let i = 0; i < v.length - 1; i++) { const d = v[i].distanceTo(v[i + 1]); if (acc + d >= s) { const p = v[i].clone().lerp(v[i + 1], (s - acc) / d); return [[...v.slice(0, i + 1), p], [p, ...v.slice(i + 1)]]; } acc += d; } return [v, null]; }
function pathOf(v, rb){ const path = new THREE.CurvePath(); let cur = v[0].clone();
  for (let i = 1; i < v.length; i++) { const b = v[i];
    if (i < v.length - 1) { const c = v[i + 1], d1 = b.clone().sub(cur).normalize(), d2 = c.clone().sub(b).normalize();
      if (d1.dot(d2) < .999) { const r = Math.min(rb, b.distanceTo(cur) * .48, c.distanceTo(b) * .48), p1 = b.clone().addScaledVector(d1, -r), p2 = b.clone().addScaledVector(d2, r);
        if (p1.distanceTo(cur) > 1e-4) path.add(new THREE.LineCurve3(cur, p1)); path.add(new THREE.QuadraticBezierCurve3(p1, b.clone(), p2)); cur = p2; continue; } }
    if (b.distanceTo(cur) > 1e-4) path.add(new THREE.LineCurve3(cur, b.clone())); cur = b.clone(); }
  return path; }
const shellMat = svc => { const [, col, ins] = M.service[svc]; return new THREE.MeshStandardMaterial(ins ? { color: 0xd8dde1, metalness: .78, roughness: .33 } : { color: new THREE.Color(col), metalness: .3, roughness: .42 }); };
for (const p of M.pipes) { const g = new THREE.Group(); LAYER.piping.add(g); if (p.floor !== undefined && p.floor !== null) onFloor(p.floor, g); const ins = insul(p.svc), mat = shellMat(p.svc);
  const rec = { p, g, mat, rad: dnR(p.dn) + ins, wm: [], ph: 0, segs: [], waters: [] };
  const v = p.pts.map(q => P3(...q)); const red = M.valves.find(x => x.pipe === p.id && x.kind.startsWith('RED_'));
  let pieces = [[v, p.dn, 0]];
  if (red) { const s = mm(red.s), [a, b] = splitAt(v, s); pieces = red.kind === 'RED_C' ? [[a, red.dn, 0], [b, p.dn, s]] : [[a, p.dn, 0], [b, red.dn, s]]; }
  for (const [pp, dn, off] of pieces) { const rad = dnR(dn), path = pathOf(pp, Math.max(.15, mm(dn * 25.4 * 1.5))), len = path.getLength(), seg = Math.max(6, Math.ceil(len / .05));
    const wmat = new THREE.ShaderMaterial({ uniforms: { ph: { value: 0 }, len: { value: len }, off: { value: off }, s0: { value: mm(p.span[0]) }, s1: { value: mm(p.span[1]) }, on: { value: 0 }, ice: { value: 0 },
      col: { value: new THREE.Color(WCOL[p.svc]) } }, vertexShader: WVS, fragmentShader: WFS }); rec.wm.push(wmat);
    const w = new THREE.Mesh(new THREE.TubeGeometry(path, seg, rad * .84, 14, false), wmat); g.add(w); rec.waters.push(w);
    const sh = mesh(new THREE.TubeGeometry(path, seg, rad + ins, 22, false), mat, g); rec.segs.push(sh);
    for (let s = .7; s < len - .3; s += 3) { const b = mesh(new THREE.CylinderGeometry(rad + ins + .005, rad + ins + .005, .16, 22, 1, true), svcMat[p.svc + '_band'], g, path.getPointAt(s / len));
      b.quaternion.setFromUnitVectors(YV, path.getTangentAt(s / len)); } }
  PIPE[p.id] = rec; }
// supports: hangers (overhead), stanchions (low runs), sleepers (roof), riser clamps
const SUP = new THREE.MeshStandardMaterial({ color: 0x8d969c, metalness: .7, roughness: .45 });
const ceilingAt = z => { if (z < 0) return -800; if (z < BLD.f1_h) return BLD.f1_h - BLD.slab; for (let f = 2; f <= BLD.floors; f++) if (z < zOf(f) + BLD.typ_h) return zOf(f) + BLD.typ_h - BLD.slab; return ROOFZ; };
const floorAt = z => { if (z < 0) return -6000; if (z >= ROOFZ) return ROOFZ; if (z < BLD.f1_h) return 0; for (let f = BLD.floors; f >= 2; f--) if (z >= zOf(f)) return zOf(f); return 0; };
const levels = [...Array(BLD.floors - 1).keys()].map(i => zOf(i + 2)).concat([ROOFZ]);
for (const p of M.pipes) { const rr = PIPE[p.id].rad, v = p.pts, G = PIPE[p.id].g;
  for (let i = 0; i < v.length - 1; i++) { const [a, b] = [v[i], v[i + 1]], L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (Math.abs(a[2] - b[2]) > 1) { const lo = Math.min(a[2], b[2]), hi = Math.max(a[2], b[2]);
      for (const z of levels.map(z => z + 300).filter(z => z > lo + 200 && z < hi - 200)) mesh(new THREE.TorusGeometry(rr + .02, .018, 8, 24), SUP, G, P3(a[0], a[1], z), [Math.PI / 2, 0, 0]); continue; }
    if (L < 600) continue; const z = a[2], top = ceilingAt(z), base = floorAt(z);
    for (let s = 500; s < L - 300; s += z > ROOFZ ? 2500 : 3000) { const x = a[0] + (b[0] - a[0]) * s / L, y = a[1] + (b[1] - a[1]) * s / L, ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
      if (z > ROOFZ) mesh(box(.6, Math.max(.05, mm(z - ROOFZ) - rr), .25), MAT.concrete, G, P3(x, y, (ROOFZ + z - rr * 1000) / 2), [0, ang, 0]);
      else if (z - base >= 1500) { mesh(cyl(.009, mm(top - z), 6), SUP, G, P3(x, y, (top + z) / 2)); mesh(new THREE.TorusGeometry(rr + .015, .012, 6, 24), SUP, G, P3(x, y, z), [0, -ang, 0]); }
      else { mesh(cyl(.045, mm(z - base) - rr, 10), SUP, G, P3(x, y, (z - rr * 1000 + base) / 2)); mesh(box(.3, .02, .3), SUP, G, P3(x, y, base + 10)); } } } }
// valves, fittings, instruments.  local frame: y = pipe axis (flow), x = stem (up for horizontal pipes)
const VALVE = [], VPOS = {}; const roomC = P3(R.x / 2, R.y / 2, 0);
function frameQ(pos, dir, stem){ const y = dir.clone().normalize(); const x = stem ? new THREE.Vector3(stem[0], stem[2], -stem[1]) : Math.abs(y.y) > .9 ? roomC.clone().sub(pos).setY(0).normalize() : YV.clone();   // r7: stem from tools/r9_clash.py
  x.sub(y.clone().multiplyScalar(x.dot(y))).normalize(); return new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, y, new THREE.Vector3().crossVectors(x, y))); }
const RUB = new THREE.MeshStandardMaterial({ color: 0x15171a, roughness: .9 });
const dial = canvasTex(128, 128, g => { g.fillStyle = '#f4f4f0'; g.beginPath(); g.arc(64, 64, 62, 0, 7); g.fill(); g.strokeStyle = '#222'; g.lineWidth = 3;
  for (let i = 0; i <= 10; i++) { const a = Math.PI * (.75 + i * .15); g.beginPath(); g.moveTo(64 + Math.cos(a) * 50, 64 + Math.sin(a) * 50); g.lineTo(64 + Math.cos(a) * 58, 64 + Math.sin(a) * 58); g.stroke(); }
  g.fillStyle = '#b91c1c'; g.fillRect(96, 90, 14, 6); });
const DIAL = new THREE.MeshBasicMaterial({ map: dial });
function flange(g, r, y){ mesh(cyl(r * 1.55, .028, 28), MAT.iron, g, new THREE.Vector3(0, y, 0)); }
for (const v of M.valves) { const pr = PIPE[v.pipe]; if (!pr || v.hidden) continue;   /* r7: legacy valves replaced by the R9 PICV */ const pdn = pr.p.dn, ins = insul(pr.p.svc), r = dnR(v.dn || pdn);
  const pos = P3(...v.xyz), dir = P3(...v.dir).sub(P3(0, 0, 0)).normalize(); const g = new THREE.Group(); g.position.copy(pos); g.quaternion.copy(frameQ(pos, dir, v.stem)); pr.g.add(g); g.position.sub(pr.g.position);
  const o = { v, g, pos: ['BFV'].includes(v.kind) ? 1 : 0, tgt: 1, k: v.kind, pr };
  const K = v.kind;
  if (['BFV', 'MBFV', 'MCV', 'CHECK'].includes(K)) { flange(g, r, -.045); flange(g, r, .045); mesh(cyl(r * 1.3, K === 'CHECK' ? .11 : .07, 28), MAT.iron, g);
    if (K !== 'CHECK') { o.disc = mesh(cyl(r * .96, .014, 28), MAT.galv, g); mesh(cyl(.028, r * .5 + .1, 10), MAT.galv, g, new THREE.Vector3(r * 1.3 + .04, 0, 0), [0, 0, Math.PI / 2]); }
    else mesh(box(.05, .05, .05), MAT.iron, g, new THREE.Vector3(r * 1.3, 0, 0));
    if (K === 'BFV') { const h = new THREE.Group(); h.position.set(r * 1.3 + .1, 0, 0); g.add(h); const ll = Math.max(.24, r * 2.2);
      mesh(box(.04, .05, .05), MAT.iron, h); mesh(box(.02, ll, .035), MAT.red, h, new THREE.Vector3(.02, ll / 2 - .03, 0)); o.ind = h; }
    if (K === 'MBFV' || K === 'MCV') { const a = new THREE.Group(); a.position.set(r * 1.3 + .12, 0, 0); g.add(a); o.act = a;
      const am = new THREE.MeshStandardMaterial({ color: K === 'MCV' ? 0x2b5ea0 : 0x5f6b78, metalness: .45, roughness: .4 }); o.am = am;
      mesh(box(.17, .24, .22, .025), am, a, new THREE.Vector3(.085, 0, 0)); mesh(box(.05, .06, .06), MAT.black, a, new THREE.Vector3(.11, -.14, .06));     // actuator + cable gland
      const ind = new THREE.Group(); ind.position.set(.18, 0, 0); a.add(ind); mesh(cyl(.07, .02, 28), new THREE.MeshStandardMaterial({ color: 0x0f1115, transparent: true, opacity: .85 }), ind, null, [0, 0, Math.PI / 2]);
      mesh(box(.014, .11, .024), MAT.yellow, ind, new THREE.Vector3(.012, .02, 0)); mesh(box(.014, .03, .05), MAT.yellow, ind, new THREE.Vector3(.012, .07, 0)); o.ind = ind;
      o.led = mesh(new THREE.SphereGeometry(.016, 10, 8), new THREE.MeshStandardMaterial({ color: 0x111, emissive: 0x22c55e, emissiveIntensity: 1.5 }), a, new THREE.Vector3(.13, .1, .112)); } }
  else if (K === 'STRAINER') { flange(g, r, -r * 1.3); flange(g, r, r * 1.3); mesh(cyl(r * 1.18, r * 2.5, 26), MAT.iron, g);
    const leg = mesh(cyl(r * .75, r * 2.1, 22), MAT.iron, g, new THREE.Vector3(-r * .95, r * .55, 0), [0, 0, Math.PI / 4]); mesh(cyl(r * .85, .03, 22), MAT.iron, leg, new THREE.Vector3(0, r * 1.05, 0));
    mesh(cyl(.012, .1, 8), MAT.galv, leg, new THREE.Vector3(0, r * 1.05 + .05, 0)); }
  else if (K === 'FLEX') { flange(g, r, -r * .95); flange(g, r, r * .95); const f = new THREE.Group(); g.add(f); o.flex = f;
    for (const y of [-r * .32, r * .32]) mesh(new THREE.SphereGeometry(r * 1.28, 24, 14), RUB, f, new THREE.Vector3(0, y, 0)).scale.set(1, .62, 1);
    for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2 + Math.PI / 4; mesh(cyl(.008, r * 2.1, 6), MAT.galv, g, new THREE.Vector3(Math.cos(a) * r * 1.45, 0, Math.sin(a) * r * 1.45)); } }
  else if (K === 'RED_E' || K === 'RED_C') { const R1 = dnR(pdn), R2 = dnR(v.dn), big = K === 'RED_E' ? R1 : R2, sm = K === 'RED_E' ? R2 : R1, ln = Math.max(.12, (R1 - R2) * 6);
    const geo = new THREE.CylinderGeometry(sm, big, ln, 28); if (K === 'RED_E') { const P = geo.attributes.position; for (let i = 0; i < P.count; i++) if (P.getY(i) < 0) P.setX(i, P.getX(i) - (R1 - R2)); P.needsUpdate = true; geo.computeVertexNormals(); }
    mesh(geo, svcMat[pr.p.svc] || MAT.iron, g); flange(g, sm, ln / 2); flange(g, big, -ln / 2); }
  else if (K === 'FM') { flange(g, r, -r * 1.1); flange(g, r, r * 1.1); mesh(cyl(r * 1.2, r * 2, 28), new THREE.MeshStandardMaterial({ color: 0x2a64a8, metalness: .4, roughness: .4 }), g);
    mesh(cyl(.04, .12, 10), MAT.galv, g, new THREE.Vector3(r * 1.2 + .06, 0, 0), [0, 0, Math.PI / 2]); const s = lcd(192, 96);
    mesh(box(.12, .18, .14, .02), MAT.panel, g, new THREE.Vector3(r * 1.2 + .17, 0, 0)); mesh(new THREE.PlaneGeometry(.1, .065), s.mat, g, new THREE.Vector3(r * 1.2 + .17, .02, .071)); o.lcd = s; }
  else if (K === 'PG') { mesh(cyl(.009, r + ins + .08, 8), MAT.galv, g, new THREE.Vector3((r + ins) / 2 + .04, 0, 0), [0, 0, Math.PI / 2]); const d = new THREE.Group(); d.position.set(r + ins + .13, 0, 0); g.add(d);
    mesh(cyl(.055, .03, 28), MAT.galv, d, null, [Math.PI / 2, 0, 0]); mesh(new THREE.CircleGeometry(.05, 28), DIAL, d, new THREE.Vector3(0, 0, .016));
    const nd = new THREE.Group(); nd.position.z = .018; d.add(nd); mesh(box(.004, .042, .003), MAT.black, nd, new THREE.Vector3(0, .018, 0)); o.needle = nd; }
  else if (['TT', 'FS', 'PT'].includes(K)) { mesh(cyl(.012, r + ins + .06, 8), MAT.galv, g, new THREE.Vector3((r + ins) / 2 + .03, 0, 0), [0, 0, Math.PI / 2]);
    mesh(K === 'TT' ? cyl(.035, .05, 16) : box(.08, .09, .08), K === 'FS' ? MAT.motor : MAT.panel, g, new THREE.Vector3(r + ins + .1, 0, 0), K === 'TT' ? [0, 0, Math.PI / 2] : null);
    if (K === 'FS') o.led = mesh(new THREE.SphereGeometry(.01, 8, 6), new THREE.MeshStandardMaterial({ color: 0x111, emissive: 0x22c55e, emissiveIntensity: 0 }), g, new THREE.Vector3(r + ins + .1, .03, .042)); }
  else if (K === 'AAV') { g.quaternion.identity(); const top = Math.abs(dir.y) > .9 ? .02 : r + ins; mesh(cyl(.012, .06, 8), MAT.galv, g, new THREE.Vector3(0, top + .03, 0)); mesh(cyl(.03, .07, 14), MAT.galv, g, new THREE.Vector3(0, top + .09, 0)); }
  else if (K === 'CAP') { const end = v.s < 1 ? -1 : 1; mesh(cyl(r * 1.55, .03, 28), MAT.iron, g, new THREE.Vector3(0, end * .015, 0)); mesh(cyl(r * 1.55, .03, 28), MAT.iron, g, new THREE.Vector3(0, end * .045, 0)); }
  else if (K === 'DRAIN') { const s = -1; mesh(cyl(.016, .14, 8), MAT.galv, g, new THREE.Vector3(s * (r + .06), 0, 0), [0, 0, Math.PI / 2]); mesh(box(.03, .1, .015), MAT.red, g, new THREE.Vector3(s * (r + .1), .04, 0)); }
  if (v.pt) VPOS[v.pt] = o; VALVE.push(o); }
// ------------------------------------------------------------------ particles & effect helpers
function particles(n, color, size, opacity, blending){ const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3));
  const m = new THREE.PointsMaterial({ color, size, map: T.soft, transparent: true, opacity, depthWrite: false, blending: blending || THREE.NormalBlending, sizeAttenuation: true });
  const p = new THREE.Points(geo, m); p.frustumCulled = false; p.userData.seed = Float32Array.from({ length: n }, Math.random); scene.add(p); return p; }
// rain
const rain = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xaecfe0, transparent: true, opacity: .0 }));
{ const n = 6000, a = new Float32Array(n * 6); for (let i = 0; i < n; i++) { const x = Math.random() * 160 - 48, y = Math.random() * 70, z = Math.random() * 160 - 100; a.set([x, y, z, x + .04, y - .55, z], i * 6); }
  rain.geometry.setAttribute('position', new THREE.Float32BufferAttribute(a, 3)); rain.frustumCulled = false; scene.add(rain); }
// clouds
const clouds = []; for (let i = 0; i < 46; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: T.cloud, transparent: true, opacity: 0, depthWrite: false, fog: false }));
  const a = Math.random() * 6.28, r = 120 + Math.random() * 520; s.position.set(Math.cos(a) * r, 70 + Math.random() * 90, Math.sin(a) * r); s.scale.set(220 + Math.random() * 180, 70 + Math.random() * 50, 1); scene.add(s); clouds.push(s); }
// stars
const stars = particles(1200, 0xffffff, 2.2, 0); { const a = stars.geometry.attributes.position.array; for (let i = 0; i < 1200; i++) { const t = Math.random() * 6.28, f = Math.random() * 1.3;
  a.set([Math.cos(t) * Math.cos(f) * 1500, Math.sin(f) * 1500 + 40, Math.sin(t) * Math.cos(f) * 1500], i * 3); } stars.material.sizeAttenuation = false; }
// heat haze plane over the roof
const hazeMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, uniforms: { t: { value: 0 }, k: { value: 0 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
  fragmentShader: 'varying vec2 vUv; uniform float t,k; void main(){ float w=sin(vUv.y*60.+t*4.)*sin(vUv.x*22.-t*2.); float a=k*(.07+.06*w)*(1.-vUv.y); gl_FragColor=vec4(1.,.82,.6,a); }' });
const haze = new THREE.Mesh(new THREE.PlaneGeometry(26, 9), hazeMat); haze.position.set(RX / 2, RH + 6, -RY / 2 + 6); scene.add(haze);
// alarm effect objects (created on demand per equipment)
const FX = {};   // eqId -> {smoke, frost, gas, spark, sprites...}
function fxOf(id){ return FX[id] || (FX[id] = {}); }
function iconSprite(kind, col){ const c = document.createElement('canvas'), g = c.getContext('2d'); c.width = c.height = 128; g.fillStyle = col; g.beginPath(); g.arc(64, 64, 58, 0, 7); g.fill();
  g.strokeStyle = '#fff'; g.lineWidth = 8; g.fillStyle = '#fff'; g.font = '700 74px "Segoe UI",sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  if (kind === 'maint') { g.lineCap = 'round'; g.beginPath(); g.moveTo(40, 88); g.lineTo(78, 50); g.stroke(); g.beginPath(); g.arc(84, 44, 16, -.6, 3.6); g.stroke(); }
  else g.fillText({ sensor: '?', hand: 'H', perf: '!', chem: 'C', airside: '!', valve: 'V', pressure: 'P' }[kind] || '!', 64, 70);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthTest: false, transparent: true })); s.scale.set(.75, .75, 1); s.renderOrder = 10; return s; }
function eqTop(id){ const r = EQ[id]; const b = new THREE.Box3().setFromObject(r.g); return new THREE.Vector3((b.min.x + b.max.x) / 2, b.max.y + .5, (b.min.z + b.max.z) / 2); }
function eqCenter(id){ const b = new THREE.Box3().setFromObject(EQ[id].g); return b.getCenter(new THREE.Vector3()); }
function eqPipes(id){ return Object.values(PIPE).filter(p => p.p.eq.includes(id)); }

// ------------------------------------------------------------------ state, weather, alarms
const V = {}; let DEMO = false; const ACTIVE = new Map();   // alarm name -> alarm
const FAIL = new Set();   // LIVE: points / alarms whose station ORD did not resolve (shown in the mode badge and Point mapping)
const OVR = { on: false, temp: 33, rh: 60, hour: 13 };
function val(k, d){ const v = V[k]; return typeof v === 'number' && !isNaN(v) ? v : (typeof v === 'boolean' ? +v : d); }
function weather(){ const now = new Date(); const W = { temp: val('OA_Temperature', 33), rh: val('OA_Humidity', 62), wb: val('OA_WetBulb', 27), hour: now.getHours() + now.getMinutes() / 60 };
  if (OVR.on) Object.assign(W, { temp: OVR.temp, rh: OVR.rh, hour: OVR.hour, wb: OVR.temp - (100 - OVR.rh) / 5 * .9 });
  W.night = W.hour < 6.1 || W.hour > 18.6; W.rain = W.rh >= 92 && W.temp <= 30; W.fog = W.rh >= 95 && (W.hour < 9 || W.night); W.hot = W.temp >= 36;
  W.cover = Math.max(0, Math.min(1, (W.rh - 50) / 40)) + (W.rain ? .3 : 0);
  W.label = W.night ? (W.rain ? 'Night rain' : 'Night') : W.rain ? 'Rain' : W.fog ? 'Mist' : W.hot ? 'Very hot, strong sun' :
    W.cover > .65 ? 'Overcast' : W.cover > .3 ? 'Partly cloudy' : 'Clear sky'; return W; }
let lastEnv = '';
function applyWeather(W, t){
  const el = THREE.MathUtils.degToRad(Math.max(-20, 78 * Math.sin(Math.PI * (W.hour - 6.2) / 12.4))), az = THREE.MathUtils.degToRad(90 + (W.hour - 6) / 12 * 180);
  const sv = new THREE.Vector3().setFromSphericalCoords(1, Math.PI / 2 - el, az); U.sunPosition.value.copy(sv);
  U.turbidity.value = 4 + W.cover * 10 + (W.hot ? 4 : 0); U.rayleigh.value = W.night ? .2 : 1.4 + W.cover * 1.5;
  sun.position.copy(sv.clone().multiplyScalar(90)).add(sun.target.position); const day = Math.max(0, Math.sin(el)); const dim = 1 - W.cover * .65;
  sun.intensity = (W.night ? 0 : 3.4 * Math.min(1, day * 2.2)) * dim; sun.color.setHSL(.09 + .04 * day, .55, .62 + .25 * day);
  hemi.intensity = W.night ? .22 : .45 + .3 * day; hemi.color.set(W.cover > .6 ? 0xb8c4cc : 0xcfe3ff);
  renderer.toneMappingExposure = W.night ? .5 : .58 + .08 * (1 - W.cover);
  stars.material.opacity = W.night ? .85 * (1 - W.cover) : 0; lampLights.forEach(L => L.intensity = W.night || W.cover > .9 ? 60 : 0);
  storeGlass.material.emissiveIntensity = W.night ? .9 : .05;
  clouds.forEach((c, i) => { c.material.opacity = Math.min(.95, W.cover * (.45 + (i % 5) * .12)); c.material.color.set(W.rain ? 0x8c949b : W.night ? 0x40474f : 0xffffff); c.position.x += Math.sin(i) * .02; });
  rain.material.opacity = W.rain ? .55 : 0; WET.forEach(m => { m.roughness = W.rain ? .18 : (m === MAT.slab ? .9 : m.map === T.asphalt ? .85 : 1); m.color.set(W.rain ? 0x8a8f94 : 0xffffff); });
  scene.fog = W.fog ? new THREE.FogExp2(0xcfd6dc, .0055) : (W.rain ? new THREE.FogExp2(0x8a959d, .006) : new THREE.FogExp2(W.night ? 0x0d1520 : 0x9fb3c4, .0009));
  hazeMat.uniforms.k.value = W.hot ? Math.min(1, (W.temp - 35) / 4) : 0; hazeMat.uniforms.t.value = t;
  const key = [Math.round(W.hour * 4), Math.round(W.cover * 5), W.rain, W.night].join('|');
  if (key !== lastEnv) { lastEnv = key; scene.environment = pmrem.fromScene(skyScene(), .04).texture; }
  $('wx').innerHTML = `<b>${W.label}</b><span>${W.temp.toFixed(1)} °C · RH ${W.rh.toFixed(0)}% · WB ${W.wb.toFixed(1)} °C · ${String(Math.floor(W.hour)).padStart(2, '0')}:${String(Math.floor(W.hour % 1 * 60)).padStart(2, '0')}</span>`; }
const envScene = new THREE.Scene(); const skyCopy = new Sky(); skyCopy.scale.setScalar(1000); envScene.add(skyCopy);
function skyScene(){ for (const k in U) skyCopy.material.uniforms[k].value = U[k].value; return envScene; }

const EFFECT_ORDER = ['power', 'fire', 'leak', 'freeze', 'overflow', 'lowlevel', 'overheat', 'noflow', 'trip', 'vibration', 'pressure', 'valve', 'chem', 'sensor', 'hand', 'maint', 'perf', 'airside'];
function applyAlarms(t){
  const byEq = {}; for (const a of ACTIVE.values()) for (const id of a.e) (byEq[id] = byEq[id] || new Set()).add(a.x);
  const global = new Set([...ACTIVE.values()].map(a => a.x));
  const pulse = .5 + .5 * Math.sin(t * 6);
  for (const id in EQ) { const r = EQ[id], ef = r.ghost ? new Set() : (byEq[id] || new Set()), fx = fxOf(id);
    // emissive tint
    let em = 0x000000, ei = 0; if (ef.has('trip') || ef.has('noflow')) { em = 0xff1a10; ei = .55 * pulse; } else if (ef.has('overheat')) { em = 0xff5a10; ei = .8 * (.6 + .4 * pulse); }
    else if (ef.has('freeze')) { em = 0x6fc3ff; ei = .35; } else if (ef.size && [...ef].some(x => !['maint', 'hand', 'sensor', 'perf'].includes(x))) { em = 0xffa000; ei = .25 * pulse; }
    r.mats.forEach(m => { m.emissive && m.emissive.setHex(em); m.emissiveIntensity = ei; });
    // freeze: frost shell + snow
    if (ef.has('freeze') && r.parts.evap) { if (!fx.frost) { fx.frost = new THREE.Mesh(r.parts.evap.geometry, new THREE.MeshStandardMaterial({ color: 0xe9f6ff, roughness: .25, metalness: 0, transparent: true, opacity: .8, emissive: 0x9fd8ff, emissiveIntensity: .25 }));
        fx.frost.scale.setScalar(1.06); r.parts.evap.add(fx.frost); fx.snow = particles(500, 0xffffff, .05, .9); } fx.frost.visible = true;
      animateCloud(fx.snow, eqCenter(id), 2.2, 1.4, t, -0.4, .9); } else { if (fx.frost) fx.frost.visible = false; if (fx.snow) fx.snow.visible = false; }
    // overheat shimmer / trip smoke / leak gas / fire smoke
    blob(fx, 'heat', ef.has('overheat'), 0xff8a40, .35, .5, THREE.AdditiveBlending, eqTop(id), .9, 1.2, t, .7);
    blob(fx, 'smoke', ef.has('trip') || ef.has('fire'), 0x6d7175, .32, .9, THREE.NormalBlending, eqTop(id), .8, 3, t, .4);
    blob(fx, 'gas', ef.has('leak'), 0xc8ffd8, .9, .35, THREE.NormalBlending, eqCenter(id), 3.2, 1.6, t, .12);
    // vibration
    r.g.position.copy(r.base); if (ef.has('vibration') || ef.has('trip') && id.startsWith('C')) { const k = ef.has('vibration') ? .02 : .006; r.g.position.x += (Math.random() - .5) * k; r.g.position.z += (Math.random() - .5) * k; }
    // cooling tower basin: overflow / low level
    if (r.parts.water && !r.ghost) { const over = ef.has('overflow'), low = ef.has('lowlevel');
      r.parts.water.position.y = over ? .56 : low ? .07 : .45; r.parts.water.material.color.set(low ? 0x7a4a3a : over ? 0x9fd0e0 : 0x8fb8c4);
      r.parts.fallMat.opacity = over ? .9 : 0; r.parts.fallMat.map.offset.y = (t * 1.6) % 1; r.parts.puddle.visible = over; r.parts.puddle.scale.setScalar(over ? 2.2 + Math.sin(t) * .1 : 1);
      blob(fx, 'splash', over, 0xe8f7ff, .95, .14, THREE.NormalBlending, r.g.position.clone().add(new THREE.Vector3(0, .55, 1.35)), 2.4, .9, t, -.6); }
    // icons
    const iconKind = ['sensor', 'hand', 'maint', 'perf', 'chem', 'valve', 'pressure', 'airside'].find(k => ef.has(k));
    if (iconKind && id !== 'BUILDING') { if (!fx.icon || fx.iconKind !== iconKind) { if (fx.icon) scene.remove(fx.icon); fx.icon = iconSprite(iconKind, iconKind === 'sensor' ? '#6b7280' : iconKind === 'maint' ? '#c99400' : iconKind === 'hand' ? '#2563eb' : '#d97706'); fx.iconKind = iconKind; scene.add(fx.icon); }
      fx.icon.visible = true; fx.icon.position.copy(eqTop(id)).add(new THREE.Vector3(0, .5 + .1 * Math.sin(t * 3), 0)); fx.icon.material.opacity = iconKind === 'sensor' ? (Math.random() < .85 ? 1 : .2) : 1; }
    else if (fx.icon) fx.icon.visible = false; }
  // pipes: no flow (red pulse, water stops) / pressure (bulge) / freeze (ice in the chiller's CHW pipes)
  for (const p of Object.values(PIPE)) { p.mat.emissive.setHex(0); p.g.scale.set(1, 1, 1); p.noflow = false; p.ice = false; }
  for (const id in byEq) { const ef = byEq[id]; for (const p of eqPipes(id)) { if (ef.has('noflow')) { p.mat.emissive.setHex(0xff2010); p.mat.emissiveIntensity = .7 * pulse; p.noflow = true; }
    if (ef.has('pressure')) { p.mat.emissive.setHex(0xff6a00); p.mat.emissiveIntensity = .5 * pulse; } if (ef.has('freeze') && /^CH[SR]/.test(p.p.id)) p.ice = true; } }
  // valves that do not follow their command: actuator hunts, LED red
  const vb = new Set(Object.keys(byEq).filter(id => byEq[id].has('valve')).flatMap(id => eqPipes(id).map(p => p.p.id)));
  VALVE.forEach(o => { o.bad = !!o.act && vb.has(o.v.pipe); if (o.am) { o.am.emissive.setHex(o.bad ? 0xff2010 : 0); o.am.emissiveIntensity = o.bad ? pulse : 0; } });
  // global: power / E-stop -> dark + red strobe + sparks at the panel; fire -> smoky room
  const pw = global.has('power'); roomLights.forEach(L => L.intensity = pw ? (Math.sin(t * 10) > .6 ? 0 : 1.5) : 7); strobe.intensity = pw || global.has('fire') ? 60 * (Math.sin(t * 8) > 0 ? 1 : 0) : 0;
  blob(fxOf('CP-01'), 'spark', pw, 0xffe08a, 1, .06, THREE.AdditiveBlending, eqCenter('CP-01').add(new THREE.Vector3(0, .6, .3)), .5, .6, t, 1.8);
  blob(fxOf('ROOM'), 'roomsmoke', global.has('fire'), 0x6a6e72, .45, 1.2, THREE.NormalBlending, P3(R.x / 2, R.y / 2, 2500), 14, 3, t, .1);
  ZALM.clear(); for (const a of ACTIVE.values()) for (const id of a.e) if (id.startsWith('Z-')) ZALM.add(id.slice(2)); }
function blob(fx, key, on, col, op, size, blend, pos, spread, rise, t, speed){ if (!on) { if (fx[key]) fx[key].visible = false; return; } if (!fx[key]) fx[key] = particles(160, col, size, op, blend); animateCloud(fx[key], pos, spread, rise, t, speed, op); }
function animateCloud(p, pos, spread, rise, t, speed, op){ p.visible = true; const a = p.geometry.attributes.position.array, s = p.userData.seed;
  for (let i = 0; i < s.length; i++) { const k = (s[i] + t * Math.abs(speed) * .3) % 1, ang = s[i] * 40;
    a[i * 3] = pos.x + Math.cos(ang) * spread * (.2 + k * .8) * .5; a[i * 3 + 1] = pos.y + (speed >= 0 ? k * rise : -k * rise * 1.8); a[i * 3 + 2] = pos.z + Math.sin(ang) * spread * (.2 + k * .8) * .5; }
  p.geometry.attributes.position.needsUpdate = true; p.material.opacity = op; }
const strobe = new THREE.PointLight(0xff2020, 0, 30, 1.5); strobe.position.copy(P3(R.x / 2, R.y / 2, 4200)); plant.add(strobe);

// ------------------------------------------------------------------ live running state: rotating parts, valves, water in pipes, cooling-tower water
function running(id){ const r = EQ[id]; if (!r || !r.e.run || r.ghost) return false; return !!V[r.e.run]; }
const ZALM = new Set();
const tripped = id => [...ACTIVE.values()].some(a => a.e.includes(id) && a.x === 'trip');
const GPM = 6.309e-5;
const ofType = re => Object.keys(EQ).filter(id => re.test(id));
function pipeQ(p){ const fl = p.fl || '', chw = val('CHWFlow', 0), cdw = val('CDW_Flow', 0), n = a => Math.max(1, a.filter(Boolean).length);
  const chp = n(ofType(/^CHP-/).map(running)), cdp = n(ofType(/^CDP-/).map(running));
  const ev = n(ofType(/^CH-/).map(id => V[`Gfx_${EQ[id].e.pt}Evap_Fwd`])), cd = n(ofType(/^CH-/).map(id => V[`Gfx_${EQ[id].e.pt}Cond_Fwd`]));
  const ct = n([...new Set(M.equipment.filter(e => e.type === 'ct').map(e => e.tower))].map(t => V[`Gfx_${t}_Fwd`]));
  if (/Bypass/.test(fl)) return chw * .12 * (VPOS.Gfx_CHW_BypassMV_Pos ? VPOS.Gfx_CHW_BypassMV_Pos.pos : .2);
  if (/AHU_F/.test(fl)) return chw / 8;
  if (/CHP\d/.test(fl)) return chw / chp; if (/CDP\d/.test(fl)) return cdw / cdp; if (/Evap_/.test(fl)) return chw / ev; if (/Cond_/.test(fl)) return cdw / cd;
  if (/_CT\d/.test(fl)) return cdw / ct / 2; return /^CD/.test(p.svc) ? cdw : chw; }
function demoFlows(){ const pos = k => VPOS[k] ? VPOS[k].pos : 0, on = id => running(id);
  const chw = ofType(/^CHP-/).some(on), cdw = ofType(/^CDP-/).some(on);
  Object.assign(V, { Gfx_ChwMain_Fwd: chw, Gfx_EvapTotal_Fwd: chw, Gfx_CdwTotal_Fwd: cdw, Gfx_Bypass_Fwd: chw && pos('Gfx_CHW_BypassMV_Pos') > .05 });
  for (const id of ofType(/^C[HD]P-/)) { const P = EQ[id].e.pt, i = +P.slice(-2); V[`Gfx_${P}_Fwd`] = on(id) && pos(i <= 2 ? `Gfx_${P}_DischargeMV_Pos` : `Gfx_${P}_MV_Pos`) > .3; }
  for (const id of ofType(/^CH-/)) { const c = EQ[id].e.pt; V[`Gfx_${c}Evap_Fwd`] = chw && pos(`Gfx_${c}_ChwIso_Pos`) > .3; V[`Gfx_${c}Cond_Fwd`] = cdw && pos(`Gfx_${c}_CdwIso_Pos`) > .3; }
  for (const t of new Set(M.equipment.filter(e => e.type === 'ct').map(e => e.tower))) { const i = +t.slice(-2); V[`Gfx_${t}_Fwd`] = cdw && pos(i <= 2 ? `Gfx_${t}_InletMV_Pos` : `Gfx_${t}_Valve_Pos`) > .3; }
  for (let f = 2; f <= BLD.floors; f++) V[`Gfx_AHU_F${String(f).padStart(2, "0")}_Fwd`] = chw && val(`AHU_F${String(f).padStart(2, "0")}_ValveCmd`, 0) > 2; }
let lcdT = 0;
function animate(t, dt){
  if (DEMO) demoFlows();
  for (const id in EQ) { const r = EQ[id]; if (r.ghost) continue; const runs = running(id) && !tripped(id);
    const spd = r.e.pt ? val(r.e.pt + 'SpeedCmd', 100) / 100 : 1; r.spin.forEach(s => { s.m.rotation[s.axis] += (runs ? (s.fan ? 9 : 40) * spd : 0) * dt; });
    if (r.e.type === 'pump' && runs) { r.g.position.y = r.base.y + Math.sin(t * 90) * .0012; }
    if (r.e.type === 'chiller') { r.parts.comp.position.y = (r.parts.compY ?? 1.72) + (runs ? Math.sin(t * 70) * .0015 : 0); r.parts.beacon.material.emissive.setHex(tripped(id) ? 0xff2020 : 0x22c55e);
      r.parts.beacon.material.emissiveIntensity = tripped(id) ? (Math.sin(t * 8) > 0 ? 2.5 : 0) : runs ? 2 : 0; }
    if (r.e.type === 'ct') { const tw = r.e.tower, flow = !!V[`Gfx_${tw}_Fwd`] && !tripped(id), W = weather();
      r.parts.curtain.opacity = flow ? .62 : 0; r.parts.curtain.map.offset.y = (r.parts.curtain.map.offset.y + dt * 1.6) % 1;
      r.parts.water.material.map.offset.x += dt * (flow ? .05 : .006); r.parts.water.material.map.offset.y += dt * (flow ? .03 : .004);
      r.parts.hot.forEach(m => { m.opacity = flow ? .9 : .25; m.map.offset.y += dt * .08; });
      const vis = runs ? Math.min(1, .15 + Math.max(0, (W.rh - 55) / 45) + Math.max(0, (30 - W.temp) / 12)) : 0;
      if (vis > .02) { const o = r.g.localToWorld(r.parts.outlet.clone()); const pl = r.parts.plume; pl.visible = true; const a = pl.geometry.attributes.position.array, sd = pl.userData.seed;
        for (let i = 0; i < sd.length; i++) { const k = (sd[i] + t * .18 * spd) % 1, j = sd[(i * 7) % sd.length] - .5;
          a[i * 3] = o.x + j * (.5 + k * 2.2); a[i * 3 + 1] = o.y + k * k * 4.5 + k * .4; a[i * 3 + 2] = o.z - k * 2.6 * spd + (sd[(i * 3) % sd.length] - .5) * k * 1.5; }
        pl.geometry.attributes.position.needsUpdate = true; pl.material.opacity = .14 * vis; pl.material.size = 1.4; } else r.parts.plume.visible = false; } }
  // valves: actuators stroke to the station position (Gfx_*_Pos), LED: green open / red closed / amber moving
  VALVE.forEach(o => { if (o.v.pt && (o.k === 'MBFV' || o.k === 'MCV')) { let x = V[o.v.pt]; if (typeof x === 'boolean') x = x ? 100 : 0; if (typeof x === 'number') o.tgt = Math.max(0, Math.min(1, x / 100)); }
    if (o.bad) o.tgt = .45 + .25 * Math.sin(t * 1.7);
    const d = o.tgt - o.pos, moving = Math.abs(d) > .01; o.pos += Math.sign(d) * Math.min(Math.abs(d), (o.k === 'MCV' ? .3 : .22) * dt);
    if (o.disc) o.disc.rotation.x = o.pos * Math.PI / 2; if (o.ind) o.ind.rotation.x = (1 - o.pos) * Math.PI / 2;
    if (o.led && o.k !== 'FS') { o.led.material.emissive.setHex(o.bad ? 0xff2020 : moving ? 0xffb020 : o.pos > .5 ? 0x22c55e : 0xef4444); o.led.material.emissiveIntensity = (moving || o.bad) ? (Math.sin(t * 12) > 0 ? 2.5 : .2) : 1.6; }
    const pf = o.pr.flow; if (o.k === 'FS') o.led.material.emissiveIntensity = pf ? 2 : 0;
    if (o.needle) { const base = /-(D\d|DH|C\d|EM|M)$/.test(o.v.pipe) || /^CHR-E|^CDS-C/.test(o.v.pipe) ? .75 : .35; o.needle.rotation.z = -(pf ? base + Math.sin(t * 23 + o.g.id) * .01 : .08) * 4 + 2.3; }
    if (o.flex) o.flex.scale.setScalar(pf ? 1 + Math.sin(t * 60) * .012 : 1); });
  // water: velocity = Q / A (gpm -> m/s), phase integrated so a change of speed never jumps
  const clear = $('flow').checked;
  for (const id in PIPE) { const p = PIPE[id], P = p.p; let f = P.fl ? (V[P.fl.replace('_Fwd', '_Rev')] === true ? -1 : V[P.fl] ? 1 : 0) : 0; if (p.noflow) f = 0;
    const A = Math.PI * (P.dn * .0254 / 2) ** 2, vel = Math.min(3.5, pipeQ(P) * GPM / A); p.flow = !!f; p.ph += f * vel * dt;
    p.wm.forEach(m => { m.uniforms.ph.value = p.ph; m.uniforms.on.value = f ? 1 : 0; m.uniforms.ice.value = p.ice ? 1 : 0; });
    if (p.clear !== clear) { p.clear = clear; p.oc = p.oc || p.mat.color.clone(); p.mat.color.copy(clear ? new THREE.Color(0xe4edf3) : p.oc); p.mat.metalness = clear ? .1 : (M.service[P.svc][2] ? .78 : .3); p.mat.needsUpdate = true; }
    if (!p.ghost) { p.mat.transparent = clear; p.mat.opacity = clear ? .22 : 1; p.mat.depthWrite = !clear; } p.waters.forEach(w => w.visible = clear && !w.userData.hide); }
  if ((lcdT += dt) > .5) { lcdT = 0; VALVE.forEach(o => { if (o.lcd) o.lcd.draw([o.v.tag, (val(o.v.pt, 0)).toFixed(0) + ' gpm']); });
    for (const id of ofType(/^CH-/)) { if (EQ[id].ghost) { EQ[id].parts.lcd.draw([id, 'NOT INSTALLED', ''], '#1a1d22', '#6b7280'); continue; } const p = EQ[id].e.pt, on = running(id); EQ[id].parts.lcd.draw(on ? [`${id} RUN`, `LWT ${val(p + '_ChwSupplyTemp', 6.7).toFixed(1)} C`, `Load ${val(p + 'LoadPct', 0).toFixed(0)} %`] : [`${id}`, 'STANDBY', ''], '#061a2a', on ? '#7fe3ff' : '#8899a6'); }
    for (const id of ofType(/^AHU-/)) { const r = EQ[id], p = r.e.pt, on = running(id); r.parts.lcd && r.parts.lcd.draw([id + (on ? ' RUN' : ' OFF'), `Valve ${val(p + '_ValveCmd', 0).toFixed(0)} %`]); }
    const cp = EQ['CP-01']; cp.parts.lcd.draw(['CPMS ' + (DEMO ? 'DEMO' : 'LIVE'), `kW/RT ${val('Plant_kW_per_RT', 0).toFixed(2)}`, `RT ${val('CoolingLoad_RT', 0).toFixed(0)}`]);
    cp.parts.leds.forEach((l, i) => l.material.emissiveIntensity = Math.random() < .7 ? 1.4 : 0); }
  renderKpi(); }
function renderKpi(){ const k = $('kpi'); if (!k) return; const f = (n, d) => val(n, NaN).toFixed(d);
  k.innerHTML = `<div class="big"><span>PLANT EFFICIENCY</span><b>${f('Plant_kW_per_RT', 2)}</b><i>kW/RT</i></div>
  <div><span>Cooling load</span><b>${f('CoolingLoad_RT', 0)}</b><i>RT</i></div><div><span>Plant power</span><b>${f('Plant_kW', 0)}</b><i>kW</i></div>
  <div><span>CHWS / CHWR</span><b>${f('CHWS', 1)} / ${f('CHWR', 1)}</b><i>°C</i></div><div><span>CDS / CDR</span><b>${f('CDS', 1)} / ${f('CDR', 1)}</b><i>°C</i></div>
  <div><span>CHW / CDW flow</span><b>${f('CHWFlow', 0)} / ${f('CDW_Flow', 0)}</b><i>gpm</i></div>`; }

// ------------------------------------------------------------------ HTML overlay: labels, alarm list, info panel
const LBL = {}; for (const e of [...M.equipment, ...M.air_equipment]) { const d = document.createElement('div'); d.className = 'lbl'; d.innerHTML = `<b>${e.id}</b><span></span>`; $('labels').appendChild(d);
  d.onclick = () => info(e.id); LBL[e.id] = d; }
let LBLT = 0;
function placeLabels(){ const w = host.clientWidth, h = host.clientHeight, shown = []; for (const id in LBL) { const p = eqTop(id).project(camera); const d = LBL[id]; d.__p = p;
  const far = camera.position.distanceTo(eqTop(id)) > 60 && ![...ACTIVE.values()].some(a => a.e.includes(id));
  if (p.z > 1 || !$('labelsOn').checked || far || !EQ[id].g.visible || !EQ[id].g.parent.visible) { d.style.display = 'none'; continue; }
  if (EQ[id].ghost) { d.style.display = ''; d.style.transform = `translate(${(p.x + 1) / 2 * w}px,${(1 - p.y) / 2 * h}px) translate(-50%,-100%)`; d.className = 'lbl ghost'; d.querySelector('span').textContent = 'Not installed (empty slot)'; shown.push(id); continue; } d.style.display = ''; d.style.transform = `translate(${(p.x + 1) / 2 * w}px,${(1 - p.y) / 2 * h}px) translate(-50%,-100%)`;
  const r = EQ[id], al = [...ACTIVE.values()].filter(a => a.e.includes(id)); const run = running(id);
  d.className = 'lbl' + (al.some(a => ['Critical', 'Emergency'].includes(a.c)) ? ' alm' : al.length ? ' warn' : run ? ' run' : '');
  d.querySelector('span').textContent = al.length ? (EFX[al[0].x][0] + (al.length > 1 ? ` +${al.length - 1}` : '')) : r.e.pt ? (run ? statusText(id) : 'Off / Standby') : ''; shown.push(id); }
  // r7: no overlapping equipment labels - alarms first, then the nearest; a label that would cover one already placed is hidden
  const now = performance.now(); if (now - LBLT < 150) { for (const id of shown) if (LBL[id].__hid) LBL[id].style.display = 'none'; return; } LBLT = now;
  const rank = id => (/ alm/.test(LBL[id].className) ? 0 : / warn/.test(LBL[id].className) ? 1e4 : 2e4) + camera.position.distanceTo(eqTop(id)) - (LBL[id].__hid === false ? 8 : 0);   // shown labels keep their place
  const placed = [];
  for (const id of shown.sort((a, b) => rank(a) - rank(b))) { const d = LBL[id], p = d.__p, x = (p.x + 1) / 2 * w, y = (1 - p.y) / 2 * h, lw = d.offsetWidth, lh = d.offsetHeight;
    const r = [x - lw / 2, y - lh, x + lw / 2, y], hit = placed.some(q => r[0] < q[2] + 4 && r[2] > q[0] - 4 && r[1] < q[3] + 2 && r[3] > q[1] - 2);
    d.__hid = hit; if (hit) d.style.display = 'none'; else placed.push(r); } }
function statusText(id){ const e = EQ[id].e, p = e.pt; if (e.type === 'ahu') return `Valve ${val(p + '_ValveCmd', 0).toFixed(0)}% · ${e.floor > 8 ? 'roof' : 'floor ' + e.floor}`;
  if (e.type === 'fcu' || e.type === 'fan') return 'Run'; if (id.startsWith('CH-')) return `Load ${val(p + 'LoadPct', 0).toFixed(0)}% · LWT ${val(p + '_ChwSupplyTemp', 6.7).toFixed(1)}°C`;
  return `Run · ${val(p + 'SpeedCmd', 0).toFixed(0)}%`; }
function info(id){ const e = [...M.equipment, ...M.air_equipment].find(x => x.id === id), al = AL.filter(a => a.e.includes(id));
  $('info').innerHTML = `<h3>${id}</h3><table>${Object.entries(e.data).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join('')}</table>
  <h4>Alarms of this unit (${al.length})</h4><div class="alist">${al.map(a => `<div class="${ACTIVE.has(a.n) ? 'on' : ''}" data-n="${a.n}"><i>${EFX[a.x][0]}</i>${a.t}</div>`).join('')}</div>`;
  $('info').className = 'open'; $('info').querySelectorAll('[data-n]').forEach(d => d.onclick = () => { if (DEMO) toggleAlarm(d.dataset.n); info(id); }); }
function renderAlarmList(){ const list = [...ACTIVE.values()]; $('acount').textContent = list.length; $('acount').className = list.length ? 'n on' : 'n';
  $('alist').innerHTML = list.length ? list.map(a => `<div class="${a.c}"><b>${a.e.join(', ')}</b> ${a.t}<i>${EFX[a.x][0]} / ${EFX[a.x][1]}</i></div>`).join('') : '<div class="none">No active alarm</div>'; }
function toggleAlarm(n, on){ const a = AL.find(x => x.n === n); if (!a) return; if (on ?? !ACTIVE.has(n)) ACTIVE.set(n, a); else ACTIVE.delete(n); renderAlarmList(); }
const ray = new THREE.Raycaster(), mp = new THREE.Vector2();
renderer.domElement.addEventListener('dblclick', ev => { const b = renderer.domElement.getBoundingClientRect(); mp.set((ev.clientX - b.left) / b.width * 2 - 1, -(ev.clientY - b.top) / b.height * 2 + 1);
  ray.setFromCamera(mp, camera); const hit = ray.intersectObjects([...plant.children, ...LAYER.air.children], true)[0]; let o = hit && hit.object; while (o && !o.userData.eq) o = o.parent; if (o) { const c = new THREE.Box3().setFromObject(o).getCenter(new THREE.Vector3()), d = camera.position.clone().sub(controls.target).setLength(9); flyTo(c.clone().add(d).toArray(), c.toArray()); return info(o.userData.eq); }
  const zh = ray.intersectObjects(LAYER.zones.children, true).find(h => h.object.userData.zone); if (zh) { const c = zh.object.position, d = camera.position.clone().sub(controls.target).setLength(22); flyTo(c.clone().add(d).toArray(), c.toArray()); zoneInfo(zh.object.userData.zone); } });
function zoneInfo(code){ const z = ZONE[code].z, al = AL.filter(a => a.e.includes('Z-' + code));
  $('info').innerHTML = `<h3>Zone ${code} · ${z.name}</h3><table><tr><td>Floor</td><td>${z.floor}</td></tr><tr><td>Temperature</td><td>${val(z.t, NaN).toFixed(1)} °C</td></tr><tr><td>Humidity</td><td>${val(z.h, NaN).toFixed(0)} %RH</td></tr><tr><td>CO2</td><td>${val(z.c, NaN).toFixed(0)} ppm</td></tr><tr><td>Out of service</td><td>${V[z.oos] ? 'Yes' : 'No'}</td></tr><tr><td>Station point</td><td>${z.t}<br>${z.h}<br>${z.c}</td></tr></table><h4>Alarm (${al.length})</h4><div class="alist">${al.map(a => `<div class="${ACTIVE.has(a.n) ? 'on' : ''}">${a.t}</div>`).join('')}</div>`; $('info').className = 'open'; }

// ------------------------------------------------------------------ controls (demo simulator, weather override, views)
const gal = $('gallery'); EFFECT_ORDER.forEach(k => { const b = document.createElement('button'); b.textContent = EFX[k][0]; b.title = EFX[k][1];
  b.onclick = () => { const a = AL.find(x => x.x === k && (k === 'airside' || x.e[0] !== 'BUILDING')) || AL.find(x => x.x === k); if (a) toggleAlarm(a.n); }; gal.appendChild(b); });
$('asel').innerHTML = '<option value="">— pick any alarm (all ' + AL.length + ' entries) —</option>' + EFFECT_ORDER.map(k => `<optgroup label="${EFX[k][0]} / ${EFX[k][1]}">${AL.filter(a => a.x === k).map(a => `<option value="${a.n}">${a.e.join(',')} · ${a.t}</option>`).join('')}</optgroup>`).join('');
$('asel').onchange = e => { if (e.target.value) toggleAlarm(e.target.value); e.target.value = ''; };
$('aclear').onclick = () => { ACTIVE.clear(); renderAlarmList(); };
for (const k of ['temp', 'rh', 'hour']) $('w_' + k).oninput = e => { OVR[k] = +e.target.value; OVR.on = true; $('wovr').checked = true; };
$('wovr').onchange = e => OVR.on = e.target.checked;
$('xray').onchange = e => { XRAY.forEach(m => { m.opacity = e.target.checked ? .16 : 1; m.depthWrite = !e.target.checked; }); glassM.opacity = e.target.checked ? .14 : .42; glassM.depthWrite = false; }; $('xray').onchange({ target: $('xray') });
const VIEWS = { iso: [[112, 84, 82], [32, 14, -20], 'all'], plant: [[40, 20, 20], [20, 1, -9], '1'], pumps: [[51, 12, 5], [37, 1, -7], '1'], room: [[1.5, 1.7, -13.6], [20, 1.2, -10.5], '1'], roof: [[54, 58, 28], [26, 36, -6], 'all'], floor: [[70, 40, 40], [32, 22, -20], '5'], site: [[150, 110, 120], [32, 10, -20], 'all'] };
if (BASEMENT) { const pl = M.equipment.filter(e => e.z < -1000), c = pl.reduce((a, e) => [a[0] + e.x / pl.length, a[1] + e.y / pl.length], [0, 0]), t = P3(c[0], c[1], B1Z + 1200);
  const pu = pl.filter(e => e.type === 'pump'), cp = pu.length ? pu.reduce((a, e) => [a[0] + e.x / pu.length, a[1] + e.y / pu.length], [0, 0]) : c, tp = P3(cp[0], cp[1], B1Z + 800);
  VIEWS.plant = [[t.x + 14, t.y + 13, t.z + 16], t.toArray(), '0']; VIEWS.pumps = [[tp.x + 7, tp.y + 7, tp.z + 9], tp.toArray(), '0'];
  VIEWS.room = [[t.x - 12, t.y + 1.2, t.z + 4], t.toArray(), '0']; }
document.querySelectorAll('[data-view]').forEach(b => b.onclick = () => { const [p, tg, f] = VIEWS[b.dataset.view]; flyTo(p, tg); if (f && typeof applyFloor === 'function') { FSEL = f; $('fsel').value = f; applyFloor(); } });

// ------------------------------------------------------------------ data: BajaScript (station) or DEMO
// ------------------------------------------------------------------ data: BajaScript (station) or DEMO
function demoTick(){ const t = Date.now() / 1000, h = new Date().getHours() + new Date().getMinutes() / 60, s = Math.sin, ph = Math.floor(t / 50) % 3;
  try { if (DEVS) DEVS.demo(t); } catch (e) { /* device layer not built yet */ }
  const inst = slot => (M.installed[slot] ?? false), chs = Object.keys(M.installed).filter(k => /^CH\d/.test(k) && inst(k));
  const nCh = Math.min(chs.length, [1, 2, 3][ph]), runCh = chs.slice(0, nCh), load = 270 * nCh + 25 * s(t / 30);
  Object.assign(V, { OA_Temperature: 30 + 5 * s(Math.PI * (h - 9) / 12), OA_Humidity: 66 - 14 * s(Math.PI * (h - 9) / 12), OA_WetBulb: 26.5,
    CHWFlow: load * 2.4 + 20 * s(t / 9), CDW_Flow: 1000 * nCh, CHWS: 6.7 + .1 * s(t / 20), CHWR: 12.1 + .2 * s(t / 25), CDS: 29.6 + .3 * s(t / 40), CDR: 34.4 + .3 * s(t / 40),
    CoolingLoad_RT: load, Plant_kW: load * (.79 + .03 * s(t / 60)), Plant_kW_per_RT: .79 + .03 * s(t / 60), Gfx_CHW_BypassMV_Pos: nCh > 1 ? 6 : 22 + 10 * s(t / 7) });
  for (const k in M.installed) V[k + '_Installed'] = M.installed[k];
  for (const c of Object.keys(M.installed).filter(k => /^CH\d/.test(k))) { const on = runCh.includes(c), i = +c.slice(2);
    Object.assign(V, { [c + 'RunProof']: on, [c + 'LoadPct']: on ? 78 + 5 * s(t / 40 + i) : 0, [c + '_ChwSupplyTemp']: on ? 6.7 + .1 * s(t / 20) : 12, [`Gfx_${c}_ChwIso_Pos`]: on ? 100 : 0, [`Gfx_${c}_CdwIso_Pos`]: on ? 100 : 0 });
    if (i <= 2) Object.assign(V, { [`Gfx_${c}_ChwFCV_Pos`]: on ? 70 + 12 * s(t / 11) : 0, [`Gfx_${c}_CdwHPV_Pos`]: on ? 60 + 20 * s(t / 15) : 0 }); }
  for (const k of ['CHP', 'CDP', 'CT']) { const sl = Object.keys(M.installed).filter(x => new RegExp('^' + k + '\\d').test(x) && inst(x)).slice(0, nCh);
    for (const u of Object.keys(M.installed).filter(x => new RegExp('^' + k + '\\d').test(x))) { const on = sl.includes(u), i = +u.slice(-2);
      if (k === 'CT') { if (i <= 2) for (const c of ['01', '02']) Object.assign(V, { [`${u}_${c}RunProof`]: on, [`${u}_${c}SpeedCmd`]: on ? 70 : 0 }); else Object.assign(V, { [u + 'RunProof']: on, [u + 'SpeedCmd']: on ? 70 : 0 });
        Object.assign(V, i <= 2 ? { [`Gfx_${u}_InletMV_Pos`]: on ? 100 : 0, [`Gfx_${u}_OutletMV_Pos`]: on ? 100 : 0 } : { [`Gfx_${u}_Valve_Pos`]: on ? 100 : 0 }); }
      else Object.assign(V, { [u + 'RunProof']: on, [u + 'SpeedCmd']: on ? 80 : 0 }, i <= 2 ? { [`Gfx_${u}_SuctionMV_Pos`]: on ? 100 : 0, [`Gfx_${u}_DischargeMV_Pos`]: on ? 100 : 0 } : { [`Gfx_${u}_MV_Pos`]: on ? 100 : 0 }); } }
  const occ = h > 7 && h < 20;
  for (const e of M.air_equipment) { const on = occ || e.type === 'fan' && /EF/.test(e.id); V[e.run] = on; if (e.type === 'ahu') V[e.pt + '_ValveCmd'] = on ? 55 + 20 * s(t / 23 + e.floor) : 0; }
  for (const z of M.zones) { const k = z.floor * 7 + +z.code.slice(-2); V[z.t] = (occ ? 24 : 27.5) + 1.4 * s(t / 37 + k) + (k % 5 === 0 ? 2.2 : 0); V[z.h] = 58 + 8 * s(t / 45 + k); V[z.c] = (occ ? 720 : 480) + 180 * s(t / 53 + k) + (k % 6 === 0 ? 380 : 0); } }
let DEMO_ID = 0;
function startDemo(){ if (DEMO) return; DEMO = true; $('mode').textContent = 'DEMO · 1 → 2 → 3 chillers every 50 s (installed slots only)'; $('mode').className = 'mode demo'; demoTick(); DEMO_ID = setInterval(demoTick, 1000); $('sim').style.display = ''; }
function offline(){ if (DEMO) { clearInterval(DEMO_ID); DEMO = false; } $('mode').textContent = 'OFFLINE · no data from the station'; $('mode').className = 'mode offline'; $('sim').style.display = 'none'; }
const SERVED = /^https?:$/.test(location.protocol) && !/[?&]demo\b/.test(location.search);   // served by the station: never fall back to DEMO numbers
function startLive(){ const ready = window.BAJA_READY; if (!ready || !SERVED) return startDemo(); let ok = false; setTimeout(() => { if (!ok) offline(); }, 7000);
  ready.then(() => window.require(['baja!'], function (baja) { ok = true; if (DEMO) { clearInterval(DEMO_ID); DEMO = false; $('sim').style.display = 'none'; ACTIVE.clear(); }
    $('mode').textContent = 'LIVE · station data'; $('mode').className = 'mode live';
    const sub = new baja.Subscriber(); const KEY = new Map();   // component -> Set of keys (one point can be both a value and an alarm source)
    sub.attach('changed', function (prop) { if (prop.getName() === 'out') read(this); });
    function read(c){ for (const k of KEY.get(c) || []) read1(c, k); }
    function read1(c, k){ try { const o = c.get('out'), v = o.getValue(), st = o.getStatus();
      if (k.alarm) { const a = k.alarm; const on = (st && st.isAlarm && st.isAlarm()) || (typeof v === 'boolean' && v === a.av); if (on) ACTIVE.set(a.n, a); else ACTIVE.delete(a.n); renderAlarmList(); }
      else V[k.v] = v; } catch (e) {} }
    const all = [...Object.entries(PTS).map(([k, s]) => ({ s, v: k })), ...AL.filter(a => a.s).map(a => ({ s: a.s, alarm: a }))];
    const BY = new Map(); for (const k of all) { const o = 'station:|slot:' + k.s; if (!BY.has(o)) BY.set(o, []); BY.get(o).push(k); }
    const attach = (o, c) => { if (!c) return failed(o); if (!KEY.has(c)) KEY.set(c, new Set()); BY.get(o).forEach(k => { KEY.get(c).add(k); FAIL.delete(k.v || k.alarm.n); }); read(c); };
    const failed = o => BY.get(o).forEach(k => FAIL.add(k.v || k.alarm.n));
    const one = o => baja.Ord.make(o).get({ subscriber: sub }).then(c => attach(o, c), () => failed(o));
    const ords = [...BY.keys()], CHUNK = 200, jobs = [];
    for (let i = 0; i < ords.length; i += CHUNK) {          // one network call per chunk; any problem -> resolve that chunk one by one
      const part = ords.slice(i, i + CHUNK);
      let p;
      try { const b = new baja.BatchResolve(part);
        p = Promise.resolve(b.resolve({ subscriber: sub })).then(() => part.forEach((o, j) => (typeof b.isResolved !== 'function' || b.isResolved(j)) ? attach(o, b.get(j)) : failed(o))); }
      catch (e) { p = Promise.reject(e); }
      jobs.push(p.catch(() => Promise.all(part.map(one))));
    }
    Promise.all(jobs).then(() => { if (!FAIL.size) return; $('mode').textContent = `LIVE · station data · ${FAIL.size} points not resolved (see Point mapping)`; $('mode').className = 'mode live warn';
      console.warn('3D LIVE: ORDs not resolved', [...FAIL]); });
  }, () => { ok = true; offline(); }), () => { ok = true; offline(); }); }
startLive();

// ------------------------------------------------------------------ installed / not installed (ghost), zones, future systems, floor filter, layers
const GHOST = new THREE.MeshStandardMaterial({ color: 0x9aa3ab, transparent: true, opacity: .16, depthWrite: false, roughness: 1, metalness: 0, envMapIntensity: 0 });   // no sky tint
function setGhost(group, on){ group.traverse(o => { if (!o.isMesh || o.material === GHOST && on) return;
  if (on) { if (!o.userData.orig) o.userData.orig = o.material; o.material = GHOST; o.castShadow = false; } else if (o.userData.orig) { o.material = o.userData.orig; o.castShadow = true; } }); }
const isInst = (slot, dflt) => V[slot + '_Installed'] === undefined ? dflt : !!V[slot + '_Installed'];
function updateGhosts(){ for (const id in EQ) { const r = EQ[id]; if (!r.e.slot) continue; const g = !isInst(r.e.slot, r.e.installed);
    if (g !== r.ghost) { r.ghost = g; setGhost(r.g, g); } }
  for (const id in PIPE) { const p = PIPE[id]; if (!p.p.slot) continue; const g = !isInst(p.p.slot, M.installed[p.p.slot]);
    if (g !== p.ghost) { p.ghost = g; setGhost(p.g, g); p.waters.forEach(w => w.userData.hide = g); } } }
// zones: translucent volume per zone, colour = temperature, label = temperature / humidity
const ZONE = {};
let METRIC = 't';    // zone colour: t temperature / h humidity / c CO2
const MRANGE = { t: [21, 29, '°C', 1], h: [40, 80, '%RH', 0], c: [400, 1200, 'ppm', 0] };
function zoneColor(v, oos, m = 't'){ if (oos || typeof v !== 'number' || isNaN(v)) return new THREE.Color(0x8a8f96);
  const [a, b] = MRANGE[m], k = Math.max(0, Math.min(1, (v - a) / (b - a))); return new THREE.Color().setHSL(.62 - .62 * k, .75, .5); }
for (const z of M.zones) { const z0 = zOf(z.floor) + 60, h = 2800, g = new THREE.Group(); LAYER.zones.add(g); onFloor(z.floor, g);
  const mat = new THREE.MeshStandardMaterial({ color: 0x22c55e, transparent: true, opacity: .16, depthWrite: false, roughness: .9, emissive: 0x000000 });
  const m = mesh(box(mm(z.x1 - z.x0) - .4, mm(h), mm(z.y1 - z.y0) - .4), mat, g, P3((z.x0 + z.x1) / 2, (z.y0 + z.y1) / 2, z0 + h / 2)); m.castShadow = false; m.userData.zone = z.code;
  const edge = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .35 })); edge.position.copy(m.position); g.add(edge);
  const c = document.createElement('canvas'); c.width = 512; c.height = 160; const tex = new THREE.CanvasTexture(c);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthWrite: false, depthTest: false, transparent: true })); sp.scale.set(5.6, 1.75, 1); sp.renderOrder = 5;
  sp.position.copy(P3((z.x0 + z.x1) / 2, (z.y0 + z.y1) / 2, z0 + h + 200)); g.add(sp);
  ZONE[z.code] = { z, g, mat, edge, c, tex, sp }; }
let zoneT = 0;
function updateZones(dt){ const now = performance.now(); if (now - zoneT < 800) return; zoneT = now; const pulse = Date.now() % 1000 < 500;   // real time: slow GPUs still refresh
  for (const k in ZONE) { const Z = ZONE[k], z = Z.z, t = V[z.t], rh = V[z.h], co2 = V[z.c], oos = !!V[z.oos], al = ZALM.has(z.code), mv = V[z[METRIC]];
    Z.sp.visible = al || (FSEL !== 'all' && FSEL !== 'roof' && +FSEL === z.floor);
    Z.mat.color.copy(zoneColor(mv, oos, METRIC)); Z.mat.emissive.setHex(al && pulse ? 0x661111 : 0); Z.mat.opacity = oos ? .07 : .17;
    const g = Z.c.getContext('2d'); g.clearRect(0, 0, 512, 160); g.fillStyle = al ? 'rgba(120,16,16,.88)' : 'rgba(7,17,36,.82)'; g.beginPath(); g.roundRect(4, 4, 504, 152, 18); g.fill();
    g.fillStyle = '#9fb0c0'; g.font = '600 30px "Segoe UI",sans-serif'; g.fillText(`${z.code} · ${z.name}`.slice(0, 30), 18, 44);
    g.fillStyle = '#' + zoneColor(t, oos, 't').getHexString(); g.font = '700 64px "Segoe UI",sans-serif'; g.fillText(oos ? 'OOS' : (typeof t === 'number' ? t.toFixed(1) + '°C' : '—'), 18, 124);
    g.fillStyle = '#e8eef4'; g.font = '600 36px "Segoe UI",sans-serif'; g.fillText(typeof rh === 'number' ? rh.toFixed(0) + '%RH' : '', 250, 100);
    g.fillStyle = typeof co2 === 'number' && co2 > 1000 ? '#ffb4a8' : '#e8eef4'; g.fillText(typeof co2 === 'number' ? co2.toFixed(0) + ' ppm' : '', 250, 142); Z.tex.needsUpdate = true; }
  const lg = $('zlegend'); if (lg) { const [a, b, u] = MRANGE[METRIC]; lg.innerHTML = `<span>${a} ${u}</span><i></i><span>${b} ${u}</span>`; } }
// future systems: devices from the register appear as markers, status from their point
const SYSDEV = [];
for (const sy of M.systems) for (const d of sy.devices) { const g = new THREE.Group(); LAYER.systems.add(g); onFloor(d.floor, g); g.userData.sys = sy.id;
  const m = mesh(new THREE.SphereGeometry(.35, 18, 12), new THREE.MeshStandardMaterial({ color: new THREE.Color(sy.color), emissive: new THREE.Color(sy.color), emissiveIntensity: .2 }), g, P3(d.x, d.y, zOf(d.floor) + d.z));
  const t = textSprite(d.tag, 34, '#ffffff', null); t.position.copy(m.position).add(new THREE.Vector3(0, .6, 0)); t.scale.set(2.4, 1.2, 1); g.add(t); SYSDEV.push({ d, sy, m }); }
function updateSystems(t){ for (const o of SYSDEV) { const on = !!V[o.d.pt]; o.m.material.emissiveIntensity = on ? (Math.sin(t * 8) > 0 ? 2.5 : .3) : .2; o.m.scale.setScalar(on ? 1.4 : 1); } }
// floor filter: show floors up to the one selected (cut-away)
let FSEL = 'all';
let ISO = false;   // true = show only the selected floor (digital twin floor view)
const LAYCHK = k => { const c = document.querySelector(`[data-layer="${k}"]`); return !c || c.checked; };
function applyFloor(){ const plantOn = !ISO || FSEL === (BASEMENT ? '0' : '1') || FSEL === 'roof' || FSEL === 'all';
  const cut = BASEMENT && FSEL === '0'; for (const gm of [ground.material, apron.material]) { gm.transparent = cut; gm.opacity = cut ? .12 : 1; gm.depthWrite = !cut; } LAYER.plant.visible = plantOn && LAYCHK('plant'); LAYER.piping.visible = plantOn && LAYCHK('piping');
  for (const k in ZONE) ZONE[k].sp.scale.set(ISO ? 8.4 : 5.6, ISO ? 2.6 : 1.75, 1);
  for (const f in FLOORS) { const show = FSEL === 'all' || FSEL === 'roof' || (ISO ? +f === +FSEL : +f <= +FSEL); for (const o of FLOORS[f]) o.visible = show; }
  for (const id in LBL) LBL[id].dataset.hidden = EQ[id].g.visible && EQ[id].g.parent.visible ? '' : '1'; }
function initPanels(){ const lay = $('layers'); if (!lay) return;
  const names = { shell: 'Building (structure / glazing)', plant: 'Chiller plant', piping: 'CHW / CDW piping', air: 'Air side (AHU / fans)', zones: 'Legacy AirPlug zones (4 per floor)', systems: 'Other systems (fire / lighting ...)',
    ...(LAYER.office ? { office: 'Rooms (colour by temp / RH / CO2)', ducts: 'SA / RA / OA / EA ducts', terminals: 'VAV / diffusers / sensors / meters', airflow: 'Airflow in ducts (measured airflow)' } : {}),
    ...(LAYER.devices ? { devices: 'Field devices (Blender) / station points' } : {}) };
  lay.innerHTML = Object.entries(names).map(([k, n]) => `<label><input type="checkbox" data-layer="${k}" checked> ${n}</label>`).join('');
  lay.querySelectorAll('[data-layer]').forEach(c => c.onchange = () => { LAYER[c.dataset.layer].visible = c.checked; applyFloor(); });
  $('fsel').innerHTML = '<option value="all">All floors</option>' + (BASEMENT ? '<option value="0">B1 plant room</option>' : '') + [...Array(BLD.floors).keys()].map(i => `<option value="${i + 1}">Floor ${i + 1}</option>`).join('') + '<option value="roof">Roof</option>';
  const goFloor = () => { applyFloor(); if (FSEL === 'all') return flyTo(...VIEWS.iso.slice(0, 2)); const z = FSEL === 'roof' ? ROOFZ : zOf(+FSEL);
    flyTo([62, mm(z) + 34, 22], [32, mm(z) + 1.5, -20]); };
  $('fsel').onchange = e => { FSEL = e.target.value; goFloor(); };
  if ($('fiso')) $('fiso').onchange = e => { ISO = e.target.checked; applyFloor(); };
  if ($('zmetric')) $('zmetric').onchange = e => { METRIC = e.target.value; zoneT = 0; };
  const step = d => { const opts = ['all', ...(BASEMENT ? ['0'] : []), ...[...Array(BLD.floors).keys()].map(i => String(i + 1)), 'roof'], i = Math.max(0, Math.min(opts.length - 1, opts.indexOf(FSEL) + d)); FSEL = opts[i]; $('fsel').value = FSEL; goFloor(); };
  const nav = { navUp: () => step(1), navDn: () => step(-1), navIn: () => zoomBy(.6), navOut: () => zoomBy(1.6), navHome: () => { FSEL = 'all'; $('fsel').value = 'all'; ISO = false; if ($('fiso')) $('fiso').checked = false; applyFloor(); flyTo(...VIEWS.iso.slice(0, 2)); } };
  for (const k in nav) if ($(k)) $(k).onclick = nav[k];
  $('sysl').innerHTML = M.systems.map(sy => `<div><b style="color:${sy.color}">●</b> ${sy.name_th} <i>${sy.devices.length ? sy.devices.length + ' points' : 'planned · add devices in the register (sheet Systems)'}</i></div>`).join(''); }
// ------------------------------------------------------------------ V7.9 r4 office layer (R9 design: rooms, VAV, ducts, airflow)
// V7.9 r5: Blender field devices with station bindings (devices79.js); water / core drawn by the R9 layer
const DEVS = buildDevices({ scene, LAYER, onFloor, V, FAIL, glb, isDemo: () => DEMO, reapply: () => applyFloor() });
renderer.domElement.addEventListener('dblclick', ev => { if (!DEVS || !LAYER.devices.visible) return; const b = renderer.domElement.getBoundingClientRect();
  mp.set((ev.clientX - b.left) / b.width * 2 - 1, -(ev.clientY - b.top) / b.height * 2 + 1); ray.setFromCamera(mp, camera);
  if (ray.intersectObjects([...plant.children, ...LAYER.air.children], true).some(h => h.object.visible)) return;
  const dh = DEVS.pick(ray); if (dh) { ev.stopImmediatePropagation(); $('info').innerHTML = DEVS.info(dh); $('info').className = 'open'; } }, true);
initPanels();
window.__CAMSET = (p, t) => flyTo(p, t, 10); window.__DEVS = DEVS; window.__V = V; window.__EQ = EQ; window.__ZONE = ZONE; window.__PIPE = PIPE;  // test / diagnostics hooks (read only)
// ------------------------------------------------------------------ V7.9 r6: R9 office / architecture / airflow layer (r9office.js)
// S gives the R9 code the scene names it used inside the original page closure; the R9 code also wraps applyFloor / updateZones / ...
const S = Object.defineProperties({}, { $: { get: () => $ }, FAIL: { get: () => FAIL }, devicesFloor: { get: () => DEVS && DEVS.floorVis }, BLD: { get: () => BLD }, DEMO: { get: () => DEMO }, EQ: { get: () => EQ }, LAYCHK: { get: () => LAYCHK }, LAYER: { get: () => LAYER }, LBL: { get: () => LBL }, M: { get: () => M }, MAT: { get: () => MAT }, MRANGE: { get: () => MRANGE }, P3: { get: () => P3 }, PIPE: { get: () => PIPE }, ROOFZ: { get: () => ROOFZ }, T: { get: () => T }, V: { get: () => V }, VALVE: { get: () => VALVE }, ZONE: { get: () => ZONE }, apron: { get: () => apron }, box: { get: () => box }, camera: { get: () => camera }, canvasTex: { get: () => canvasTex }, cyl: { get: () => cyl }, flyTo: { get: () => flyTo }, ground: { get: () => ground }, hemi: { get: () => hemi }, isInst: { get: () => isInst }, mesh: { get: () => mesh }, mm: { get: () => mm }, mp: { get: () => mp }, onFloor: { get: () => onFloor }, ray: { get: () => ray }, renderer: { get: () => renderer }, scene: { get: () => scene }, sky: { get: () => sky }, sun: { get: () => sun }, svcMat: { get: () => svcMat }, textSprite: { get: () => textSprite }, trees: { get: () => trees }, zOf: { get: () => zOf }, zoomBy: { get: () => zoomBy },
  FSEL: { get: () => FSEL, set: v => { FSEL = v; } }, ISO: { get: () => ISO, set: v => { ISO = v; } }, METRIC: { get: () => METRIC, set: v => { METRIC = v; } }, applyFloor: { get: () => applyFloor, set: v => { applyFloor = v; } }, applyWeather: { get: () => applyWeather, set: v => { applyWeather = v; } }, updateGhosts: { get: () => updateGhosts, set: v => { updateGhosts = v; } }, updateZones: { get: () => updateZones, set: v => { updateZones = v; } } });
installR9(S);

// ------------------------------------------------------------------ loop
renderer.setAnimationLoop(() => { const dt = Math.min(.05, clock.getDelta()), t = clock.elapsedTime; flyStep(); controls.update();
  if (DEVS) DEVS.update(t, dt, { flow: !!($('flow') && $('flow').checked) });
  const W = weather(); applyWeather(W, t);
  if (rain.material.opacity > 0) { rain.position.y -= dt * 24; if (rain.position.y < -20) rain.position.y += 20; }
  updateGhosts(); applyAlarms(t); animate(t, dt); updateZones(dt); updateSystems(t); placeLabels(); renderer.render(scene, camera); });
renderAlarmList();
// point mapping panel: every station point the 3D page reads, its slot ORD and the value received
$('mapBtn').onclick = () => { const rows = window.MAP || []; const fmt = v => v === undefined ? '—' : typeof v === 'number' ? v.toFixed(2) : String(v);
  $('info').className = 'open wide'; const draw = () => { if (!$('info').classList.contains('wide')) return;
    const got = rows.filter(r => V[r.p] !== undefined).length, nf = rows.filter(r => FAIL.has(r.p)).length;
    $('info').innerHTML = `<h3>Point mapping · ${DEMO ? 'DEMO (simulated values)' : 'LIVE'} · values received ${got}/${rows.length} points${nf ? ` · not resolved ${nf} points` : ''} · alarm ${AL.filter(a => a.s).length} points${FAIL.size - nf > 0 ? ` (not resolved ${FAIL.size - nf})` : ''}</h3><button onclick="document.getElementById('info').className=''">off</button>
    <table>${rows.map(r => `<tr><td>${r.p}</td><td class="${V[r.p] === undefined ? 'no' : 'ok'}">${FAIL.has(r.p) ? 'not resolved' : fmt(V[r.p])}</td><td>${r.u}</td><td style="color:#9fb0c0">station:|slot:${r.s}</td></tr>`).join('')}</table>`; setTimeout(draw, 1000); }; draw(); };
