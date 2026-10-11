// V7.9 r5: R9 field devices, floor chilled-water branches and building core on the 3D page (window.OFFICE = R9 design,
// window.R9BIND = station point of each device from tools/r9_bindings.py).
//   devices : instruments on the pipes (TT / PT / FM / BTU / MBFV / PICV), AHU air devices (VSD, SAT / RAT / MAT, filter / duct DP,
//             OA airflow station, OA / RA / relief dampers), toilet-exhaust dampers, roof design units (KEF / TEF / MAU / relief fan).
//             Blender models (dev_*.glb) drawn instanced; a status lamp per device: green = station point live, amber = point not
//             resolved in LIVE, grey = no station point (design only, see docs/R9_POINT_COVERAGE.csv).
//   water   : CHS / CHR floor branches riser -> floor meter -> AHU coil, insulated, water particles only while the coil valve is open.
//   arch    : MEP / exhaust shafts, lifts, fire stairs and tenant entrances of the R9 core.
// Coordinates of the design file: metres, x east, y north, z up -> page (x, z, -y).
import * as THREE from 'three';

const P = ([x, y, z]) => new THREE.Vector3(x, z, -y);
const pad = n => String(n).padStart(2, '0');
const MODEL_OF = { TT: 'dev_tt', PT: 'dev_pt', MBFV: 'dev_mbfv', FM: 'dev_fm', BTU: 'dev_btu', PICV: 'dev_picv', MD: 'dev_md', VSD: 'dev_vsd',
  AirTT: 'dev_airtt', AirDP: 'dev_airdp', AirFlow: 'dev_afms', AirMD: 'dev_md' };
const PIPE_REF = { dev_mbfv: .1, dev_picv: .035, dev_fm: .1 };          // models sized by the pipe radius (others sit on the pipe surface)
const KIND_TH = { TT: 'Temperature transmitter', PT: 'Pressure transmitter', FM: 'Flow meter (electromagnetic)', BTU: 'BTU / energy meter',
  MBFV: 'Motorised butterfly valve', PICV: 'Pressure-independent control valve', MD: 'Motorised damper', VSD: 'Variable speed drive',
  AirTT: 'Duct temperature sensor', AirDP: 'Differential pressure transmitter', AirFlow: 'Airflow measuring station', AirMD: 'AHU damper + actuator',
  fan: 'Roof fan (R9 design)', ahu: 'Make-up air unit (R9 design)' };

function basis(dir, offY, scale){                                         // local x = pipe / duct axis, y = stem (up when possible)
  const x = dir.clone(); if (x.lengthSq() < 1e-9) x.set(1, 0, 0); x.normalize();
  const ref = Math.abs(x.y) > .9 ? new THREE.Vector3(Math.abs(x.x) > .9 ? 0 : 1, 0, Math.abs(x.x) > .9 ? 1 : 0) : new THREE.Vector3(0, 1, 0);
  const z = new THREE.Vector3().crossVectors(x, ref).normalize(), y = new THREE.Vector3().crossVectors(z, x).normalize();
  const m = new THREE.Matrix4().makeBasis(x, y, z);
  if (offY) m.multiply(new THREE.Matrix4().makeTranslation(0, offY, 0));
  return m.multiply(new THREE.Matrix4().makeScale(...(Array.isArray(scale) ? scale : [scale, scale, scale]))); }

export function buildDevices(ctx){
  const { scene, LAYER, onFloor, V, FAIL, glb, isDemo } = ctx, OD = window.OFFICE, BIND = window.R9BIND || {};
  if (!OD) return null;
  const root = { devices: new THREE.Group(), water: new THREE.Group(), arch: new THREE.Group() };
  for (const k in root) { scene.add(root[k]); LAYER[k] = root[k]; }
  const fz = { 0: -6.0, 9: 34.9 }; for (const s of OD.roomSensors || []) fz[s.floor] = s.position[2] - s.height_m;
  const top = f => (fz[f + 1] ?? fz[f] + 4.2);

  // ---------------------------------------------------------------- device records (one per R9 device drawn)
  const DEV = [], integral = new Set((OD.motorizedDampers || []).filter(d => d.integralVAV).map(d => d.id));   // integral MDs = the VAV box
  for (const d of OD.instruments || []) { const mdl = MODEL_OF[d.kind], r = d.radius || .05, ref = PIPE_REF[mdl];
    const s = ref ? Math.max(.35, Math.min(3, r / ref)) : 1, off = ref ? 0 : r - .1;
    DEV.push({ d, kind: d.kind, f: d.floor, mdl, pos: P(d.position), m: basis(P(d.direction || [1, 0, 0]), off, s), lamp: .18 + r * 1.6 }); }
  for (const d of OD.ahuAirDevices || []) { const mdl = MODEL_OF[d.kind];
    DEV.push({ d, kind: d.kind, f: d.floor, mdl, pos: P(d.position), m: basis(new THREE.Vector3(1, 0, 0), 0, d.kind === 'AirMD' ? [1, .55, .7] : 1), lamp: .45 }); }
  for (const d of OD.motorizedDampers || []) { if (integral.has(d.id)) continue;
    DEV.push({ d, kind: 'MD', f: d.floor, mdl: 'dev_md', pos: P(d.position), m: basis(P(d.direction || [1, 0, 0]), 0, [1, d.h || .2, d.w || .2]), lamp: (d.h || .2) / 2 + .1 }); }
  for (const r of DEV) { const b = BIND[r.d.id]; r.p = b ? b.p : null; r.s = b ? b.s : null; }

  // instanced Blender models, one InstancedMesh per floor x model part
  const byModel = {}; DEV.forEach((r, i) => { r.i = i; (byModel[r.mdl] = byModel[r.mdl] || []).push(r); });
  const PICK = [];
  for (const name in byModel) glb(name, model => { model.updateMatrixWorld(true); const parts = [];
    model.traverse(o => { if (o.isMesh) parts.push({ g: o.geometry, mat: o.material, mw: o.matrixWorld.clone() }); });
    const perFloor = {}; for (const r of byModel[name]) (perFloor[r.f] = perFloor[r.f] || []).push(r);
    for (const f in perFloor) { const list = perFloor[f];
      for (const pt of parts) { const im = new THREE.InstancedMesh(pt.g, pt.mat, list.length); im.castShadow = false; im.receiveShadow = true;
        list.forEach((r, i) => im.setMatrixAt(i, new THREE.Matrix4().makeTranslation(r.pos.x, r.pos.y, r.pos.z).multiply(r.m).multiply(pt.mw)));
        im.userData.devs = list; im.computeBoundingSphere(); root.devices.add(im); onFloor(+f, im); PICK.push(im); } } });

  // status lamps (one instanced sphere set per floor, colour per device)
  const LAMPS = []; const lampG = new THREE.SphereGeometry(.045, 10, 8), lampM = new THREE.MeshBasicMaterial({ toneMapped: false });
  const lampFloor = {}; for (const r of DEV) (lampFloor[r.f] = lampFloor[r.f] || []).push(r);
  for (const f in lampFloor) { const list = lampFloor[f], im = new THREE.InstancedMesh(lampG, lampM, list.length);
    list.forEach((r, i) => { const up = new THREE.Vector3(0, 1, 0).applyMatrix4(new THREE.Matrix4().extractRotation(r.m)).normalize();
      im.setMatrixAt(i, new THREE.Matrix4().makeTranslation(r.pos.x + up.x * r.lamp, r.pos.y + up.y * r.lamp, r.pos.z + up.z * r.lamp)); im.setColorAt(i, new THREE.Color(0x64748b)); });
    root.devices.add(im); onFloor(+f, im); LAMPS.push({ im, list }); }

  // roof design units (R9 KEF / TEF / MAU / relief fan): Blender models scaled to the design size, no station point
  const UNITS = [];
  for (const u of OD.equipment || []) { const g = new THREE.Group(); g.position.copy(P(u.position)); root.devices.add(g); onFloor(u.floor, g);
    const [w, d, h] = u.size, name = u.type === 'ahu' ? 'oau' : 'roof_fan', ref = u.type === 'ahu' ? [4.2, 2.0, 2.2] : [1.2, 1.2, 1.1];
    g.userData.unit = u; UNITS.push({ u, g, spin: null });
    glb(name, model => { const o = model.clone(true); o.scale.set(w / ref[0], h / ref[2], d / ref[1]); g.add(o);
      const fw = o.getObjectByName('fanWheel'); UNITS.find(x => x.g === g).spin = fw; }); }

  // ---------------------------------------------------------------- floor chilled-water branches (insulated) + water particles
  const PC = OD.pipeColors || { CHS: '#1559d6', CHR: '#57c5f5' }, tmp = new THREE.Object3D(), Y = new THREE.Vector3(0, 1, 0);
  const pipeMat = {}, segsBy = {}, PIPES = [];
  for (const w of OD.waterPipes || []) { const pts = w.points.map(P), r = (w.outsideRadius_m || .03) + .025, segs = [];   // + 25 mm insulation
    for (let i = 0; i + 1 < pts.length; i++) { const a = pts[i], b = pts[i + 1], L = a.distanceTo(b); if (L > .005) segs.push({ a, b, L }); }
    const key = w.floor + '|' + w.service; (segsBy[key] = segsBy[key] || []).push(...segs.map(s => ({ ...s, r })));
    const valve = valveOf(w.id), len = segs.reduce((s, x) => s + x.L, 0); PIPES.push({ w, segs, len, valve, back: w.service === 'CHR' }); }
  function valveOf(id){ let m = id.match(/F(\d\d)-METER-FEED$/); if (m) return +m[1] === 1 ? ['AHU01_ValveCmd', 'AHU02_ValveCmd'] : [`AHU_F${m[1]}_ValveCmd`];
    m = id.match(/-(AHU|OAU)-(\d\d)-COIL$/); if (m) return [`${m[1]}${m[2]}_ValveCmd`]; return []; }
  for (const key in segsBy) { const [f, svc] = key.split('|'), list = segsBy[key];
    const mat = pipeMat[svc] || (pipeMat[svc] = new THREE.MeshStandardMaterial({ color: new THREE.Color(PC[svc] || '#8899aa').lerp(new THREE.Color(0xffffff), .18), roughness: .55, metalness: .1 }));
    const im = new THREE.InstancedMesh(new THREE.CylinderGeometry(1, 1, 1, 18), mat, list.length), el = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 14, 10), mat, list.length);
    list.forEach((s, i) => { tmp.position.copy(s.a).add(s.b).multiplyScalar(.5); tmp.quaternion.setFromUnitVectors(Y, s.b.clone().sub(s.a).normalize()); tmp.scale.set(s.r, s.L, s.r);
      tmp.updateMatrix(); im.setMatrixAt(i, tmp.matrix); tmp.position.copy(s.b); tmp.scale.setScalar(s.r * 1.02); tmp.quaternion.identity(); tmp.updateMatrix(); el.setMatrixAt(i, tmp.matrix); });
    for (const o of [im, el]) { root.water.add(o); onFloor(+f, o); } }
  const WP = []; const wpG = new THREE.SphereGeometry(.035, 8, 6);
  for (const p of PIPES) { if (!p.len) continue; const n = Math.max(3, Math.round(p.len / .5)), m = new THREE.MeshBasicMaterial({ color: PC[p.w.service] || '#9cf', toneMapped: false });
    const im = new THREE.InstancedMesh(wpG, m, n); im.frustumCulled = false; root.water.add(im); onFloor(p.w.floor, im); WP.push({ p, im, n }); }
  function along(p, u){ let d = u * p.len; for (const s of p.segs) { if (d <= s.L) return s.a.clone().lerp(s.b, d / s.L); d -= s.L; } return p.segs[p.segs.length - 1].b.clone(); }

  // ---------------------------------------------------------------- building core: shafts, lifts, fire stairs, tenant entrances
  const VT = OD.verticalTransport || {}, edgeM = c => new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: .65 });
  const vol = (rect, z0, z1, color, op, f, label) => { const [x0, y0, x1, y1] = rect, g = new THREE.Group(); root.arch.add(g); onFloor(f, g);
    const geo = new THREE.BoxGeometry(x1 - x0, z1 - z0, y1 - y0), c = new THREE.Vector3((x0 + x1) / 2, (z0 + z1) / 2, -(y0 + y1) / 2);
    const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color, transparent: true, opacity: op, depthWrite: false, roughness: .8 })); m.position.copy(c); g.add(m);
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo), edgeM(color)); e.position.copy(c); g.add(e); return g; };
  const SHC = { 'MEP-RISER': 0x3b82f6, 'KITCHEN-EA': 0xf97316, 'MAKEUP-AIR': 0x22c55e, 'TOILET-EA': 0xa855f7, 'AHU-RELIEF': 0x94a3b8 };
  for (let f = 0; f <= 8; f++) { const z0 = fz[f], z1 = top(f) - .05;
    for (const s of OD.shafts || []) if (f >= 1 || s.id === 'MEP-RISER') vol(s.rect, z0, z1, SHC[s.id] || 0x94a3b8, .07, f);
    for (const l of VT.lifts || []) { vol(l.rect, z0, z1, 0x9aa5b1, .05, f); }
    for (const s of VT.fireStairs || []) { const g = vol(s.rect, z0, z1, 0xdc2626, .06, f), [x0, y0, x1, y1] = s.rect, h = z1 - z0, run = (y1 - y0) * .62, wFl = (x1 - x0) / 2 - .1;
      const sm = new THREE.MeshStandardMaterial({ color: 0xb8b2a7, roughness: .9 });
      for (const k of [0, 1]) { const flight = new THREE.Mesh(new THREE.BoxGeometry(wFl, .18, Math.hypot(run, h / 2)), sm);
        flight.position.set(x0 + .05 + wFl / 2 + k * (wFl + .1), z0 + h / 4 + k * h / 2, -(y0 + (y1 - y0) / 2)); flight.rotation.x = (k ? -1 : 1) * Math.atan2(h / 2, run); g.add(flight); }
      const land = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 - .1, .18, (y1 - y0) * .18), sm); land.position.set((x0 + x1) / 2, z0 + h / 2, -(y1 - (y1 - y0) * .1)); g.add(land); } }
  const carM = new THREE.MeshStandardMaterial({ color: 0xc9ced3, metalness: .7, roughness: .3 });
  (VT.lifts || []).forEach((l, i) => { const [x0, y0, x1, y1] = l.rect, f = i ? 5 : 1, car = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 - .4, 2.3, y1 - y0 - .4), carM);
    car.position.set((x0 + x1) / 2, fz[f] + 1.2, -(y0 + y1) / 2); root.arch.add(car); onFloor(f, car); });
  const doorM = new THREE.MeshStandardMaterial({ color: 0x3f4448, metalness: .6, roughness: .4 }), leafM = new THREE.MeshStandardMaterial({ color: 0x9db8c2, transparent: true, opacity: .35, depthWrite: false });
  for (const d of OD.tenantEntrances || []) { const t = (OD.tenancies || []).find(x => x.floor === d.floor && x.company === d.tenant), [x, y, z] = d.position, w = d.clearWidth_m || 1.1;
    const alongY = t ? Math.min(Math.abs(x - t.rect[0]), Math.abs(x - t.rect[2])) < .1 : false, g = new THREE.Group(); g.position.copy(P([x, y, fz[d.floor] ?? z])); if (alongY) g.rotation.y = Math.PI / 2;
    for (const s of [-1, 1]) { const post = new THREE.Mesh(new THREE.BoxGeometry(.06, 2.2, .12), doorM); post.position.set(s * (w / 2 + .03), 1.1, 0); g.add(post); }
    const lin = new THREE.Mesh(new THREE.BoxGeometry(w + .12, .08, .12), doorM); lin.position.set(0, 2.24, 0); g.add(lin);
    const leaf = new THREE.Mesh(new THREE.BoxGeometry(w, 2.15, .02), leafM); leaf.position.set(0, 1.08, 0); g.add(leaf); root.arch.add(g); onFloor(d.floor, g); }

  // ---------------------------------------------------------------- live update
  const num = k => (typeof V[k] === 'number' ? V[k] : typeof V[k] === 'boolean' ? (V[k] ? 100 : 0) : undefined);
  const C_OK = new THREE.Color(0x22c55e), C_WARN = new THREE.Color(0xf59e0b), C_NONE = new THREE.Color(0x475569);
  let last = 0;
  function state(r){ if (!r.p) return 'none'; if (FAIL && FAIL.has(r.p)) return 'fail'; return isDemo() || V[r.p] !== undefined ? 'ok' : 'fail'; }
  function update(t, dt, opts){
    if (performance.now() - last > 900) { last = performance.now();
      for (const L of LAMPS) { L.list.forEach((r, i) => { const s = state(r); L.im.setColorAt(i, s === 'ok' ? C_OK : s === 'fail' ? C_WARN : C_NONE); }); L.im.instanceColor.needsUpdate = true; } }
    const show = opts.flow;
    for (const o of WP) { const v = Math.max(0, ...o.p.valve.map(k => num(k) ?? 0)), on = show && v > 5 && root.water.visible;
      o.im.count = on ? o.n : 0; if (!on) continue; const sp = .25 + .9 * Math.min(1, v / 100);
      for (let i = 0; i < o.n; i++) { let u = ((t * sp / Math.max(o.p.len, 1)) * 3 + i / o.n) % 1; if (o.p.back) u = 1 - u;
        tmp.position.copy(along(o.p, u)); tmp.quaternion.identity(); tmp.scale.setScalar(1); tmp.updateMatrix(); o.im.setMatrixAt(i, tmp.matrix); }
      o.im.instanceMatrix.needsUpdate = true; }
    for (const u of UNITS) if (u.spin) u.spin.rotation.y += dt * (isDemo() ? 6 : 0);
  }
  function pick(ray){ const h = ray.intersectObjects(PICK.filter(o => o.visible && o.parent.visible), false)[0];
    if (h && h.instanceId !== undefined) return { r: h.object.userData.devs[h.instanceId] };
    const u = ray.intersectObjects(UNITS.map(x => x.g).filter(g => g.visible), true)[0]; if (!u) return null;
    let o = u.object; while (o && !o.userData.unit) o = o.parent; return o ? { u: o.userData.unit } : null; }
  function info(hit){ const fmt = v => v === undefined ? '—' : typeof v === 'number' ? v.toFixed(2) : String(v);
    if (hit.u) { const u = hit.u; return `<h3>${u.id}</h3><table><tr><td>ประเภท</td><td>${KIND_TH[u.type] || u.type}</td></tr><tr><td>ชั้น</td><td>${u.floor === 9 ? 'ดาดฟ้า' : u.floor}</td></tr>
      <tr><td>ขนาด (m)</td><td>${u.size.join(' × ')}</td></tr><tr><td>จุดใน station</td><td class="no">ไม่มี (หน่วยตามแบบ R9 เท่านั้น)</td></tr><tr><td>สถานะแบบ</td><td>${u.status || 'Proposed / unbound'}</td></tr></table>`; }
    const r = hit.r, d = r.d, s = state(r);
    const rows = [['ประเภท', KIND_TH[r.kind] || r.kind], ['ชั้น', d.floor === 0 ? 'B1' : d.floor === 9 ? 'ดาดฟ้า' : d.floor], ['อุปกรณ์ / ท่อ', [d.equipment, d.pipe, d.room].filter(Boolean).join(' · ') || '—'],
      ['จุดใน station', r.p ? `${r.p}<br><span class="hint">${r.s}</span>` : '<span class="no">ไม่มี — ดู docs/R9_POINT_COVERAGE.csv</span>'],
      ['ค่า', r.p ? `<b class="${s === 'ok' ? 'ok' : 'no'}">${fmt(V[r.p])}</b>${s === 'fail' ? ' (LIVE: resolve ไม่ได้)' : ''}` : '—'], ['สถานะแบบ R9', d.status || d.control || '—']];
    if (d.note) rows.push(['หมายเหตุ', d.note]);
    return `<h3>${d.id}</h3><table>${rows.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('')}</table>`; }
  function demo(t){ for (const r of DEV) if (r.p && V[r.p] === undefined) V[r.p] = /Temp|SAT|RAT|MAT|LAT|TT_/.test(r.p) ? 12 + 2 * Math.sin(t / 30 + r.i) : 40 + 20 * Math.sin(t / 40 + r.i); }
  const stats = () => ({ devices: DEV.length, bound: DEV.filter(r => r.p).length, units: UNITS.length, pipes: PIPES.length, instanced: PICK.length });
  return { update, pick, info, demo, stats, DEV };
}
