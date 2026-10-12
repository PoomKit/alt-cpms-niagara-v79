// V7.9 r5: R9 field devices, floor chilled-water branches and building core on the 3D page (window.OFFICE = R9 design,
// window.R9BIND = station point of each device from tools/r9_bindings.py).
//   devices : instruments on the pipes (TT / PT / FM / BTU / MBFV / PICV), AHU air devices (VSD, SAT / RAT / MAT, filter / duct DP,
//             OA airflow station, OA / RA / relief dampers), toilet-exhaust dampers, roof design units (KEF / TEF / MAU / relief fan).
//             Blender models (dev_*.glb) drawn instanced; a status lamp per device: green = station point live, amber = point not
//             resolved in LIVE, grey = no station point (design only, see docs/R9_POINT_COVERAGE.csv).
//   (r6: floor water branches, dampers and the building core are drawn by the R9 layer, r9office.js)
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

function basis(dir, offY, scale, stem){                                   // local x = pipe / duct axis, y = stem (up when possible)
  const x = dir.clone(); if (x.lengthSq() < 1e-9) x.set(1, 0, 0); x.normalize();
  let y, z;
  if (stem) { y = P(stem); y.addScaledVector(x, -y.dot(x)); }                // r7: stem side chosen by tools/r9_clash.py (clear of other pipes)
  if (stem && y.lengthSq() > 1e-6) { y.normalize(); z = new THREE.Vector3().crossVectors(x, y).normalize(); }
  else { const ref = Math.abs(x.y) > .9 ? new THREE.Vector3(Math.abs(x.x) > .9 ? 0 : 1, 0, Math.abs(x.x) > .9 ? 1 : 0) : new THREE.Vector3(0, 1, 0);
    z = new THREE.Vector3().crossVectors(x, ref).normalize(); y = new THREE.Vector3().crossVectors(z, x).normalize(); }
  const m = new THREE.Matrix4().makeBasis(x, y, z);
  if (offY) m.multiply(new THREE.Matrix4().makeTranslation(0, offY, 0));
  return m.multiply(new THREE.Matrix4().makeScale(...(Array.isArray(scale) ? scale : [scale, scale, scale]))); }

export function buildDevices(ctx){
  const { scene, LAYER, onFloor, V, FAIL, glb, isDemo, reapply } = ctx, OD = window.OFFICE, BIND = window.R9BIND || {};
  if (!OD) return null;
  const root = { devices: new THREE.Group() };
  for (const k in root) { scene.add(root[k]); LAYER[k] = root[k]; }
  const fz = { 0: -6.0, 9: 34.9 }; for (const s of OD.roomSensors || []) fz[s.floor] = s.position[2] - s.height_m;
  const top = f => (fz[f + 1] ?? fz[f] + 4.2);

  // ---------------------------------------------------------------- device records (one per R9 device drawn)
  const DEV = [], integral = new Set((OD.motorizedDampers || []).filter(d => d.integralVAV).map(d => d.id));   // integral MDs = the VAV box
  for (const d of OD.instruments || []) { const mdl = MODEL_OF[d.kind], r = d.radius || .05, ref = PIPE_REF[mdl];
    const s = ref ? Math.max(.35, Math.min(3, r / ref)) : 1, off = ref ? 0 : r + (d.insulation || 0) - .1;   // taps sit on the insulation
    DEV.push({ d, kind: d.kind, f: d.floor, mdl, pos: P(d.position), m: basis(P(d.direction || [1, 0, 0]), off, s, d.stem), lamp: .18 + r * 1.6 + (ref ? 0 : d.insulation || 0) }); }
  for (const d of OD.ahuAirDevices || []) { const mdl = MODEL_OF[d.kind];
    DEV.push({ d, kind: d.kind, f: d.floor, mdl, pos: P(d.position), m: basis(new THREE.Vector3(1, 0, 0), 0, d.kind === 'AirMD' ? [1, .55, .7] : 1), lamp: .45 }); }
  // r6: motorised dampers (integral VAV and toilet exhaust) are drawn by the R9 layer with a blade that follows the feedback
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
        im.userData.devs = list; im.computeBoundingSphere(); root.devices.add(im); onFloor(+f, im); PICK.push(im); } }
    if (reapply) reapply(); });   // r6: models load after the floor filter ran

  // status lamps (one instanced sphere set per floor, colour per device)
  const LAMPS = []; const lampG = new THREE.SphereGeometry(.032, 10, 8), lampM = new THREE.MeshBasicMaterial({ toneMapped: false });
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
      const fw = o.getObjectByName('fanWheel'); UNITS.find(x => x.g === g).spin = fw; if (reapply) reapply(); }); }

  // r6: floor chilled-water branches, shafts, lifts, stairs and tenant doors are drawn by the R9 layer (r9office.js)
  // ---------------------------------------------------------------- live update
  const num = k => (typeof V[k] === 'number' ? V[k] : typeof V[k] === 'boolean' ? (V[k] ? 100 : 0) : undefined);
  const C_OK = new THREE.Color(0x22c55e), C_WARN = new THREE.Color(0xf59e0b), C_NONE = new THREE.Color(0x475569);
  let last = 0;
  function state(r){ if (!r.p) return 'none'; if (FAIL && FAIL.has(r.p)) return 'fail'; return isDemo() || V[r.p] !== undefined ? 'ok' : 'fail'; }
  function update(t, dt, opts){
    if (performance.now() - last > 900) { last = performance.now();
      for (const L of LAMPS) { L.list.forEach((r, i) => { const s = state(r); L.im.setColorAt(i, s === 'ok' ? C_OK : s === 'fail' ? C_WARN : C_NONE); }); L.im.instanceColor.needsUpdate = true; } }
    const show = opts.flow;
    root.devices.visible = !document.getElementById('officeInstruments') || document.getElementById('officeInstruments').checked;
    for (const u of UNITS) if (u.spin) u.spin.rotation.y += dt * (isDemo() ? 6 : 0);
  }
  function pick(ray){ const h = ray.intersectObjects(PICK.filter(o => o.visible && o.parent.visible), false)[0];
    if (h && h.instanceId !== undefined) return { r: h.object.userData.devs[h.instanceId] };
    const u = ray.intersectObjects(UNITS.map(x => x.g).filter(g => g.visible), true)[0]; if (!u) return null;
    let o = u.object; while (o && !o.userData.unit) o = o.parent; return o ? { u: o.userData.unit } : null; }
  function info(hit){ const fmt = v => v === undefined ? '—' : typeof v === 'number' ? v.toFixed(2) : String(v);
    if (hit.u) { const u = hit.u; return `<h3>${u.id}</h3><table><tr><td>Type</td><td>${KIND_TH[u.type] || u.type}</td></tr><tr><td>Floor</td><td>${u.floor === 9 ? 'Roof' : u.floor}</td></tr>
      <tr><td>Size (m)</td><td>${u.size.join(' × ')}</td></tr><tr><td>Station point</td><td class="no">none (R9 design unit only)</td></tr><tr><td>Design status</td><td>${u.status || 'Proposed / unbound'}</td></tr></table>`; }
    const r = hit.r, d = r.d, s = state(r);
    const rows = [['Type', KIND_TH[r.kind] || r.kind], ['Floor', d.floor === 0 ? 'B1' : d.floor === 9 ? 'Roof' : d.floor], ['Equipment / pipe', [d.equipment, d.pipe, d.room].filter(Boolean).join(' · ') || '—'],
      ['Station point', r.p ? `${r.p}<br><span class="hint">${r.s}</span>` : '<span class="no">none — see docs/R9_POINT_COVERAGE.csv</span>'],
      ['Value', r.p ? `<b class="${s === 'ok' ? 'ok' : 'no'}">${fmt(V[r.p])}</b>${s === 'fail' ? ' (LIVE: not resolved)' : ''}` : '—'], ['R9 design status', d.status || d.control || '—']];
    if (d.note) rows.push(['Note', d.note]);
    return `<h3>${d.id}</h3><table>${rows.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('')}</table>`; }
  function demo(t){ for (const r of DEV) if (r.p && V[r.p] === undefined) V[r.p] = /Temp|SAT|RAT|MAT|LAT|TT_/.test(r.p) ? 12 + 2 * Math.sin(t / 30 + r.i) : 40 + 20 * Math.sin(t / 40 + r.i); }
  function floorVis(vis){ for (const o of root.devices.children) if (o.userData.floor !== undefined) o.visible = vis(o.userData.floor); }
  const stats = () => ({ devices: DEV.length, bound: DEV.filter(r => r.p).length, units: UNITS.length, instanced: PICK.length });
  return { update, pick, info, demo, stats, floorVis, DEV };
}
