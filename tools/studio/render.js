const { chromium } = require('playwright'); const fs = require('fs');
const path = require('path');
const G3D = path.resolve(__dirname, '..', '..', 'graphics3d');                  // mk.py writes graphics3d/studio/studio.html
const OUT = process.env.STUDIO_OUT || path.join(G3D, 'studio', 'raw'); fs.mkdirSync(OUT, { recursive: true });
const JOBS = [
  { name: 'chiller', ids: ['CH-01'], az: -22, el: 22, ppm: 120, frames: 1,
    anc: e => { const L = e.L / 1000; return { chw_in: [-L*.5-.31, .9, .18], chw_out: [-L*.5-.31, 1.26, .18], cdw_in: [L*.5+.56, .46, -.22], cdw_out: [L*.5+.56, .78, -.22] }; } },
  { name: 'pump', ids: ['CHP-01'], az: 20, el: 18, ppm: 120, frames: 1,
    anc: e => { const L = e.L / 1000; return { suction: [-L*.44-.15, .62, 0], discharge: [-L*.3, 1.11, 0] }; } },
  { name: 'ct', ids: ['CT-01/1', 'CT-01/2'], az: 150, el: 24, ppm: 80, frames: 8,
    anc: e => { const L = e.L / 1000, H = e.H / 1000, D = e.W / 1000; return { in1: [-L*.3, H+.25, 0], in2: [2.8 + L*.3, H+.25, 0], out: [1.4, .2, D/2], mu: [-L/2, .35, D/2] }; } },
];
(async () => {
  const b = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 900, height: 700 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.join(G3D, 'studio', 'studio.html'), { waitUntil: 'load', timeout: 200000 }); await p.waitForTimeout(8000);
  await p.evaluate(() => { const S = __S, T = S.THREE; S.renderer.setAnimationLoop(null); S.renderer.setPixelRatio(1);
    S.scene.background = null; S.scene.fog = null; S.renderer.setClearColor(0x000000, 0);
    S.scene.environment = S.pmrem.fromScene(new S.RoomEnvironment(), .04).texture; S.scene.environmentIntensity = .9; S.renderer.toneMappingExposure = 1.05;
    const st = new T.Group(); st.name = 'studio'; S.scene.add(st);
    const d = new T.DirectionalLight(0xffffff, 2.6); d.position.set(-30, 60, 80); st.add(d); st.add(d.target);
    const d2 = new T.DirectionalLight(0xdfe8ff, .8); d2.position.set(60, 30, -40); st.add(d2);
    st.add(new T.HemisphereLight(0xeef4ff, 0x404040, .7)); window.__ST = st; });
  for (const j of JOBS) {
    const res = await p.evaluate(async (j) => { const S = __S, T = S.THREE, anc = eval(j.anc);
      const tg = j.ids.map(id => S.EQ[id].g), keep = new Set([__ST, ...tg]), up = new Set();
      for (const g of [...tg, __ST]) { let o = g.parent; while (o) { up.add(o); o = o.parent; } }
      tg.forEach(g => g.visible = true);
      (function walk(o){ if (keep.has(o)) return; if (up.has(o)) { o.visible = true; o.children.forEach(walk); } else o.visible = false; })(S.scene);
      const g0 = tg[0]; g0.updateMatrixWorld(true); const q = g0.getWorldQuaternion(new T.Quaternion());
      const az = j.az * Math.PI / 180, el = j.el * Math.PI / 180;
      const dir = new T.Vector3(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).applyQuaternion(q);
      const box = new T.Box3(); tg.forEach(g => box.expandByObject(g)); const c = box.getCenter(new T.Vector3()), R = box.getSize(new T.Vector3()).length();
      const cam = new T.OrthographicCamera(-1, 1, 1, -1, .1, R * 4); cam.position.copy(c).addScaledVector(dir, R * 2); cam.up.set(0, 1, 0); cam.lookAt(c); cam.updateMatrixWorld();
      const right = new T.Vector3().setFromMatrixColumn(cam.matrixWorld, 0), upv = new T.Vector3().setFromMatrixColumn(cam.matrixWorld, 1);
      let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
      tg.forEach(g => g.traverse(o => { if (!o.isMesh || !o.visible || !o.geometry) return; o.geometry.computeBoundingBox(); const bb = o.geometry.boundingBox;
        for (const x of [bb.min.x, bb.max.x]) for (const y of [bb.min.y, bb.max.y]) for (const z of [bb.min.z, bb.max.z]) {
          const v = new T.Vector3(x, y, z).applyMatrix4(o.matrixWorld).sub(c); const a = v.dot(right), b = v.dot(upv);
          x0 = Math.min(x0, a); x1 = Math.max(x1, a); y0 = Math.min(y0, b); y1 = Math.max(y1, b); } }));
      const m = .06; x0 -= m; x1 += m; y0 -= m; y1 += m;
      Object.assign(cam, { left: x0, right: x1, top: y1, bottom: y0 }); cam.updateProjectionMatrix();
      const W = Math.round((x1 - x0) * j.ppm), H = Math.round((y1 - y0) * j.ppm); S.renderer.setSize(W, H, false);
      const A = {}; const e = S.EQ[j.ids[0]].e; for (const [k, v] of Object.entries(anc(e))) { const w = g0.localToWorld(new T.Vector3(...v)).sub(c);
        A[k] = [Math.round((w.dot(right) - x0) * j.ppm), Math.round((y1 - w.dot(upv)) * j.ppm)]; }
      const frames = []; const fans = []; j.ids.forEach(id => (S.EQ[id].spin || []).forEach(s => { if (s.fan) fans.push(s.m); }));
      for (let f = 0; f < j.frames; f++) { fans.forEach(m => m.rotation.y = f * Math.PI / 3 / j.frames); S.renderer.render(S.scene, cam); frames.push(S.renderer.domElement.toDataURL('image/png')); }
      return { W, H, A, frames }; }, { ...j, anc: j.anc.toString() });
    res.frames.forEach((d, i) => fs.writeFileSync(`${OUT}/${j.name}_${i}.png`, Buffer.from(d.split(',')[1], 'base64')));
    fs.writeFileSync(`${OUT}/${j.name}.json`, JSON.stringify({ size: [res.W, res.H], anchors: res.A, ppm: j.ppm }));
    console.log(j.name, res.W, res.H, JSON.stringify(res.A));
  }
  console.log('errors', JSON.stringify(errs.slice(0, 3))); process.exit(0); })();
